"""Filter and compare sourced resources without ratings or automatic winners."""

import streamlit as st

from src.components import clean_value, contains_unknown, get_resources, image

resources = get_resources()
st.title("Compare tools", icon=":material/compare_arrows:")
intro, visual = st.columns([1.2, 0.8], vertical_alignment="center")
with intro:
    st.caption("Review differences side by side. DigitalWell does not score tools or choose a universal winner.")
    st.write("Use the filters to narrow the options, then compare source-backed details. Unknown information stays visible so you can decide what to check next.")
with visual:
    image("photos/compare_student_tools.jpg", "Two students reviewing a laptop together at a table.")

kind_by_id = {
    "google-dw": "Built-in Android feature",
    "apple-screen-time": "Built-in Apple feature",
    "stayfocusd": "Browser extension",
    "leechblock": "Browser extension",
    "freedom": "Cross-device app/service",
    "eff-ssd": "Online learning resource",
    "isoc-safety": "Online learning resource",
    "firefox-etp": "Built-in browser feature",
    "privacy-badger": "Browser extension",
}

filter_cols = st.columns(2)
with filter_cols[0]:
    category_filter = st.selectbox("Filter by resource category", ["All categories"] + sorted(resources["category"].unique().tolist()), key="compare_category")
with filter_cols[1]:
    platform_filter = st.selectbox("Filter by platform", ["All platforms", "Android", "Apple devices", "Browser", "Web resource"], key="compare_platform")

filtered = resources.copy()
if category_filter != "All categories":
    filtered = filtered[filtered["category"] == category_filter]
platform_terms = {
    "Android": ("android",),
    "Apple devices": ("apple", "iphone", "ipad", "mac"),
    "Browser": ("browser", "firefox", "chrome", "edge", "extension"),
    "Web resource": ("web resource", "browser-based", "web;", "web resource"),
}
if platform_filter != "All platforms":
    terms = platform_terms[platform_filter]
    filtered = filtered[filtered["platforms"].astype(str).str.casefold().apply(lambda value: any(term in value for term in terms))]

if "comparison_resources" not in st.session_state:
    st.session_state["comparison_resources"] = resources["name"].tolist()[:2]

def reset_comparison() -> None:
    st.session_state["comparison_resources"] = []

available_names = filtered["name"].tolist()
preserved_names = [name for name in st.session_state.get("comparison_resources", []) if name not in available_names]
options = available_names + preserved_names
st.caption("Category and platform filters narrow new choices. Resources you already selected remain selected until you remove them or reset the comparison.")
selection, reset = st.columns([4, 1], vertical_alignment="bottom")
with selection:
    selected = st.multiselect(
        "Choose two to four resources",
        options,
        max_selections=4,
        key="comparison_resources",
        help="The category and platform filters narrow new choices; existing selections remain selected.",
    )
with reset:
    st.button("Reset comparison", on_click=reset_comparison, width="stretch")

layout = st.segmented_control("Layout", ["Side by side", "Stacked"], default="Side by side", key="comparison_layout", help="Use stacked cards on a narrow screen.")
fields = [
    ("Purpose", "problem"),
    ("Platforms", "platforms"),
    ("Cost", "cost"),
    ("Privacy considerations", "privacy"),
    ("Accessibility", "accessibility"),
    ("Advantages", "advantages"),
    ("Limitations", "limitations"),
]

if len(selected) < 2:
    st.info("Select at least two resources above. Choose up to four, then compare the details that matter to you.", icon=":material/compare_arrows:")
else:
    chosen = resources.set_index("name").loc[selected]
    distinct_fields = []
    for label, field in fields:
        values = {clean_value(chosen.loc[name, field]) for name in selected}
        if len(values) > 1:
            distinct_fields.append(label)
    if distinct_fields:
        st.info("Differences appear in: " + ", ".join(distinct_fields) + ". Compare these details against your own device and needs.", icon=":material/difference:")
    else:
        st.caption("The selected resources share the same recorded values for the comparison fields.")

    def render_resource(name: str) -> None:
        row = chosen.loc[name]
        with st.container(border=True):
            st.subheader(name)
            st.caption(f"{clean_value(row['category'])} · {kind_by_id.get(str(row['id']), 'Resource type not classified')}")
            for label, field in fields:
                value = clean_value(row[field])
                is_different = len({clean_value(chosen.loc[item, field]) for item in selected}) > 1
                prefix = "**Different · " if is_different else "**"
                suffix = "**" if is_different else "**"
                if contains_unknown(value):
                    value = f"Unverified / not stated: {value}"
                st.markdown(f"{prefix}{label}{suffix}  \n{value}")

    if layout == "Stacked":
        for name in selected:
            render_resource(name)
    else:
        for start in range(0, len(selected), 2):
            columns = st.columns(2)
            for column, name in zip(columns, selected[start : start + 2]):
                with column:
                    render_resource(name)

    st.caption("Unverified / not stated means that detail was not established in the reviewed source. Confirm current information with the provider.")
    csv_data = chosen.reset_index()[["name", "id", "category", "problem", "platforms", "cost", "privacy", "accessibility", "advantages", "limitations", "source_reference", "verified_on"]].to_csv(index=False).encode("utf-8-sig")
    st.download_button("Download selected comparison (CSV)", data=csv_data, file_name="digitalwell_comparison.csv", mime="text/csv", icon=":material/download:")

    st.markdown("## What should I check before choosing?")
    st.write("Use these questions to decide what to verify for your own situation:")
    prompts = set()
    for name in selected:
        row = chosen.loc[name]
        cost_text = clean_value(row["cost"]).casefold()
        if contains_unknown(row["cost"]) or "not included" in cost_text or "exact price" in cost_text:
            prompts.add(f"Check current price, free-tier limits, renewal, and cancellation terms for {name}.")
        if contains_unknown(row["privacy"]) or "should be checked" in clean_value(row["privacy"]).casefold():
            prompts.add(f"Review {name}'s current privacy information and the permissions it requests.")
        if contains_unknown(row["accessibility"]):
            prompts.add(f"Check whether {name} supports the accessibility features you use.")
    prompts.add("Confirm that the listed platforms match your actual device, operating system, and account type.")
    prompts.add("Consider whether any limitation would interfere with coursework, support, or essential communication.")
    for prompt in sorted(prompts):
        st.markdown(f"- {prompt}")
