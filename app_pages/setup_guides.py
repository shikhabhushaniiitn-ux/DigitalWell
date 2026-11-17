import streamlit as st

from src.components import guide_card
from src.content import GUIDES

st.title("Setup Guides", icon=":material/menu_book:")
st.caption("Choose one practical walkthrough. Menu names vary across device, browser, operating-system, and app versions.")

columns = st.columns(3)
for column, (guide_id, guide) in zip(columns, GUIDES.items()):
    with column:
        guide_card(guide_id, guide)

st.info("The local artwork is illustrative. Screenshot placeholders inside the guides are reserved for genuine device captures.", icon=":material/photo_camera:")
