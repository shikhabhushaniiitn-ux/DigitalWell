"""Transparent goal-to-resource suggestions and a session-only next-step plan."""

import streamlit as st

from src.components import get_resources, image, resource_card
from src.content import FINDER_GOALS, GUIDES, TOPICS

GOAL_TOPICS = {
    "I want to focus better": "focus",
    "I want to reduce distracting screen time": "screen-time",
    "I want healthier bedtime habits": "sleep",
    "I want to improve my online privacy": "privacy",
}
DEVICE_SETTING_IDS = {"google-dw", "apple-screen-time", "stayfocusd", "leechblock", "firefox-etp", "privacy-badger"}

st.title("Resource Finder", icon=":material/lightbulb:")
intro, visual = st.columns([1.15, 0.85], vertical_alignment="center")
with intro:
    st.caption("Choose a goal, explore relevant resources, and pick one manageable next step.")
    st.info("Suggestions use the existing fixed topic-to-resource mappings. They are not AI, clinical advice, or a claim that a tool will produce a particular outcome.", icon=":material/info:")
with visual:
    image("student-study-hero.jpg", "A student writes study notes beside a laptop, representing planning a manageable next step.")


def reset_plan() -> None:
    for key in list(st.session_state.keys()):
        if key.startswith("finder_step_"):
            del st.session_state[key]
    st.session_state.pop("finder_goal", None)
    st.session_state.pop("finder_action_type", None)
    st.session_state.pop("finder_target", None)


with st.form("goal_finder"):
    st.markdown("### Step 1 · Choose a goal")
    goal_choice = st.selectbox("What would you like help with?", list(FINDER_GOALS), key="finder_goal_choice")
    submitted = st.form_submit_button("Show relevant resources", width="stretch")
if submitted:
    if st.session_state.get("finder_goal") != goal_choice:
        reset_plan()
    st.session_state["finder_goal"] = goal_choice

goal = st.session_state.get("finder_goal")
if goal:
    mapping = FINDER_GOALS[goal]
    st.markdown("## Step 2 · Explore relevant resources")
    st.write(mapping["description"])
    st.caption("Why these appear: this goal maps to the resource IDs listed for its topic in `src/content.py`. The app does not rank or score the options.")
    resources = get_resources()
    suggestions = resources[resources["id"].isin(mapping["resources"])]
    for start in range(0, len(suggestions), 2):
        columns = st.columns(2)
        for column, (_, row) in zip(columns, suggestions.iloc[start : start + 2].iterrows()):
            with column:
                resource_card(row, compact=True)

    st.markdown("## Step 3 · Choose one next action")
    action_options = ["Read a resource", "Review a device setting", "Explore a related topic"]
    if mapping["guides"]:
        action_options.insert(1, "Follow a setup guide")
    action_type = st.selectbox(
        "What would you like to do next?",
        action_options,
        key="finder_action_type",
    )
    if action_type == "Read a resource":
        choices = suggestions["name"].tolist()
    elif action_type == "Review a device setting":
        choices = suggestions[suggestions["id"].isin(DEVICE_SETTING_IDS)]["name"].tolist()
    elif action_type == "Follow a setup guide":
        choices = [GUIDES[guide_id]["title"] for guide_id in mapping["guides"]]
    else:
        choices = [str(TOPICS[GOAL_TOPICS[goal]]["title"])]

    if not choices:
        st.info("There is no directly mapped setup guide for this goal yet. Choose “Read a resource” to continue with a relevant source.")
        st.selectbox("Choose an action that is available", ["Read a resource"], key="finder_action_fallback")
        action_type = "Read a resource"
        choices = suggestions["name"].tolist()
    if "finder_target" not in st.session_state or st.session_state["finder_target"] not in choices:
        st.session_state["finder_target"] = choices[0]
    target = st.selectbox("Choose an item", choices, key="finder_target")

    st.markdown("## Step 4 · Your short action checklist")
    target_key = "".join(character.lower() if character.isalnum() else "_" for character in target).strip("_")
    action_key = f"finder_step_{GOAL_TOPICS[goal]}_{action_type.replace(' ', '_').lower()}_{target_key}"
    checklist = [
        "Open the selected resource, guide, or topic.",
        "Check whether its device, cost, permissions, and limitations fit my situation.",
        "Choose one small next step, or decide that another option fits better.",
    ]
    for index, item in enumerate(checklist):
        st.checkbox(item, key=f"{action_key}_{index}")
    completed = sum(bool(st.session_state.get(f"{action_key}_{index}")) for index in range(len(checklist)))
    st.progress(completed / len(checklist), text=f"{completed} of {len(checklist)} steps checked")

    selected_resource = suggestions[suggestions["name"] == target]
    if action_type in ("Read a resource", "Review a device setting") and not selected_resource.empty:
        row = selected_resource.iloc[0]
        action_col, why_col = st.columns([1, 2], vertical_alignment="center")
        with action_col:
            if st.button("Open selected resource", key="finder_open_resource", width="stretch"):
                st.session_state["selected_resource_id"] = row["id"]
                st.switch_page("app_pages/resource_detail.py")
        with why_col:
            st.caption(f"This option appears because it is included in the fixed mapping for “{goal}”. Check current official information before installing or relying on it.")
    elif action_type == "Follow a setup guide":
        selected_guide_id = next((guide_id for guide_id in mapping["guides"] if GUIDES[guide_id]["title"] == target), None)
        if selected_guide_id:
            if st.button("Open selected guide", key="finder_open_guide"):
                st.session_state["selected_guide_id"] = selected_guide_id
                st.switch_page("app_pages/guide_detail.py")
    else:
        topic_id = GOAL_TOPICS[goal]
        if st.button("Explore selected topic", key="finder_open_topic"):
            st.session_state["selected_topic_id"] = topic_id
            st.switch_page("app_pages/topic_detail.py")

    st.markdown("## Step 5 · Reflect on your next step")
    if completed == len(checklist):
        st.success("You completed this checklist in DigitalWell. That records your progress in this session only; it does not change a device setting.", icon=":material/task_alt:")
    reflection = st.selectbox("Which statement fits your next step?", ["I found a step I can try", "I want to compare another option", "I need to check more information first", "I will come back to this later"], key=f"{action_key}_reflection")
    st.caption(f"Your reflection: {reflection}. No score is calculated.")
    st.button("Reset this action plan", on_click=reset_plan)
