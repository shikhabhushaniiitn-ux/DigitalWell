
import streamlit as st

st.set_page_config(
    page_title="DigitalWell | Student Resource Hub",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 DigitalWell")
st.subheader("A Student's Guide to Healthy Digital Habits")

st.write(
    "Discover practical tools and resources to build "
    "healthier digital habits."
)

st.info(
    "Welcome to DigitalWell! Our resource hub is currently "
    "under development."
)

st.markdown("### Explore Digital Wellness")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎯 Focus & Productivity")
    st.write("Discover tools to reduce study distractions.")

with col2:
    st.subheader("📱 Screen Time")
    st.write("Explore screen-time management resources.")

with col3:
    st.subheader("🌙 Sleep & Wellbeing")
    st.write("Learn about healthier bedtime routines.")

st.caption("DigitalWell | Educational resource project")
