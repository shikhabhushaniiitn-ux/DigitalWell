"""Editorial content for DigitalWell topic, guide, and finder pages."""

TOPICS = {
    "focus": {
        "title": "Focus & Productivity",
        "image": "focus.svg",
        "photo": "photos/topic_focus.jpg",
        "alt": "A student studying at a library table with a laptop and notes.",
        "summary": "Make room for study by noticing and reducing avoidable digital interruptions.",
        "challenges": ["Frequent app or message interruptions", "Distracting sites during study blocks", "Difficulty restarting after a notification"],
        "habits": ["Choose one task before opening your device.", "Silence nonessential notifications for a short study block.", "Schedule a planned break and keep essential communication available."],
        "resources": ["stayfocusd", "leechblock", "freedom"],
        "guides": ["leechblock"],
    },
    "screen-time": {
        "title": "Screen-Time Balance",
        "image": "screen_balance.svg",
        "photo": "photos/home_digital_balance.jpg",
        "alt": "A hiker checks a phone while planning a route outdoors.",
        "summary": "Look at how, when, and why you use devices, then choose a boundary that fits your day.",
        "challenges": ["Losing track of time in apps", "Switching often between coursework and social apps", "Relying on a single total-time number without context"],
        "habits": ["Review app use as information, not a score.", "Set a realistic limit for one app at a time.", "Make space for offline study breaks, meals, movement, and social time."],
        "resources": ["google-dw", "apple-screen-time", "freedom"],
        "guides": ["android-timer"],
    },
    "sleep": {
        "title": "Sleep & Digital Habits",
        "image": "sleep.svg",
        "photo": "photos/guide_bedtime.jpg",
        "alt": "A quiet bedroom with a bedside lamp and an uncluttered nightstand.",
        "summary": "Explore device routines that make it easier to protect time for rest.",
        "challenges": ["Late-night notifications", "Using a phone in bed longer than intended", "Different routines across class or work days"],
        "habits": ["Choose a wind-down time and adjust it to your routine.", "Review notification exceptions so important contacts remain reachable.", "Keep an alarm plan before changing bedtime settings."],
        "resources": ["google-dw", "apple-screen-time"],
        "guides": ["bedtime"],
    },
    "privacy": {
        "title": "Privacy & Online Safety",
        "image": "privacy.svg",
        "photo": "photos/privacy_secure_laptop.jpg",
        "alt": "Hands typing on a laptop in a quiet, focused workspace.",
        "summary": "Build everyday habits for protecting accounts, personal information, and browsing privacy.",
        "challenges": ["Unclear app or extension permissions", "Unexpected links, messages, or requests for data", "Difficulty understanding tracking and privacy settings"],
        "habits": ["Check permissions against the feature you want to use.", "Use unique passwords and multi-factor authentication where available.", "Install from official sources and keep software updated."],
        "resources": ["eff-ssd", "isoc-safety", "firefox-etp", "privacy-badger"],
        "guides": [],
    },
}

GUIDES = {
    "android-timer": {
        "title": "Android app timer",
        "filename": "guide_01_android_app_timer.md",
        "image": "screen_balance.svg",
        "photo": "photos/guide_app_timer.jpg",
        "alt": "A person checks a smartphone outdoors; this is a context photo, not an Android settings screen.",
        "summary": "Set a daily app limit using Digital Wellbeing on supported Android devices.",
    },
    "leechblock": {
        "title": "Block sites with LeechBlock NG",
        "filename": "guide_02_leechblock.md",
        "image": "focus.svg",
        "photo": "photos/resource_focus.jpg",
        "alt": "A student works at a library table; this is not a browser extension screenshot.",
        "summary": "Create a simple browser rule for selected distracting sites.",
    },
    "bedtime": {
        "title": "Android Bedtime mode",
        "filename": "guide_03_bedtime_mode.md",
        "image": "sleep.svg",
        "photo": "photos/guide_bedtime.jpg",
        "alt": "A bedside lamp creates a calm evening scene; this is not an Android settings screenshot.",
        "summary": "Set a bedtime schedule and review the screen or notification options.",
    },
}

FINDER_GOALS = {
    "I want to focus better": {
        "description": "Suggested from the focus and productivity topic. Choose a browser or cross-device option that fits your study setup.",
        "resources": ["stayfocusd", "leechblock", "freedom"],
        "guides": ["leechblock"],
    },
    "I want to reduce distracting screen time": {
        "description": "Suggested from screen-time tools. Built-in controls can help you review usage and set a boundary.",
        "resources": ["google-dw", "apple-screen-time", "freedom"],
        "guides": ["android-timer"],
    },
    "I want healthier bedtime habits": {
        "description": "Suggested from bedtime and device-routine content. Device settings vary; keep important alarms and contacts in mind.",
        "resources": ["google-dw", "apple-screen-time"],
        "guides": ["bedtime"],
    },
    "I want to improve my online privacy": {
        "description": "Suggested from privacy education and browser protection resources. Read current permissions and privacy information before installing tools.",
        "resources": ["eff-ssd", "isoc-safety", "firefox-etp", "privacy-badger"],
        "guides": [],
    },
}

RESOURCE_RELATED = {
    "google-dw": ["apple-screen-time", "freedom"],
    "apple-screen-time": ["google-dw", "freedom"],
    "stayfocusd": ["leechblock", "freedom"],
    "leechblock": ["stayfocusd", "freedom"],
    "freedom": ["google-dw", "leechblock"],
    "eff-ssd": ["isoc-safety", "privacy-badger"],
    "isoc-safety": ["eff-ssd", "privacy-badger"],
    "firefox-etp": ["privacy-badger", "eff-ssd"],
    "privacy-badger": ["firefox-etp", "eff-ssd"],
}
