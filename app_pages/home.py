import streamlit as st

from src.components import IMAGE_DIR, get_resources, image, page_header, resource_card, topic_card
from src.content import TOPICS

resources = get_resources()
hero_photo = IMAGE_DIR / "student-study-hero.jpg"
hero_copy, hero_visual = st.columns([1.08, 0.92], vertical_alignment="center")
with hero_copy:
    st.caption("A UNIVERSITY-STYLE STUDENT RESOURCE PORTAL")
    page_header("Build a healthier relationship with technology.", "Practical, source-based guidance for focus, screen habits, sleep, and online safety.", ":material/self_improvement:")
    st.write("DigitalWell helps you discover useful tools, compare their trade-offs, and take a small next step. Choose what fits your studies and daily life.")
    st.page_link("app_pages/explore_resources.py", label="Explore resources", icon=":material/search:", width="stretch")
    st.page_link("app_pages/topics.py", label="Discover digital wellness", icon=":material/spa:", width="stretch")
with hero_visual:
    if hero_photo.exists():
        st.image(str(hero_photo), width="stretch", alt="A student studying at a desk with a laptop, notebook, and writing tools in a calm setting.")
    else:
        image("digitalwell_hero.svg", "Original illustration of a student studying at a laptop with a notebook and plant nearby.")

st.markdown("## Build a Balanced Digital Study Day")
st.caption("Small, flexible ideas for balancing focused screen use with rest and offline time.")
day_cards = [
    ("Focused Study Sessions", "Choose one task and a realistic study block.", "Put your phone on Focus mode for one short block; keep essential contacts available.", "photos/resource_focus.jpg", "A student working quietly at a library table.", "focus", None),
    ("Short Study Breaks", "A pause can help you step away between tasks.", "Stand up, get water, or look away from the screen before starting the next block.", "photos/home_digital_balance.jpg", "A person planning an outdoor activity with a phone.", "screen-time", None),
    ("Movement and Stretching", "Add a little movement between long periods of sitting.", "Take a brief walk or stretch in a way that feels comfortable for you.", "photos/topic_focus.jpg", "A student studying at a library table.", "screen-time", None),
    ("Eye and Posture Comfort", "Notice whether your screen setup feels comfortable.", "Pause regularly, change position, and adjust your device to a comfortable viewing angle.", "photos/guide_app_timer.jpg", "A person holding a phone outdoors.", "screen-time", None),
    ("Meals and Offline Time", "Make room for meals and activities away from a screen.", "Try placing your device aside during one meal or planned offline activity.", "photos/home_digital_balance.jpg", "A person planning time outdoors.", "screen-time", None),
    ("Social Connection", "Leave space for conversations and time with other people.", "Choose a moment to connect without multitasking on a device, if that works for you.", "photos/about_student_collaboration.jpg", "Students collaborating around a laptop.", "screen-time", None),
    ("Bedtime and Wind-Down Routine", "Decide what device settings or habits suit your evening.", "Review bedtime notifications and keep important alarms and contacts reachable.", "photos/guide_bedtime.jpg", "A calm bedside lamp and bedroom.", "sleep", "bedtime"),
]
for start in range(0, len(day_cards), 3):
    columns = st.columns(3)
    for column, card in zip(columns, day_cards[start : start + 3]):
        title, summary, suggestion, photo, alt, topic_id, guide_id = card
        with column:
            with st.container(border=True):
                image(photo, alt)
                st.subheader(title)
                st.write(summary)
                st.caption(f"**Try:** {suggestion}")
                if st.button("Open related guidance", key=f"day_idea_{title}", width="stretch"):
                    if guide_id:
                        st.session_state["selected_guide_id"] = guide_id
                        st.switch_page("app_pages/guide_detail.py")
                    else:
                        st.session_state["selected_topic_id"] = topic_id
                        st.switch_page("app_pages/topic_detail.py")
st.caption("These are optional ideas, not health instructions or a routine everyone must follow.")
st.page_link("app_pages/daily_routine_planner.py", label="Draft a flexible study-day plan", icon=":material/calendar_month:")

st.markdown("## Explore a topic")
st.caption("Choose one area to see practical habits, related resources, and relevant setup guidance.")
topic_columns = st.columns(4)
for column, (topic_id, topic) in zip(topic_columns, TOPICS.items()):
    with column:
        topic_card(topic_id, topic)

st.markdown("## Featured resources")
st.caption("A few starting points from the nine-resource library. Open Explore Resources to search all entries.")
featured = resources[resources["id"].isin(["google-dw", "leechblock", "eff-ssd"])]
feature_columns = st.columns(3)
art_by_id = {"google-dw": "photos/home_digital_balance.jpg", "leechblock": "photos/resource_focus.jpg", "eff-ssd": "photos/privacy_secure_laptop.jpg"}
for column, (_, row) in zip(feature_columns, featured.iterrows()):
    with column:
        resource_card(row, compact=True, thumbnail=art_by_id.get(row["id"]))

st.markdown("## How DigitalWell works")
steps = st.columns(3)
for column, number, title, detail in zip(
    steps,
    ("01", "02", "03"),
    ("Discover", "Compare", "Take action"),
    ("Find resources by need and platform.", "Review real trade-offs and unknowns.", "Follow a guide and choose what suits you."),
):
    with column:
        with st.container(border=True):
            st.caption(number)
            st.subheader(title)
            st.write(detail)

st.info("DigitalWell is an educational resource hub, not a medical service or diagnostic tool. Resource details can change; check current official information before installing or relying on a tool.", icon=":material/info:")
st.page_link("app_pages/resource_finder.py", label="Not sure where to start? Use the guided resource finder", icon=":material/lightbulb:")
