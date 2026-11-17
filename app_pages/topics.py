import streamlit as st

from src.components import topic_card
from src.content import TOPICS

st.title("Digital Wellness Topics", icon=":material/spa:")
st.caption("Explore practical, student-focused pathways. Each topic opens its own detail page with habits, resources, and guides.")

columns = st.columns(2)
for column, (topic_id, topic) in zip(columns * 2, TOPICS.items()):
    with column:
        topic_card(topic_id, topic)

st.info("These suggestions are educational starting points, not clinical advice. Choose the steps that fit your situation.", icon=":material/info:")
