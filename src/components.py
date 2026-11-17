"""Reusable Streamlit components shared by the multipage portal."""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.utils.data_loader import load_resources

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "assets" / "images"
GUIDE_DIR = ROOT / "guides"
NOT_STATED = "Not stated in the reviewed source"


@st.cache_data(show_spinner=False)
def get_resources() -> pd.DataFrame:
    return load_resources(ROOT / "data" / "resources" / "resources.csv")


def clean_value(value: object) -> str:
    if value is None or pd.isna(value) or not str(value).strip():
        return NOT_STATED
    return str(value).strip()


def contains_unknown(value: object) -> bool:
    text = clean_value(value).casefold()
    return any(term in text for term in ("not verified", "not stated", "not confirmed"))


def page_header(title: str, description: str, icon: str) -> None:
    st.title(title, icon=icon)
    st.caption(description)


def image(name: str, alt: str, caption: str | None = None) -> None:
    path = IMAGE_DIR / name
    if path.is_file():
        st.image(str(path), width="stretch", alt=alt, caption=caption)
    else:
        st.caption(f"Image unavailable: {alt}")


def reference_screenshot(name: str, alt: str, detail: str, source_url: str, source_label: str) -> None:
    """Show an attributed, locally stored product reference without implying testing."""
    path = IMAGE_DIR / "reference_screenshots" / name
    if not path.is_file():
        st.warning(f"Reference screenshot unavailable: {name}")
        return
    with st.container(border=True):
        image_column, detail_column = st.columns([1, 1.45], vertical_alignment="center")
        with image_column:
            st.image(str(path), width=288, alt=alt)
        with detail_column:
            st.caption("Official Google product reference screenshot — interface may vary by device or version.")
            st.write(detail)
            st.link_button(source_label, source_url, width="stretch")


def switch(page: str) -> None:
    st.switch_page(f"app_pages/{page}.py")


def open_resource(resource_id: str) -> None:
    st.session_state["selected_resource_id"] = resource_id
    switch("resource_detail")


def resource_card(row: pd.Series, compact: bool = False, thumbnail: str | None = None) -> None:
    name = clean_value(row["name"])
    resource_id = clean_value(row["id"])
    with st.container(border=True):
        if thumbnail:
            image(thumbnail, f"Photograph representing the {clean_value(row['category']).lower()} resource category.")
        st.subheader(name)
        st.caption(f"{clean_value(row['category'])} · {clean_value(row['problem'])}")
        st.write(clean_value(row["description"]))
        if not compact:
            left, right = st.columns(2)
            with left:
                st.markdown(f"**Platforms**  \n{clean_value(row['platforms'])}")
                st.markdown(f"**Cost**  \n{clean_value(row['cost'])}")
            with right:
                st.markdown(f"**Privacy**  \n{clean_value(row['privacy'])}")
                st.markdown(f"**Limitations**  \n{clean_value(row['limitations'])}")
        st.caption(f"Source reviewed {clean_value(row['verified_on'])}")
        actions = st.columns(2)
        with actions[0]:
            if st.button("View details", key=f"details_{resource_id}", width="stretch"):
                open_resource(resource_id)
        with actions[1]:
            if bool(row["url_valid"]):
                st.link_button("Official website", clean_value(row["official_url"]), width="stretch")
            else:
                st.warning("Official link needs review")


def guide_card(guide_id: str, guide: dict[str, object]) -> None:
    with st.container(border=True):
        image(str(guide.get("photo", guide["image"])), str(guide["alt"]))
        st.subheader(str(guide["title"]))
        st.write(str(guide["summary"]))
        st.caption("The photograph provides context; it is not a real device screenshot.")
        if st.button("Open guide", key=f"open_guide_{guide_id}", width="stretch"):
            st.session_state["selected_guide_id"] = guide_id
            switch("guide_detail")


def topic_card(topic_id: str, topic: dict[str, object]) -> None:
    with st.container(border=True):
        image(str(topic.get("photo", topic["image"])), str(topic["alt"]))
        st.subheader(str(topic["title"]))
        st.write(str(topic["summary"]))
        if st.button("Explore topic", key=f"topic_{topic_id}", width="stretch"):
            st.session_state["selected_topic_id"] = topic_id
            switch("topic_detail")


def resource_rows(resource_ids: list[str]) -> pd.DataFrame:
    frame = get_resources()
    return frame[frame["id"].isin(resource_ids)].set_index("id").reindex(resource_ids).dropna(subset=["name"]).reset_index()


def resource_detail_block(row: pd.Series) -> None:
    st.markdown(f"**Purpose**  \n{clean_value(row['problem'])}")
    st.markdown(f"**Supported platforms**  \n{clean_value(row['platforms'])}")
    st.markdown(f"**Cost**  \n{clean_value(row['cost'])}")
    st.markdown(f"**Privacy considerations**  \n{clean_value(row['privacy'])}")
    st.markdown(f"**Accessibility**  \n{clean_value(row['accessibility'])}")
    st.markdown(f"**Advantages**  \n{clean_value(row['advantages'])}")
    st.markdown(f"**Limitations**  \n{clean_value(row['limitations'])}")


def footer() -> None:
    st.divider()
    st.caption("DigitalWell · Student Digital Wellness Resource Hub · Educational information, not medical advice")
