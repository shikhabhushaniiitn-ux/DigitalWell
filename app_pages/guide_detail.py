"""Render existing Markdown guides with session-only interactive progress."""

import re
from pathlib import Path

import streamlit as st

from src.components import GUIDE_DIR, image, page_header, reference_screenshot
from src.content import GUIDES

STEP_ILLUSTRATIONS_DIR = Path(__file__).resolve().parents[1] / "assets" / "images" / "guide_steps"

guide_id = st.session_state.get("selected_guide_id")
guide = GUIDES.get(guide_id)

if guide is None:
    st.info("Choose a guide from the Setup Guides page to read its instructions.")
    st.page_link("app_pages/setup_guides.py", label="Back to Setup Guides", icon=":material/arrow_back:")
else:
    page_header(str(guide["title"]), str(guide["summary"]), ":material/menu_book:")
    st.page_link("app_pages/setup_guides.py", label="All setup guides", icon=":material/arrow_back:")
    image(str(guide.get("photo", guide["image"])), str(guide["alt"]), "Context photo only; not an actual device-settings screenshot.")
    st.info("This checklist tracks your reading progress in the current session only. It does not change Android or browser settings.", icon=":material/checklist:")

    markdown = (GUIDE_DIR / str(guide["filename"])).read_text(encoding="utf-8")
    sections: list[tuple[str, list[str]]] = []
    title = "Guide"
    body: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("## "):
            if body or sections:
                sections.append((title, body))
            title, body = line[3:].strip(), []
        else:
            body.append(line)
    if body:
        sections.append((title, body))

    steps: list[str] = []
    step_keys: list[str] = []
    for section_title, lines in sections:
        if section_title.casefold() == "steps":
            st.markdown("## Steps")
            for line in lines:
                match = re.match(r"\s*\d+\.\s+(.*)", line)
                if match:
                    steps.append(match.group(1).strip())
            step_keys = [f"guide_progress_{guide_id}_{index}" for index in range(len(steps))]
            for index, (key, step) in enumerate(zip(step_keys, steps), start=1):
                with st.container(border=True):
                    text_column, image_column = st.columns([1.35, 1], vertical_alignment="center")
                    with text_column:
                        st.checkbox(f"{index}. {step}", key=key)
                    with image_column:
                        illustration = STEP_ILLUSTRATIONS_DIR / f"{guide_id}_step_{index}.svg"
                        if illustration.is_file():
                            st.image(
                                str(illustration),
                                width="stretch",
                                alt=f"Illustration for step {index}: {step}",
                                caption="Illustrative screen; menus may vary by device or version.",
                            )
            done = sum(bool(st.session_state.get(key, False)) for key in step_keys)
            if step_keys:
                st.progress(done / len(step_keys), text=f"{done} of {len(step_keys)} guide steps checked")
        else:
            text = "\n".join(lines).strip()
            placeholder = None
            clean_lines = []
            for line in lines:
                if "Screenshot placeholder:" in line:
                    placeholder = line.lstrip("> ").strip()
                else:
                    clean_lines.append(line)
            text = "\n".join(clean_lines).strip()
            if text:
                st.markdown(f"## {section_title}")
                st.markdown(text)
            if placeholder:
                st.info("Genuine screenshot placeholder: add a real capture from your own device or browser, with personal information hidden. The existing photo is illustrative and is not a settings screenshot.", icon=":material/photo_camera:")

    if guide_id == "android-timer":
        st.markdown("## Official Android interface references")
        reference_screenshot(
            "google_play_app_timer_expired.png",
            "Google Digital Wellbeing promotional screenshot showing an app paused after its timer runs out.",
            "This Google Play image shows the app-paused result after a timer expires; it is not a capture of the timer setup screen.",
            "https://play.google.com/store/apps/details?id=com.google.android.apps.wellbeing",
            "Open Google Play source",
        )
        st.link_button("Google Android Help: set an app timer", "https://support.google.com/android/answer/9346420")
        with st.expander("Related reference: Android Focus mode"):
            reference_screenshot(
                "google_play_focus_mode.png",
                "Google Digital Wellbeing promotional screenshot showing Focus mode with selected distracting apps.",
                "Focus mode is a related Android option for pausing selected apps. It is separate from the daily app timer steps in this guide.",
                "https://play.google.com/store/apps/details?id=com.google.android.apps.wellbeing",
                "Open Google Play source",
            )
            st.link_button("Google Android Help: Digital Wellbeing and Focus mode", "https://support.google.com/android/answer/9346420")
    elif guide_id == "bedtime":
        st.markdown("## Official Android interface reference")
        reference_screenshot(
            "google_play_bedtime_mode.png",
            "Google Digital Wellbeing promotional screenshot showing a scheduled Bedtime mode routine.",
            "This product reference shows a Bedtime mode schedule. Options and labels can differ across Android versions and devices.",
            "https://play.google.com/store/apps/details?id=com.google.android.apps.wellbeing",
            "Open Google Play source",
        )
        st.link_button("Google Android Help: Bedtime mode setup", "https://support.google.com/android/answer/9346420")
    elif guide_id == "leechblock":
        st.markdown("## Official setup references")
        st.info("No LeechBlock settings screenshot is embedded: the official site’s interface examples do not state a screenshot reuse license. Use the official links below, and keep the genuine browser screenshot placeholder for your own capture.", icon=":material/link:")
        link_columns = st.columns(2)
        with link_columns[0]:
            st.link_button("LeechBlock NG Quick Start", "https://www.proginosko.com/leechblock/documentation/", width="stretch")
            st.link_button("LeechBlock NG on Firefox Add-ons", "https://addons.mozilla.org/en-US/firefox/addon/leechblock-ng/", width="stretch")
        with link_columns[1]:
            st.link_button("LeechBlock permissions FAQ", "https://www.proginosko.com/leechblock/faq/permissions/", width="stretch")
            st.link_button("Chrome Help: manage extensions", "https://support.google.com/chrome/answer/2664769", width="stretch")

    st.markdown("## My setup reflection")
    if step_keys and all(bool(st.session_state.get(key, False)) for key in step_keys):
        st.success("You checked every step in this guide. DigitalWell has not changed any setting on your device.", icon=":material/task_alt:")
    st.selectbox("What best describes your next step?", ["I followed the steps", "My menus looked different", "I need to check an official help page", "I will finish this later"], key=f"guide_reflection_{guide_id}")
    st.caption("If your menu names differ, use Settings search or the linked official support documentation. Keep essential contacts, coursework, and alarms reachable.")

    def reset_progress() -> None:
        for key in step_keys:
            st.session_state[key] = False

    st.button("Reset guide progress", on_click=reset_progress)
