"""DigitalWell multipage student digital wellness portal."""

import streamlit as st

from src.components import footer

st.set_page_config(
    page_title="DigitalWell | Student Digital Wellness Hub",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.html("""<style>
.stImage img { border-radius: 1rem; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 1rem; }
@media (max-width: 700px) {
  h1 { font-size: 2rem !important; }
  h2 { font-size: 1.55rem !important; }
}
</style>""")

brand, strapline = st.columns([1, 2], vertical_alignment="center")
with brand:
    st.markdown("### 🌿 DigitalWell")
with strapline:
    st.caption("Student Digital Wellness Resource Hub · Discover · Compare · Take action")

main_pages = [
    st.Page("app_pages/home.py", title="Home", icon=":material/home:", default=True, help="Start here for featured resources, topic areas, and a guided way to choose a next step."),
    st.Page("app_pages/explore_resources.py", title="Explore Resources", icon=":material/search:", help="Search and filter the sourced resource library, then open a focused resource detail view."),
    st.Page("app_pages/compare_tools.py", title="Compare Tools", icon=":material/compare_arrows:", help="Compare two to four resources across platform, cost, privacy, accessibility, and limitations."),
    st.Page("app_pages/topics.py", title="Digital Wellness Topics", icon=":material/spa:", help="Explore pathways for focus, screen habits, sleep, and online privacy."),
]
learn_pages = [
    st.Page("app_pages/setup_guides.py", title="Setup Guides", icon=":material/menu_book:", help="Choose a setup guide with preparation, steps, troubleshooting, and official references."),
    st.Page("app_pages/resource_finder.py", title="Resource Finder", icon=":material/lightbulb:", help="Choose a goal to see transparent, rule-based resource and guide suggestions."),
    st.Page("app_pages/daily_routine_planner.py", title="Daily Routine Planner", icon=":material/calendar_month:", help="Draft a flexible study-day schedule using session-only time inputs."),
]
about_pages = [
    st.Page("app_pages/privacy_safety.py", title="Privacy & Online Safety", icon=":material/security:", help="Review student checklists and trusted privacy and safety resources."),
    st.Page("app_pages/about.py", title="About DigitalWell", icon=":material/info:", help="Learn about DigitalWell's purpose, methods, limitations, and responsible-use principles."),
]
detail_pages = [
    st.Page("app_pages/resource_detail.py", title="Resource details", url_path="resource-detail", visibility="hidden", icon=":material/article:"),
    st.Page("app_pages/topic_detail.py", title="Topic details", url_path="topic-detail", visibility="hidden", icon=":material/article:"),
    st.Page("app_pages/guide_detail.py", title="Guide details", url_path="guide-detail", visibility="hidden", icon=":material/article:"),
]

page = st.navigation(
    {"": main_pages, "Learn & act": learn_pages, "About": about_pages, "Details": detail_pages},
    position="top",
)
page.run()
footer()
