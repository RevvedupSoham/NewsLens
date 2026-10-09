"""
Dashboard data services.

NewsLens's real narrative-framing / sentiment / entity pipeline is out of
scope for this task (see project brief). Every function below returns
clearly-structured, clearly-labeled demo data shaped exactly like what the
real analysis pipeline would eventually return, so the dashboard's views
and templates don't need to change when that pipeline is wired in later --
only these functions do.
"""

FRAMING_DIMENSIONS = [
    "Political", "Economic", "Social", "Environmental", "Security", "Human Interest",
]

EMOTIONS = ["Joy", "Sadness", "Anger", "Fear", "Surprise", "Neutral"]


def get_kpis():
    return [
        {"label": "Articles Analyzed", "value": "128", "delta": "+12 this week", "tone": "positive"},
        {"label": "Events Tracked", "value": "24", "delta": "+3 this week", "tone": "positive"},
        {"label": "Sources Compared", "value": "17", "delta": "steady", "tone": "neutral"},
        {"label": "Avg. Semantic Similarity", "value": "78.4%", "delta": "-1.2 pts", "tone": "negative"},
        {"label": "Narrative Divergence", "value": "21.6%", "delta": "+0.8 pts", "tone": "warning"},
    ]


def get_narrative_landscape():
    """Grouped horizontal bars: framing-dimension emphasis per source."""
    sources = {
        "The Guardian": [0.72, 0.41, 0.68, 0.55, 0.30, 0.22],
        "Reuters":      [0.38, 0.74, 0.30, 0.20, 0.42, 0.15],
        "BBC":          [0.55, 0.48, 0.61, 0.33, 0.47, 0.29],
        "Al Jazeera":   [0.66, 0.35, 0.52, 0.24, 0.63, 0.31],
        "Associated Press": [0.44, 0.52, 0.40, 0.26, 0.39, 0.18],
    }
    return {
        "dimensions": FRAMING_DIMENSIONS,
        "sources": [{"name": name, "values": values} for name, values in sources.items()],
    }


def get_same_event_cards():
    return {
        "event_name": "Global Climate Summit \u2014 Closing Session",
        "cards": [
            {
                "source": "Reuters",
                "headline": "Nations agree on emissions framework after late-night talks",
                "time": "2h ago",
                "frame": "Economic",
                "sentiment": "Neutral",
                "emotion": "Neutral",
                "similarity": "81%",
                "entities": ["UN Climate Body", "G20", "Emissions Framework"],
                "excerpt": "Negotiators reached a compromise text early Friday, focusing on financing "
                           "mechanisms for developing economies rather than binding targets.",
            },
            {
                "source": "BBC",
                "headline": "Climate deal criticized as too weak by island nations",
                "time": "1h ago",
                "frame": "Social",
                "sentiment": "Negative",
                "emotion": "Concern",
                "similarity": "74%",
                "entities": ["Pacific Island Forum", "Sea-level Rise", "Emissions Framework"],
                "excerpt": "Delegates from low-lying nations said the agreement fails to reflect the "
                           "urgency communities already facing displacement are living through.",
            },
            {
                "source": "Al Jazeera",
                "headline": "Wealthy nations accused of stalling climate justice again",
                "time": "45m ago",
                "frame": "Political",
                "sentiment": "Negative",
                "emotion": "Anger",
                "similarity": "69%",
                "entities": ["G20", "Global South", "Climate Finance"],
                "excerpt": "Critics say the closing statement repeats a pattern of wealthy nations "
                           "deferring responsibility onto future summits without firm commitments.",
            },
        ],
    }


def get_narrative_fingerprint():
    """Radar/polar chart: same dimensions, per-source shape."""
    sources = {
        "Reuters": [0.38, 0.74, 0.30, 0.20, 0.42, 0.15],
        "BBC": [0.55, 0.48, 0.61, 0.33, 0.47, 0.29],
        "Al Jazeera": [0.66, 0.35, 0.52, 0.24, 0.63, 0.31],
    }
    return {
        "dimensions": FRAMING_DIMENSIONS,
        "sources": [{"name": name, "values": values} for name, values in sources.items()],
    }


def get_emotional_signal():
    sources = {
        "Reuters": [0.12, 0.08, 0.05, 0.10, 0.07, 0.58],
        "BBC": [0.09, 0.22, 0.14, 0.18, 0.09, 0.28],
        "Al Jazeera": [0.06, 0.19, 0.31, 0.15, 0.11, 0.18],
    }
    return {
        "emotions": EMOTIONS,
        "sources": [{"name": name, "values": values} for name, values in sources.items()],
    }


def get_topic_distribution():
    return {
        "topics": ["Politics", "Economy", "International Affairs", "Society", "Environment", "Security", "Healthcare", "Education"],
        "values": [24, 19, 17, 14, 11, 8, 4, 3],
    }


def get_entity_intelligence():
    return [
        {"entity": "Narendra Modi", "type": "PERSON", "mentions": 18, "sources": 4},
        {"entity": "India", "type": "LOCATION", "mentions": 27, "sources": 5},
        {"entity": "United Nations", "type": "ORGANIZATION", "mentions": 12, "sources": 3},
        {"entity": "European Union", "type": "ORGANIZATION", "mentions": 15, "sources": 4},
        {"entity": "Antonio Guterres", "type": "PERSON", "mentions": 9, "sources": 3},
        {"entity": "Pacific Islands Forum", "type": "ORGANIZATION", "mentions": 7, "sources": 2},
    ]


def get_narrative_evolution():
    """Line chart: framing emphasis across reporting dates for one event."""
    dates = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6"]
    return {
        "dates": dates,
        "series": [
            {"dimension": "Political", "values": [0.30, 0.34, 0.41, 0.52, 0.58, 0.63]},
            {"dimension": "Economic", "values": [0.55, 0.51, 0.47, 0.44, 0.40, 0.38]},
            {"dimension": "Social", "values": [0.22, 0.28, 0.33, 0.35, 0.39, 0.41]},
            {"dimension": "Security", "values": [0.12, 0.14, 0.15, 0.19, 0.24, 0.27]},
        ],
    }


def get_narrative_divergence():
    return {
        "divergence_pct": 21.6,
        "semantic_similarity": 78.4,
        "framing_distance": 0.34,
        "emotional_distance": 0.27,
    }


def get_recent_events():
    return [
        {"event": "India Budget 2026", "sources": 6, "articles": 22, "theme": "Economic", "similarity": "83%", "updated": "2h ago"},
        {"event": "Global Climate Summit", "sources": 5, "articles": 18, "theme": "Environmental", "similarity": "74%", "updated": "45m ago"},
        {"event": "AI Regulation Debate", "sources": 7, "articles": 26, "theme": "Political", "similarity": "69%", "updated": "3h ago"},
        {"event": "Major Election Developments", "sources": 8, "articles": 31, "theme": "Political", "similarity": "61%", "updated": "5h ago"},
        {"event": "Global Economic Outlook", "sources": 4, "articles": 14, "theme": "Economic", "similarity": "88%", "updated": "6h ago"},
    ]


# ---------------------------------------------------------------------------
# Articles
# ---------------------------------------------------------------------------

def get_articles():
    """Flat table of demo articles backing the Articles page."""
    rows = [
        ("Nations agree on emissions framework after late-night talks", "Reuters", "Global Climate Summit", "2h ago", "Neutral", "Neutral", "Economic", "81%"),
        ("Climate deal criticized as too weak by island nations", "BBC", "Global Climate Summit", "1h ago", "Negative", "Concern", "Social", "74%"),
        ("Wealthy nations accused of stalling climate justice again", "Al Jazeera", "Global Climate Summit", "45m ago", "Negative", "Anger", "Political", "69%"),
        ("Government unveils India Budget 2026 with tax relief for middle class", "The Guardian", "India Budget 2026", "3h ago", "Positive", "Optimism", "Economic", "85%"),
        ("Budget 2026: economists split on long-term fiscal impact", "Reuters", "India Budget 2026", "2h ago", "Neutral", "Neutral", "Economic", "79%"),
        ("Opposition calls new budget a missed opportunity for jobs", "Al Jazeera", "India Budget 2026", "1h ago", "Negative", "Frustration", "Political", "66%"),
        ("Lawmakers clash over proposed AI regulation framework", "BBC", "AI Regulation Debate", "4h ago", "Negative", "Concern", "Political", "71%"),
        ("Tech industry warns new AI rules could slow innovation", "Associated Press", "AI Regulation Debate", "3h ago", "Neutral", "Neutral", "Economic", "77%"),
        ("Civil society groups welcome stronger AI oversight proposal", "The Guardian", "AI Regulation Debate", "2h ago", "Positive", "Relief", "Social", "68%"),
        ("Regulators say framework balances innovation and safety", "Reuters", "AI Regulation Debate", "1h ago", "Neutral", "Neutral", "Political", "73%"),
        ("Election results reshape balance of power in parliament", "BBC", "Major Election Developments", "5h ago", "Neutral", "Neutral", "Political", "64%"),
        ("Markets react cautiously to surprise election outcome", "Reuters", "Major Election Developments", "4h ago", "Neutral", "Concern", "Economic", "70%"),
        ("Analysts say election signals shift toward coalition politics", "Al Jazeera", "Major Election Developments", "3h ago", "Neutral", "Neutral", "Political", "58%"),
        ("Winning coalition pledges swift economic reform", "The Guardian", "Major Election Developments", "2h ago", "Positive", "Optimism", "Political", "61%"),
        ("Global growth forecast revised upward for next fiscal year", "Associated Press", "Global Economic Outlook", "6h ago", "Positive", "Optimism", "Economic", "90%"),
        ("IMF flags inflation risk despite improved growth outlook", "Reuters", "Global Economic Outlook", "5h ago", "Neutral", "Concern", "Economic", "86%"),
        ("Emerging markets seen as key driver of 2026 recovery", "BBC", "Global Economic Outlook", "4h ago", "Positive", "Optimism", "Economic", "84%"),
        ("Central banks signal cautious approach to rate cuts", "The Guardian", "Global Economic Outlook", "3h ago", "Neutral", "Neutral", "Economic", "88%"),
    ]
    fields = ["title", "source", "event", "published", "sentiment", "emotion", "topic", "similarity"]
    return [dict(zip(fields, r)) for r in rows]


def get_article_filters():
    articles = get_articles()
    return {
        "sources": sorted({a["source"] for a in articles}),
        "events": sorted({a["event"] for a in articles}),
        "sentiments": ["Positive", "Neutral", "Negative"],
        "topics": sorted({a["topic"] for a in articles}),
    }


# ---------------------------------------------------------------------------
# Compare
# ---------------------------------------------------------------------------

COMPARE_EVENTS = {
    "climate-summit": {
        "label": "Global Climate Summit — Closing Session",
        "sources": ["Reuters", "BBC", "Al Jazeera"],
        "dimensions": FRAMING_DIMENSIONS,
        "fingerprint": {
            "Reuters": [0.38, 0.74, 0.30, 0.20, 0.42, 0.15],
            "BBC": [0.55, 0.48, 0.61, 0.33, 0.47, 0.29],
            "Al Jazeera": [0.66, 0.35, 0.52, 0.24, 0.63, 0.31],
        },
        "matrix": [
            {"source": "Reuters", "title": "Nations agree on emissions framework after late-night talks", "sentiment": "Neutral", "emotion": "Neutral", "topic": "Economic", "frame": "Economic", "similarity": "81%"},
            {"source": "BBC", "title": "Climate deal criticized as too weak by island nations", "sentiment": "Negative", "emotion": "Concern", "topic": "Social", "frame": "Social", "similarity": "74%"},
            {"source": "Al Jazeera", "title": "Wealthy nations accused of stalling climate justice again", "sentiment": "Negative", "emotion": "Anger", "topic": "Political", "frame": "Political", "similarity": "69%"},
        ],
        "differences": [
            "Reuters places greater emphasis on economic framing — financing mechanisms and fiscal terms dominate its coverage.",
            "BBC gives more weight to the social dimension, foregrounding communities already affected by rising sea levels.",
            "Al Jazeera registers the strongest political framing, centering responsibility and accountability among wealthy nations.",
        ],
    },
    "india-budget": {
        "label": "India Budget 2026",
        "sources": ["The Guardian", "Reuters", "Al Jazeera"],
        "dimensions": FRAMING_DIMENSIONS,
        "fingerprint": {
            "The Guardian": [0.28, 0.81, 0.34, 0.12, 0.18, 0.22],
            "Reuters": [0.24, 0.86, 0.22, 0.10, 0.15, 0.14],
            "Al Jazeera": [0.58, 0.62, 0.40, 0.14, 0.26, 0.19],
        },
        "matrix": [
            {"source": "The Guardian", "title": "Government unveils India Budget 2026 with tax relief for middle class", "sentiment": "Positive", "emotion": "Optimism", "topic": "Economic", "frame": "Economic", "similarity": "85%"},
            {"source": "Reuters", "title": "Budget 2026: economists split on long-term fiscal impact", "sentiment": "Neutral", "emotion": "Neutral", "topic": "Economic", "frame": "Economic", "similarity": "79%"},
            {"source": "Al Jazeera", "title": "Opposition calls new budget a missed opportunity for jobs", "sentiment": "Negative", "emotion": "Frustration", "topic": "Political", "frame": "Political", "similarity": "66%"},
        ],
        "differences": [
            "Reuters holds the strongest economic framing of the three, concentrating almost entirely on fiscal mechanics.",
            "Al Jazeera shows comparatively higher political framing, foregrounding opposition reaction over budget mechanics.",
            "The Guardian's coverage sits between the two, blending economic detail with household-level impact.",
        ],
    },
    "ai-regulation": {
        "label": "AI Regulation Debate",
        "sources": ["BBC", "Associated Press", "The Guardian"],
        "dimensions": FRAMING_DIMENSIONS,
        "fingerprint": {
            "BBC": [0.64, 0.30, 0.28, 0.10, 0.22, 0.16],
            "Associated Press": [0.32, 0.58, 0.24, 0.08, 0.19, 0.12],
            "The Guardian": [0.40, 0.28, 0.62, 0.14, 0.24, 0.20],
        },
        "matrix": [
            {"source": "BBC", "title": "Lawmakers clash over proposed AI regulation framework", "sentiment": "Negative", "emotion": "Concern", "topic": "Political", "frame": "Political", "similarity": "71%"},
            {"source": "Associated Press", "title": "Tech industry warns new AI rules could slow innovation", "sentiment": "Neutral", "emotion": "Neutral", "topic": "Economic", "frame": "Economic", "similarity": "77%"},
            {"source": "The Guardian", "title": "Civil society groups welcome stronger AI oversight proposal", "sentiment": "Positive", "emotion": "Relief", "topic": "Social", "frame": "Social", "similarity": "68%"},
        ],
        "differences": [
            "BBC's coverage carries the strongest political framing, centered on legislative disagreement.",
            "Associated Press leans most heavily economic, emphasizing industry and innovation impact.",
            "The Guardian gives comparatively more weight to the social dimension, foregrounding civil-society reaction.",
        ],
    },
}


def get_compare_events():
    return [{"slug": slug, "label": data["label"]} for slug, data in COMPARE_EVENTS.items()]


def get_compare_data(slug):
    slug = slug if slug in COMPARE_EVENTS else next(iter(COMPARE_EVENTS))
    data = COMPARE_EVENTS[slug]
    return {
        "slug": slug,
        "label": data["label"],
        "matrix": data["matrix"],
        "differences": data["differences"],
        "fingerprint": {
            "dimensions": data["dimensions"],
            "sources": [{"name": name, "values": values} for name, values in data["fingerprint"].items()],
        },
    }


# ---------------------------------------------------------------------------
# Analysis (single-article deep dive)
# ---------------------------------------------------------------------------

def get_analysis_article():
    return {
        "title": "Wealthy nations accused of stalling climate justice again",
        "source": "Al Jazeera",
        "author": "H. Osei",
        "published": "45m ago",
        "event": "Global Climate Summit — Closing Session",
        "summary": "Critics say the closing statement repeats a pattern of wealthy nations deferring "
                   "responsibility onto future summits without firm commitments, reigniting long-running "
                   "disputes over climate finance and historical emissions responsibility.",
        "sentiment": "Negative",
        "emotion": "Anger",
        "similarity": "69%",
        "topic": "Political",
        "frame": "Political",
        "entities": {
            "PERSON": ["A. Guterres", "M. Fontaine"],
            "ORGANIZATION": ["G20", "UN Climate Body", "Global South Coalition"],
            "LOCATION": ["Global South", "Pacific Islands"],
        },
        "keywords": ["climate finance", "accountability", "emissions", "global south", "summit"],
        "framing_scores": [
            {"label": "Political", "value": 0.66},
            {"label": "Economic", "value": 0.35},
            {"label": "Social", "value": 0.52},
            {"label": "Environmental", "value": 0.24},
            {"label": "Security", "value": 0.63},
            {"label": "Human Interest", "value": 0.31},
        ],
        "emotion_distribution": [
            {"label": "Joy", "value": 0.04},
            {"label": "Sadness", "value": 0.14},
            {"label": "Anger", "value": 0.41},
            {"label": "Fear", "value": 0.11},
            {"label": "Surprise", "value": 0.06},
            {"label": "Neutral", "value": 0.24},
        ],
        "feature_contributions": [
            {"label": "accountability", "value": 0.31},
            {"label": "wealthy nations", "value": 0.27},
            {"label": "global south", "value": 0.19},
            {"label": "finance", "value": 0.14},
            {"label": "summit", "value": -0.09},
        ],
    }


# ---------------------------------------------------------------------------
# Narrative Trends
# ---------------------------------------------------------------------------

def get_trends_filters():
    return {
        "dimensions": FRAMING_DIMENSIONS,
        "events": [e["label"] for e in get_compare_events()],
        "sources": ["Reuters", "BBC", "Al Jazeera", "The Guardian", "Associated Press"],
    }


def get_trends_evolution():
    return get_narrative_evolution()


def get_trends_similarity_over_time():
    dates = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6"]
    return {
        "dates": dates,
        "series": [
            {"name": "Reuters", "values": [0.88, 0.85, 0.83, 0.80, 0.79, 0.81]},
            {"name": "BBC", "values": [0.79, 0.78, 0.75, 0.74, 0.72, 0.74]},
            {"name": "Al Jazeera", "values": [0.74, 0.71, 0.70, 0.69, 0.68, 0.69]},
        ],
    }


def get_trends_sentiment_shift():
    dates = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6"]
    return {
        "dates": dates,
        "series": [
            {"name": "Positive", "values": [0.28, 0.30, 0.33, 0.31, 0.29, 0.27]},
            {"name": "Neutral", "values": [0.46, 0.44, 0.40, 0.39, 0.38, 0.37]},
            {"name": "Negative", "values": [0.26, 0.26, 0.27, 0.30, 0.33, 0.36]},
        ],
    }


# ---------------------------------------------------------------------------
# Settings / Profile
# ---------------------------------------------------------------------------

def get_settings_data():
    return {
        "profile": {"name": "R. Ahuja", "email": "r.ahuja@newslens.example", "role": "Researcher"},
        "pipeline": {"model_version": "demo-0.1.0", "mode": "Mocked analysis pipeline", "last_seeded": "On project setup"},
        "notifications": [
            {"label": "New event detected", "enabled": True},
            {"label": "Weekly divergence digest", "enabled": True},
            {"label": "Source coverage gaps", "enabled": False},
        ],
    }


def get_profile_data():
    return {
        "name": "R. Ahuja",
        "role": "Researcher",
        "organization": "Independent Media Research Lab",
        "initials": "RA",
        "bio": "Studies how coverage of the same event diverges across outlets, with a focus on "
               "framing and emotional language rather than truth or bias judgments.",
        "stats": [
            {"label": "Events followed", "value": "24"},
            {"label": "Articles reviewed", "value": "128"},
            {"label": "Comparisons run", "value": "37"},
        ],
        "activity": [
            {"action": "Compared 3 sources on", "target": "Global Climate Summit", "time": "45m ago"},
            {"action": "Reviewed article from", "target": "Al Jazeera", "time": "1h ago"},
            {"action": "Flagged divergence spike on", "target": "AI Regulation Debate", "time": "3h ago"},
            {"action": "Added event", "target": "India Budget 2026", "time": "1d ago"},
        ],
    }
