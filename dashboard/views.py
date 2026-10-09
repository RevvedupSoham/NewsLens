from django.shortcuts import render

from . import services
from .plot_theme import as_json_theme


def _nav_context(active, page_title):
    return {"page_title": page_title, "active_nav": active}


def overview(request):
    # NOTE: this is a plain dict, not a pre-serialized string. The template
    # serializes it exactly once via the `json_script` filter -- json.dumps-ing
    # it here too would double-encode it into a JSON string-of-a-string.
    chart_payload = {
        "theme": as_json_theme(),
        "narrativeLandscape": services.get_narrative_landscape(),
        "narrativeFingerprint": services.get_narrative_fingerprint(),
        "emotionalSignal": services.get_emotional_signal(),
        "topicDistribution": services.get_topic_distribution(),
        "narrativeEvolution": services.get_narrative_evolution(),
    }

    context = {
        **_nav_context("overview", "Overview"),
        "kpis": services.get_kpis(),
        "same_event": services.get_same_event_cards(),
        "entities": services.get_entity_intelligence(),
        "divergence": services.get_narrative_divergence(),
        "recent_events": services.get_recent_events(),
        "chart_data": chart_payload,
    }
    return render(request, "dashboard/overview.html", context)


def articles(request):
    context = {
        **_nav_context("articles", "Articles"),
        "articles": services.get_articles(),
        "filters": services.get_article_filters(),
    }
    return render(request, "dashboard/articles.html", context)


def compare(request):
    slug = request.GET.get("event", "")
    data = services.get_compare_data(slug)

    chart_payload = {
        "theme": as_json_theme(),
        "narrativeFingerprint": data["fingerprint"],
    }

    context = {
        **_nav_context("compare", "Compare"),
        "events": services.get_compare_events(),
        "active_event": data["slug"],
        "event_label": data["label"],
        "matrix": data["matrix"],
        "differences": data["differences"],
        "chart_data": chart_payload,
    }
    return render(request, "dashboard/compare.html", context)


def analysis(request):
    article = services.get_analysis_article()
    chart_payload = {
        "theme": as_json_theme(),
        "framingScores": article["framing_scores"],
        "emotionDistribution": article["emotion_distribution"],
        "featureContributions": article["feature_contributions"],
    }
    context = {
        **_nav_context("analysis", "Analysis"),
        "article": article,
        "chart_data": chart_payload,
    }
    return render(request, "dashboard/analysis.html", context)


def trends(request):
    chart_payload = {
        "theme": as_json_theme(),
        "narrativeEvolution": services.get_trends_evolution(),
        "similarityOverTime": services.get_trends_similarity_over_time(),
        "sentimentShift": services.get_trends_sentiment_shift(),
    }
    context = {
        **_nav_context("trends", "Narrative Trends"),
        "filters": services.get_trends_filters(),
        "chart_data": chart_payload,
    }
    return render(request, "dashboard/trends.html", context)


def settings_view(request):
    context = {
        **_nav_context("settings", "Settings"),
        "settings": services.get_settings_data(),
    }
    return render(request, "dashboard/settings.html", context)


def profile(request):
    context = {
        **_nav_context("profile", "Profile"),
        "profile": services.get_profile_data(),
    }
    return render(request, "dashboard/profile.html", context)
