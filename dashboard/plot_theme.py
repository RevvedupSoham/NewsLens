"""
Centralized visual language for every chart on the NewsLens dashboard.

Charts are rendered client-side with Plotly.js (see static/js/newslens.js),
so instead of building `plotly.graph_objects` figures here, this module is
the single source of truth for the design tokens (colors, fonts, spacing)
that every chart must use. `views.overview` serializes PLOT_THEME straight
into the page as JSON, and newslens.js reads it when constructing each
`Plotly.newPlot(...)` call. Keeping the tokens in one Python module (rather
than duplicated inline in JS) means the whole dashboard's chart language
changes from one place.

If a future iteration renders figures server-side with the `plotly` Python
package instead, `base_layout()` below returns an equivalent layout dict
that can be passed directly to `go.Figure(layout=...)`.
"""

COLORS = {
    "background": "#090B0F",
    "surface": "#0F1217",
    "surface_alt": "#14181F",
    "surface_elevated": "#191E26",
    "border": "rgba(255,255,255,0.07)",
    "accent": "#4CC9F0",
    "accent_secondary": "#60A5FA",
    "positive": "#4ADE80",
    "negative": "#FB7185",
    "neutral": "#94A3B8",
    "warning": "#FBBF24",
    "text": "#F3F4F6",
    "text_secondary": "#9CA3AF",
    "text_muted": "#6B7280",
    "grid": "rgba(255,255,255,0.06)",
}

# Ordered palette used when a chart needs one trace per source. Kept short
# and controlled on purpose -- brief explicitly rules out a rainbow chart.
SOURCE_PALETTE = [
    "#4CC9F0",  # accent
    "#60A5FA",  # secondary blue
    "#A78BFA",  # violet, used sparingly as the third series only
    "#FBBF24",  # warning, used only where a 4th/5th trace is unavoidable
    "#4ADE80",
]

FONT_FAMILY = "Inter, -apple-system, 'Segoe UI', sans-serif"
MONO_FAMILY = "'JetBrains Mono', 'IBM Plex Mono', ui-monospace, monospace"

MODEBAR_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "displaylogo": False,
}


def base_layout(height=280, extra=None):
    """Shared Plotly layout dict every chart should start from."""
    layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": FONT_FAMILY,
            "color": COLORS["text_secondary"],
            "size": 12,
        },
        "margin": {"l": 48, "r": 16, "t": 16, "b": 36},
        "height": height,
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
            "font": {"size": 11, "color": COLORS["text_secondary"]},
            "bgcolor": "rgba(0,0,0,0)",
        },
        "hoverlabel": {
            "bgcolor": COLORS["surface_elevated"],
            "bordercolor": COLORS["border"],
            "font": {"family": FONT_FAMILY, "color": COLORS["text"], "size": 12},
        },
        "xaxis": {
            "gridcolor": COLORS["grid"],
            "zerolinecolor": COLORS["grid"],
            "color": COLORS["text_muted"],
            "linecolor": COLORS["border"],
            "tickfont": {"size": 11},
        },
        "yaxis": {
            "gridcolor": COLORS["grid"],
            "zerolinecolor": COLORS["grid"],
            "color": COLORS["text_muted"],
            "linecolor": COLORS["border"],
            "tickfont": {"size": 11},
        },
    }
    if extra:
        layout.update(extra)
    return layout


def as_json_theme():
    """Theme payload embedded into the page for newslens.js to consume."""
    return {
        "colors": COLORS,
        "sourcePalette": SOURCE_PALETTE,
        "fontFamily": FONT_FAMILY,
        "monoFamily": MONO_FAMILY,
        "modebarConfig": MODEBAR_CONFIG,
        "baseLayout": base_layout(),
    }
