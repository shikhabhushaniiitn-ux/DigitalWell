import streamlit as st

from src.components import clean_value, get_resources, page_header, reference_screenshot, resource_card, resource_detail_block
from src.content import RESOURCE_RELATED

resources = get_resources()
resource_id = st.session_state.get("selected_resource_id")
match = resources[resources["id"] == resource_id]

if match.empty:
    st.info("Choose a resource from the library to view its details.")
    st.page_link("app_pages/explore_resources.py", label="Back to Explore Resources", icon=":material/arrow_back:")
else:
    row = match.iloc[0]
    page_header(clean_value(row["name"]), clean_value(row["description"]), ":material/article:")
    st.page_link("app_pages/explore_resources.py", label="Explore Resources", icon=":material/arrow_back:")
    with st.container(border=True):
        st.markdown(f"**Category**  \n{clean_value(row['category'])}")
        resource_detail_block(row)
        st.caption(f"Source reviewed {clean_value(row['verified_on'])}")
        source = clean_value(row["source_reference"])
        if source.startswith(("https://", "http://")):
            st.link_button("Open reviewed source", source)
        if bool(row["url_valid"]):
            st.link_button(f"Visit {clean_value(row['name'])} official website", clean_value(row["official_url"]))
    if resource_id == "google-dw":
        with st.expander("Official product reference: Digital Wellbeing overview"):
            reference_screenshot(
                "google_play_digital_wellbeing_dashboard.png",
                "Google Digital Wellbeing promotional screenshot showing its dashboard with usage and routine options.",
                "An official product overview from Google Play. It is illustrative reference material, not a screenshot of this student's device or evidence of testing.",
                "https://play.google.com/store/apps/details?id=com.google.android.apps.wellbeing",
                "Open Google Play source",
            )
    st.markdown("## Before you use it")
    st.caption("This checklist helps you review a resource; it does not certify that a product is safe or suitable.")
    checklist = [
        "Is this resource compatible with my device and account?",
        "Have I checked its current cost and payment conditions?",
        "Have I reviewed the permissions it requests?",
        "Have I read the provider's privacy information?",
        "Have I checked its accessibility and limitations?",
        "Is this tool appropriate for my actual requirements?",
    ]
    state_keys = [f"resource_review_{resource_id}_{index}" for index in range(len(checklist))]
    for key in state_keys:
        st.session_state.setdefault(key, False)
    def reset_review() -> None:
        for key in state_keys:
            st.session_state[key] = False
    for key, question in zip(state_keys, checklist):
        st.checkbox(question, key=key)
    checked = sum(bool(st.session_state[key]) for key in state_keys)
    st.progress(checked / len(checklist), text=f"{checked} of {len(checklist)} checks reviewed")
    st.button("Reset this checklist", on_click=reset_review)
    st.caption("Your progress is kept only in this Streamlit session. Confirm details with the provider before installing or relying on a tool.")
    st.markdown("### Related resources")
    related_ids = RESOURCE_RELATED.get(resource_id, [])
    related = resources[resources["id"].isin(related_ids)]
    columns = st.columns(min(2, max(1, len(related))))
    for column, (_, related_row) in zip(columns, related.iterrows()):
        with column:
            resource_card(related_row, compact=True)
