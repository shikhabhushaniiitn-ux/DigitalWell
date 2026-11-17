# DigitalWell — Student Digital Wellness Resource Hub

DigitalWell is a student-focused Streamlit portal for discovering and comparing digital wellness resources and learning simple setup steps. It covers focus, screen time, sleep, privacy and online safety through distinct pages and focused detail views. It provides educational information, not medical, clinical, cybersecurity incident-response or legal advice.

## Features

- Native `st.navigation` top navigation for Home, Explore Resources, Compare Tools, Digital Wellness Topics, Setup Guides, Resource Finder, Daily Routine Planner, Privacy & Online Safety, and About DigitalWell.
- A responsive balanced-study-day card section on Home linking practical ideas to existing topics, guides, and the planner.
- Session-only Daily Routine Planner that drafts a non-overlapping schedule for study blocks, breaks, meals, and wind-down time.
- Nine sourced resources with search, category/platform filters, focused detail views, and comparison for two to four tools.
- Advanced resource comparison with category/platform filters, resource-type labels, difference cues, decision prompts, and CSV download.
- Four topic pathways, each with student challenges, practical habits, related resources and relevant guides.
- A transparent fixed-rule resource finder with a guided action checklist and session-only reflection.
- Three interactive setup guides with session progress, troubleshooting, official references, and clearly labeled genuine screenshot placeholders.
- Unaltered, attributed Google Digital Wellbeing product-reference screenshots for app-timer outcome, Bedtime mode, Focus mode, and the resource overview.
- Per-resource pre-use checklist and optional privacy/notification self-audit, with no scores or security certification.
- Manually executed standard-library URL checker that writes a separate report and never changes the catalogue.
- Student privacy guidance, trusted learning resources, and clear educational disclaimers.
- Ten locally stored real photographs used across the portal, five original SVG illustrations, and descriptive alternative text.
- CSV schema checking, URL validation, duplicate-ID flags, and reusable Pandas loading/filtering.

## Technology

Python 3.13, Streamlit 1.67, Pandas and Pytest. Each contributor should create a local `.venv` from the project requirements; virtual environments are machine-specific and are not part of the repository. Sprint 6 adds no Python package dependencies; the standalone link checker uses the Python standard library.

## Project structure

```text
app.py                         Streamlit entry point and native multipage router
app_pages/                     Main page scripts and focused detail views, including the routine planner
src/components.py              Shared cards, resource loading and UI helpers
src/content.py                 Topic content and transparent finder mappings
src/utils/data_loader.py       CSV loading, validation and filtering
data/resources/resources.csv   Nine sourced resource records
guides/                        Three markdown setup guides
scripts/check_resource_links.py Manually run URL checker; report goes to ignored reports/
assets/images/                 Local hero photo, optimized page photos, and original SVG illustrations
tests/                         Existing resource loader unit tests
docs/                          Sources, image credits, evidence and project materials
.codex_backups/                Dated pre-edit backups; ignored by Git
```

The `app.py` entry point registers visible pages with `st.Page` and `st.navigation(position="top")`. Hidden Streamlit detail pages handle individual resource, topic, and guide views. Resource data and guide text remain outside the interface scripts. The finder uses fixed mappings in `src/content.py`; it does not use AI or claim clinical personalization. Planner, guide, resource checklist, and self-audit progress remain in Streamlit session state and are not saved to a database or sent to an external service.

## Install and run

Install Python 3.13, then run these commands in PowerShell from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Alternatively, run without activating the environment:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Manually check official resource links

Run this only when you want to make network requests. It reads the catalogue and writes a separate ignored CSV report; it never edits resource records and is not called by the Streamlit app.

```powershell
.\.venv\Scripts\python.exe scripts\check_resource_links.py
```

The report is written to `reports/resource_link_check.csv`. A responding URL does not prove that its content is accurate, safe, or endorsed.

## Resource and image methods

Resource descriptions are original summaries based on linked official provider or project pages. Cost, compatibility, privacy and accessibility details are qualified when not stated in the reviewed source. See [docs/resource_sources.md](docs/resource_sources.md). Photograph sources, creators, license checks, placements, and access dates are recorded in [docs/image_credits.md](docs/image_credits.md). The official Google product-reference screenshots are unaltered, attributed school-project references permitted by Google's [Brand Resource Center guidance](https://about.google/brand-resource-center/guidance/); they are not personal-device screenshots or testing evidence. Their interfaces may vary by device, operating-system version, or product update. Existing photographs are contextual illustrations and do not imply endorsement by the people shown. The source license does not replace any separate rights that may apply to recognizable people or brands.

## Limitations and next steps

Product details and device interfaces can change by version, region, device and account. Source review is not a security audit or endorsement. The resource finder is a transparent rule-based mapping, not an AI recommendation. Accessibility has not had a formal audit and student usability sessions have not yet been conducted.

Capture genuine setup screenshots and demonstration evidence using [docs/evidence_checklist.md](docs/evidence_checklist.md). Product-reference images help explain interfaces but do not replace your own setup screenshots or demonstrate testing. Review the interface visually and with a keyboard on desktop and narrow/mobile viewports. The student feedback form is at [docs/student_feedback_form.md](docs/student_feedback_form.md); no participant feedback is claimed. Sprint 6 interactive features still need manual usability, link, and accessibility review before submission.

See [docs/final_project_report.md](docs/final_project_report.md) and [docs/presentation_outline.md](docs/presentation_outline.md) for submission materials. Record only checks and results actually completed.
