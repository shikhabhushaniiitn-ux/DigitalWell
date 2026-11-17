# DigitalWell — Final project report

## Problem statement

Students use connected devices for study, communication, and entertainment. It can be difficult to find approachable, trustworthy tools and compare their trade-offs for focus, screen habits, sleep, and online safety.

## Objectives

- Present student-relevant digital wellness resources in one place.
- Help students search and compare options using source-linked information.
- Provide practical topic pathways and introductory setup instructions.
- Encourage thoughtful review of privacy, permissions, limitations, and accessibility.

## Proposed solution

DigitalWell is a multipage Streamlit portal with Home, Explore Resources, Compare Tools, Digital Wellness Topics, Setup Guides, Resource Finder, Daily Routine Planner, Privacy & Online Safety, and About DigitalWell. Dedicated detail routes display individual resources, topic pathways, and guides.

## Main features

- Search and filter nine resources by name, category, purpose, and platform.
- View each resource's full source-backed details and related resources.
- Compare two to four resources by purpose, platforms, cost, privacy, accessibility, advantages, and limitations.
- Explore four topic pathways with common student challenges, practical habits, related resources, and guides.
- Use a transparent, fixed-rule finder for four common student goals.
- Draft a flexible, session-only study-day schedule with wake, study, break, meal, and wind-down times.
- Follow three interactive setup guides with session-only checkboxes and progress indicators.
- Use a guided next-step checklist after choosing a Finder goal.
- Compare resources with category/platform filters, difference cues, decision prompts, and CSV export.
- Review a per-resource pre-use checklist and an optional privacy/notification self-audit.
- Use a manually run link-check utility that writes a separate report and never modifies the catalogue.
- Browse a local Unsplash hero photo and original SVG illustrations.

## Technology stack

Python 3.13, Streamlit 1.67.0, Pandas, CSV, and Pytest. Sprint 6 adds no package dependencies; the manual link checker uses Python's standard library.

## Application architecture

`app.py` registers pages with Streamlit `st.Page` and `st.navigation(position="top")`. The `app_pages/` directory contains separate page scripts and three hidden detail views, plus the Daily Routine Planner. `src/components.py` provides shared image, navigation, resource-card, and loading helpers. `src/content.py` stores topic content, guide metadata, related-resource mappings, and fixed Finder rules. The existing CSV schema and `src/utils/data_loader.py` are preserved. Guides remain in Markdown under `guides/`. The optional link checker is a standalone standard-library script and is never run by the web app.

## Resource library

The nine entries cover built-in Android and Apple controls, website and app distraction blockers, privacy education, tracking protection, and online safety. Entries retain official source references and verification dates. Unknown costs, privacy practices, accessibility details, or compatibility are qualified rather than inferred. Source review is not a security audit or endorsement.

## Setup guides

1. Set an Android app timer using Digital Wellbeing.
2. Block distracting websites with LeechBlock NG.
3. Configure an Android Bedtime routine.

Each guide includes preparation, numbered instructions, an expected result, practical tips, troubleshooting, official references, and a placeholder for a genuine personal-device screenshot. The app also displays unaltered, attributed Google Play product-reference screenshots for app-timer outcome, Bedtime mode, Focus mode, and the Digital Wellbeing overview. These are illustrative references, not student captures or evidence of testing; interface labels vary by device and version. LeechBlock settings screenshots remain placeholders because no reuse license for the official site's UI images was found.

## Privacy and responsible use

The portal encourages students to review permissions and provider privacy information, use account-security practices, install tools from official sources, and preserve access to essential contacts and services. DigitalWell is educational information, not a medical service, diagnostic tool, legal adviser, or incident-response service. The resource finder uses explicit fixed mappings, not AI or clinical advice.

Planner entries, guide checkboxes, resource-review checks, and self-audit selections use Streamlit session state only. The app adds no accounts, database, or external service for these interactions. Selections do not certify security or change device settings.

## Testing actually performed

- `python -m pytest -q --basetemp=.pytest-tmp-20261111-1855`: 12 passed.
- Streamlit health endpoint at `http://127.0.0.1:8767/_stcore/health`: returned `ok`.
- `AppTest.from_file("app.py").run()`: rendered the Home page with no app exceptions.
- Student usability sessions, manual screenshots, full browser visual review, and formal accessibility audit have not been performed.
- Official reference screenshots are illustrative only and do not count as personal setup or testing evidence.
- Sprint 6 interactive additions require a fresh app run, functional review, student usability sessions, and accessibility review before submission. Do not treat the earlier test results above as verification of Sprint 6 changes.

## Limitations

Provider details and interfaces can change by version, region, device, and account. Some price, privacy, accessibility, or compatibility details are not stated in reviewed sources. The SVG assets are contextual illustrations and are not device interfaces. Student usability testing and formal accessibility review are pending.

## Future scope

- Capture genuine device and browser screenshots with personal information hidden.
- Review responsive layouts and keyboard navigation manually.
- Conduct voluntary student usability sessions and record anonymized feedback.
- Recheck official resource information at future milestones.
- Run `scripts/check_resource_links.py` manually and retain the generated report if a link-check record is needed.

## Conclusion

DigitalWell organizes practical, source-linked resources and student-friendly setup guidance behind clear multipage navigation. It is ready for a project demonstration after genuine screenshots, manual visual review, and student evaluation are completed.
