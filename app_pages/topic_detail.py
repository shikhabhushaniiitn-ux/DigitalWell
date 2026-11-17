import streamlit as st

from src.components import get_resources, image, page_header, resource_card
from src.content import GUIDES, TOPICS

topic_id = st.session_state.get("selected_topic_id")
topic = TOPICS.get(topic_id)

if topic is None:
    st.info("Choose a topic from the Digital Wellness Topics page to see its detail pathway.")
    st.page_link("app_pages/topics.py", label="Back to Digital Wellness Topics", icon=":material/arrow_back:")
else:
    page_header(str(topic["title"]), str(topic["summary"]), ":material/spa:")
    st.page_link("app_pages/topics.py", label="All wellness topics", icon=":material/arrow_back:")
    visual, overview = st.columns([0.8, 1.2], vertical_alignment="center")
    with visual:
        image(str(topic.get("photo", topic["image"])), str(topic["alt"]))
    with overview:
        st.markdown("### Common student challenges")
        for challenge in topic["challenges"]:
            st.markdown(f"- {challenge}")
        st.markdown("### Practical habits to try")
        for habit in topic["habits"]:
            st.markdown(f"- {habit}")

    if topic_id == "sleep":
        sleep_visual, sleep_note = st.columns([0.8, 1.2], vertical_alignment="center")
        with sleep_visual:
            image("photos/topic_sleep_phone.jpg", "A smartphone is being used in bed, illustrating a common late-night screen habit.")
        with sleep_note:
            st.markdown("### When a phone follows you to bed")
            st.write("Treat this as an example of a common challenge, not a recommended routine. Try charging the phone on a nearby table and keeping essential alarms or contacts available.")

    resources = get_resources()
    related = resources[resources["id"].isin(topic["resources"])]
    st.markdown("### Related resources")
    columns = st.columns(2)
    for column, (_, row) in zip(columns * 2, related.iterrows()):
        with column:
            resource_card(row, compact=True)

    if topic["guides"]:
        st.markdown("### Relevant setup guides")
        guide_columns = st.columns(min(2, len(topic["guides"])))
        for column, guide_id in zip(guide_columns, topic["guides"]):
            guide = GUIDES[guide_id]
            with column:
                with st.container(border=True):
                    st.subheader(str(guide["title"]))
                    st.write(str(guide["summary"]))
                    if st.button("Open this guide", key=f"topic_guide_{guide_id}"):
                        st.session_state["selected_guide_id"] = guide_id
                        st.switch_page("app_pages/guide_detail.py")
