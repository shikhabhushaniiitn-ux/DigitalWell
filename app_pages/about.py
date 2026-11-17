import streamlit as st

from src.components import image

st.title("About DigitalWell", icon=":material/info:")
st.caption("A student-built educational resource hub for everyday digital wellness choices.")

about_intro, about_visual = st.columns([1.1, 0.9], vertical_alignment="center")
with about_intro:
    st.markdown("### Practical guidance, organized around student needs")
    st.write("DigitalWell brings together tools, habits, and source links so students can explore options at their own pace.")
with about_visual:
    image("photos/about_student_collaboration.jpg", "Students collaborate around a laptop in a classroom, representing shared learning.")

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader("Purpose and audience")
        st.write("DigitalWell helps students discover, compare, and use resources related to attention, screen habits, sleep routines, privacy, and online safety.")
        st.subheader("What it offers")
        st.write("A sourced nine-resource catalogue, advanced comparisons, four topic pathways, three interactive setup guides, a session-only daily planner, and a transparent goal-based action finder.")
with right:
    with st.container(border=True):
        st.subheader("Technology and architecture")
        st.write("Python, Streamlit 1.67, Pandas, a CSV catalogue, `st.navigation` multipage routing, shared rendering helpers, and local SVG/photo assets.")
        st.subheader("Selection approach")
        st.write("Resources are chosen for relevance to student needs. Entries link to official provider or project pages; unknown costs, privacy details, accessibility, or compatibility remain qualified.")

st.markdown("## Scope and responsible use")
st.write("DigitalWell is educational information, not a medical service, diagnostic tool, legal adviser, or incident-response service. It does not create accounts or use AI recommendations. Source review is not a security audit or endorsement. Product details, prices, availability, and interfaces may change; confirm current information with the provider.")
st.markdown("## What remains to be completed")
st.write("Genuine Android and browser screenshots, a manual visual and keyboard review across viewport sizes, student usability feedback, and a fresh functional review of the new interactive features remain part of the next project milestone.")
