import streamlit as st

from src.components import get_resources, image, resource_card
from src.content import TOPICS
from src.utils.data_loader import filter_resources

resources = get_resources()
st.title("Explore resources", icon=":material/search:")
st.caption("Search a small, source-linked library of digital wellness tools and learning resources.")

st.markdown("### Browse by what you need")
feature_topics = [
    ("focus", "photos/resource_focus.jpg", "A student working quietly in a library."),
    ("screen-time", "photos/guide_app_timer.jpg", "A person checking a smartphone outdoors."),
    ("privacy", "photos/privacy_secure_laptop.jpg", "Hands using a laptop in a focused workspace."),
]
feature_columns = st.columns(3)
for column, (topic_id, filename, alt) in zip(feature_columns, feature_topics):
    with column:
        with st.container(border=True):
            image(filename, alt)
            st.subheader(str(TOPICS[topic_id]["title"]))
            st.write(str(TOPICS[topic_id]["summary"]))
            if st.button("Explore this topic", key=f"resource_topic_{topic_id}", width="stretch"):
                st.session_state["selected_topic_id"] = topic_id
                st.switch_page("app_pages/topic_detail.py")

if "resource_search" not in st.session_state:
    st.session_state["resource_search"] = ""
if "resource_category" not in st.session_state:
    st.session_state["resource_category"] = "All categories"
if "resource_platform" not in st.session_state:
    st.session_state["resource_platform"] = "All platforms"

categories = ["All categories"] + sorted(resources["category"].dropna().unique().tolist())
platforms = sorted({p.strip() for cell in resources["platforms"] for p in str(cell).split(",") if p.strip()})

def reset_search():
    st.session_state["resource_search"] = ""
    st.session_state["resource_category"] = "All categories"
    st.session_state["resource_platform"] = "All platforms"

with st.container(border=True):
    st.markdown("### Find a useful starting point")
    controls = st.columns([2, 1, 1, 0.75], vertical_alignment="bottom")
    with controls[0]:
        st.text_input("Search by name, need, or description", key="resource_search", placeholder="For example: focus, Android, privacy")
    with controls[1]:
        st.selectbox("Category", categories, key="resource_category")
    with controls[2]:
        st.selectbox("Platform", ["All platforms"] + platforms, key="resource_platform")
    with controls[3]:
        st.button("Reset", on_click=reset_search, width="stretch")

category = st.session_state["resource_category"]
platform = st.session_state["resource_platform"]
filtered = filter_resources(
    resources,
    query=st.session_state["resource_search"],
    category="All" if category == "All categories" else category,
    platform="All" if platform == "All platforms" else platform,
)
st.caption(f"{len(filtered)} of {len(resources)} resources")
if filtered.empty:
    st.info("No resources match those filters. Try a broader search or reset the filters.", icon=":material/search_off:")
else:
    for start in range(0, len(filtered), 2):
        columns = st.columns(2)
        for column, (_, row) in zip(columns, filtered.iloc[start : start + 2].iterrows()):
            with column:
                resource_card(row)

st.page_link("app_pages/compare_tools.py", label="Compare selected options", icon=":material/compare_arrows:")
