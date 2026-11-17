## Introduction
LeechBlock NG is a browser extension that can block chosen websites at set times or after a usage allowance. This guide gives a minimal starting setup. Extension interfaces may vary by browser, version and device.

## Requirements
- A supported browser and the LeechBlock NG extension installed from its official browser extension store.
- A short list of sites you personally want to limit.
- Permission to install extensions (managed school or work browsers may restrict this).

## Before you start
Use the official extension listing linked below. Read the permission prompt: the extension needs access to website addresses to apply block rules. Decide in advance which course, work, health and support sites must stay available.

## Steps
1. Open the LeechBlock NG toolbar button and choose **Options**.
2. Open **Block Set 1** (or another block set).
3. Under **What to Block**, enter one domain per line, such as `example.com`. Leave off `https://` and `www`.
4. Under **When to Block**, choose either a time window in 24-hour `HHMM-HHMM` format (for example, `0900-1200`) or a usage allowance. Avoid filling incompatible combinations until you understand the combination setting.
5. Select the days on which this rule should apply.
6. Scroll to the bottom and choose **Save Options**.
7. Test the rule with a nonessential site and adjust the schedule if it blocks too much.

## Practical tip
Try a short study window first. You can add allowed sites or adjust the schedule as your timetable changes. Avoid setting a block that could prevent access to coursework or help.

## Expected result
The selected domain should be blocked according to the schedule or allowance. LeechBlock requests site access permissions so it can inspect requested URLs and apply your rules. Its maintainer says the extension stores settings locally unless sync storage is chosen and does not send information to external sites; review the current permissions and policy yourself before installing.

## Troubleshooting
- **Nothing is blocked:** check that at least one domain is listed, a time rule is set, active days are selected, and options were saved.
- **A site still loads:** check whether you entered the correct domain and whether the extension has site access permission.
- **A needed page is blocked:** pause or edit the rule and add exceptions where appropriate. Do not block emergency, learning or support access.
- **The extension is unavailable:** check its official installation page for current browser support.

## Official references
- [LeechBlock documentation: Quick Start](https://www.proginosko.com/leechblock/documentation/)
- [LeechBlock FAQ: requested permissions and data](https://www.proginosko.com/leechblock/faq/permissions/)
- [LeechBlock NG on Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/leechblock-ng/)

> Screenshot placeholder: Capture the extension's block list and schedule with personal browsing data removed. No screenshot is included yet.
