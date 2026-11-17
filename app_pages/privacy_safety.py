import streamlit as st

from src.components import get_resources, guide_card, image, resource_card
from src.content import GUIDES

resources = get_resources()
st.title("Privacy & Online Safety", icon=":material/security:")
st.caption("Everyday steps for protecting personal information, accounts, and devices while learning and socializing online.")

visual, intro = st.columns([0.9, 1.1], vertical_alignment="center")
with visual:
    image("photos/privacy_secure_laptop.jpg", "Hands using a laptop in a quiet workspace, representing careful device use.")
with intro:
    st.markdown("### A few careful checks go a long way")
    st.write("Review what a service asks to access, what information it says it uses, and where to get help if something feels unsafe.")

guidance = [
    ("Personal information and digital identity", "Share only what is needed. Review profile visibility, tagged content, and account recovery details from time to time."),
    ("App permissions", "Check whether access to location, contacts, microphone, files, or browsing data is needed for the feature. Optional permissions can often be changed later."),
    ("Passwords and account security", "Use a unique password for each important account. Enable multi-factor authentication when available, and protect recovery methods."),
    ("Tracking and browser privacy", "Built-in tracking protections can reduce some tracking, but cannot make browsing anonymous or block every method. Some privacy settings may affect site features."),
    ("Safe app and extension installation", "Prefer official stores or provider websites. Check the developer, requested permissions, recent updates, and current privacy information."),
    ("Responsible online communication", "Pause before forwarding urgent claims or sharing someone else's private information. Use respectful language and report harmful content through trusted channels."),
]
for title, details in guidance:
    with st.container(border=True):
        st.subheader(title)
        st.write(details)

st.markdown("## Optional privacy and notification self-audit")
st.caption("Use this private, session-only checklist to decide what you may want to review. It does not test or certify that an account or device is secure.")
audit_items = [
    ("permissions", "Have I reviewed unnecessary app or extension permissions?", "Review why each permission is requested before installing or continuing to use a tool."),
    ("unique_passwords", "Do I use unique passwords for important accounts?", "Consider a unique password for each important account and review account recovery options."),
    ("mfa", "Have I enabled multi-factor authentication where available?", "Check the account's official security settings and keep recovery methods current."),
    ("notifications", "Have I checked which apps send frequent notifications?", "Review notification settings and keep essential contacts and services reachable."),
    ("tracking", "Have I reviewed my browser's tracking protection?", "Read the browser's current help page and check whether stronger settings affect sites you rely on."),
    ("reporting", "Do I know how to report suspicious messages?", "Use the service's reporting controls or ask a trusted person or institution for help."),
    ("privacy_settings", "Have I reviewed my account privacy settings?", "Check profile visibility, data sharing, and account recovery settings with the provider."),
]
audit_keys = [f"privacy_audit_{item[0]}" for item in audit_items]
audit_resource_map = {
    "permissions": ["leechblock", "privacy-badger"],
    "unique_passwords": ["eff-ssd", "isoc-safety"],
    "mfa": ["eff-ssd", "isoc-safety"],
    "notifications": ["google-dw"],
    "tracking": ["firefox-etp", "privacy-badger"],
    "reporting": ["isoc-safety", "eff-ssd"],
    "privacy_settings": ["eff-ssd", "isoc-safety"],
}
audit_guide_map = {
    "permissions": ["leechblock"],
    "notifications": ["android-timer", "bedtime"],
}
for key in audit_keys:
    st.session_state.setdefault(key, False)
for (slug, question, _), key in zip(audit_items, audit_keys):
    st.checkbox(question, key=key)
completed_audit = [item for item, key in zip(audit_items, audit_keys) if st.session_state[key]]
review_audit = [item for item, key in zip(audit_items, audit_keys) if not st.session_state[key]]
st.progress(len(completed_audit) / len(audit_items), text=f"{len(completed_audit)} of {len(audit_items)} checks reviewed")

def reset_audit() -> None:
    for key in audit_keys:
        st.session_state[key] = False

st.button("Reset self-audit", on_click=reset_audit)
done_col, next_col = st.columns(2)
with done_col:
    st.markdown("### Checks you reviewed")
    if completed_audit:
        for _, question, _ in completed_audit:
            st.markdown(f"- {question}")
    else:
        st.caption("No checks selected yet. You can use the list as a prompt and skip any item.")
with next_col:
    st.markdown("### Items you may want to review")
    if review_audit:
        for _, question, next_step in review_audit:
            st.markdown(f"- **{question}** {next_step}")
    else:
        st.success("You reviewed every item in this checklist. This does not certify that an account or device is secure.")
st.caption("Selections are kept only in this session. DigitalWell does not collect these answers or assign a security score.")

st.markdown("## Related resources and setup guides")
st.write("Suggestions below connect the items you may want to review with existing DigitalWell resources. They are learning links, not a security assessment.")
related_ids = list(dict.fromkeys(resource_id for slug, _, _ in review_audit for resource_id in audit_resource_map.get(slug, [])))
if not related_ids:
    related_ids = ["eff-ssd", "isoc-safety"]
related_resources = resources[resources["id"].isin(related_ids)]
for start in range(0, len(related_resources), 2):
    resource_columns = st.columns(2)
    for column, (_, resource_row) in zip(resource_columns, related_resources.iloc[start : start + 2].iterrows()):
        with column:
            resource_card(resource_row, compact=True)

related_guide_ids = list(dict.fromkeys(guide_id for slug, _, _ in review_audit for guide_id in audit_guide_map.get(slug, [])))
if related_guide_ids:
    st.markdown("### Guides related to your review items")
    guide_columns = st.columns(min(2, len(related_guide_ids)))
    for column, guide_id in zip(guide_columns, related_guide_ids):
        with column:
            guide_card(guide_id, GUIDES[guide_id])

st.markdown("## Privacy in shared spaces")
privacy_visual, privacy_copy = st.columns([0.75, 1.25], vertical_alignment="center")
with privacy_visual:
    image("photos/guide_app_timer.jpg", "A person checks a smartphone while outdoors; keep private screen content shielded in shared spaces.")
with privacy_copy:
    st.markdown("### Think about where you use a device")
    st.write("When studying in a shared place, angle your screen away from passers-by and avoid opening personal information where others can easily see it. A photo here shows ordinary phone use, not a security setting.")
st.write("For broader privacy and online safety learning, use the related resources selected above or browse the complete catalogue.")
st.page_link("app_pages/explore_resources.py", label="Explore all resources", icon=":material/search:")

st.warning("If a device or account may be monitored, changing settings can sometimes be visible to the person monitoring it. Consider using a trusted device and support channel. For immediate danger, contact local emergency or campus support services.", icon=":material/support:")
