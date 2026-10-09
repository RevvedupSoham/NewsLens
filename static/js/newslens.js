(function () {
  "use strict";

  console.log("NewsLens: newslens.js loaded and running.");

  // ---------- icons ----------
  if (window.lucide) lucide.createIcons();

  // ---------- intro sequence: brand reveal, then dashboard opens up ----------
  (function runIntro() {
    var INTRO_ONCE_PER_SESSION = true; // set false to replay the intro on every page load
    var overlay = document.getElementById("intro-overlay");
    var shell = document.getElementById("app-shell");
    var reveal = window.__nlReveal || function () {
      if (overlay) overlay.style.display = "none";
      if (shell) shell.classList.add("app-in");
    };
    if (!overlay || !shell) return;

    var alreadyShown = INTRO_ONCE_PER_SESSION && sessionStorage.getItem("nl-intro-shown") === "1";
    if (alreadyShown) {
      reveal();
      return;
    }

    var mark = overlay.querySelector(".intro-mark");
    var brandEl = document.getElementById("intro-brand");
    var tagline = overlay.querySelector(".intro-tagline");
    var brandText = "NewsLens";

    brandEl.innerHTML = brandText.split("").map(function (ch, i) {
      var displayCh = ch === " " ? "&nbsp;" : ch;
      return '<span class="intro-letter" style="transition-delay:' + (i * 55) + 'ms">' + displayCh + "</span>";
    }).join("");

    requestAnimationFrame(function () {
      mark.classList.add("in");
      requestAnimationFrame(function () {
        overlay.querySelectorAll(".intro-letter").forEach(function (el) { el.classList.add("in"); });
      });
    });

    setTimeout(function () { tagline.classList.add("in"); }, 650);

    setTimeout(function () {
      overlay.classList.add("intro-exit");
      shell.classList.add("app-in");
      window.__nlRevealed = true;
      if (INTRO_ONCE_PER_SESSION) sessionStorage.setItem("nl-intro-shown", "1");
    }, 1650);

    setTimeout(function () { overlay.style.display = "none"; }, 2300);
  })();

  // ---------- mobile sidebar ----------
  var sidebar = document.getElementById("sidebar");
  var backdrop = document.getElementById("sidebar-backdrop");
  var toggle = document.getElementById("sidebar-toggle");

  function closeSidebar() {
    sidebar.classList.remove("open");
    backdrop.classList.remove("open");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("open");
      backdrop.classList.toggle("open");
    });
  }
  if (backdrop) backdrop.addEventListener("click", closeSidebar);

  // ---------- "Analyze Article" (out of scope for this prototype) ----------
  var analyzeBtn = document.getElementById("analyze-btn");
  if (analyzeBtn) {
    analyzeBtn.addEventListener("click", function () {
      showToast("Article analysis isn't wired up in this dashboard prototype yet.");
    });
  }

  function showToast(message) {
    var existing = document.getElementById("nl-toast");
    if (existing) existing.remove();
    var el = document.createElement("div");
    el.id = "nl-toast";
    el.textContent = message;
    el.style.cssText = [
      "position:fixed", "bottom:20px", "left:50%", "transform:translateX(-50%)",
      "background:#191E26", "color:#F3F4F6", "border:1px solid rgba(255,255,255,0.1)",
      "padding:10px 16px", "border-radius:9px", "font-size:12.5px", "z-index:999",
      "box-shadow:0 8px 24px rgba(0,0,0,0.4)", "opacity:0", "transition:opacity .2s ease"
    ].join(";");
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.style.opacity = "1"; });
    setTimeout(function () {
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 200);
    }, 2600);
  }
  window.NLShowToast = showToast;

  // ---------- chart data ----------
  var dataEl = document.getElementById("chart-data");
  if (!dataEl) return;
  var payload = JSON.parse(dataEl.textContent);
  var theme = payload.theme;
  var palette = theme.sourcePalette;
  var config = theme.modebarConfig;

  function mergeLayout(overrides) {
    return Object.assign({}, theme.baseLayout, overrides || {});
  }

  // ---------- Narrative Landscape (grouped horizontal bars) ----------
  (function () {
    var el = document.getElementById("chart-narrative-landscape");
    if (!el) return;
    var d = payload.narrativeLandscape;
    var traces = d.sources.map(function (s, i) {
      return {
        type: "bar",
        orientation: "h",
        name: s.name,
        y: d.dimensions,
        x: s.values,
        marker: { color: palette[i % palette.length] },
        hovertemplate: "%{y}: %{x:.0%}<extra>" + s.name + "</extra>",
      };
    });
    var layout = mergeLayout({
      barmode: "group",
      bargap: 0.24,
      bargroupgap: 0.12,
      xaxis: Object.assign({}, theme.baseLayout.xaxis, { tickformat: ".0%", range: [0, 1] }),
      yaxis: Object.assign({}, theme.baseLayout.yaxis, { automargin: true }),
      height: 340,
      margin: { l: 110, r: 16, t: 8, b: 36 },
    });
    Plotly.newPlot(el, traces, layout, config);
  })();

  // ---------- Narrative Fingerprint (radar) ----------
  (function () {
    var el = document.getElementById("chart-narrative-fingerprint");
    if (!el) return;
    var d = payload.narrativeFingerprint;
    var dims = d.dimensions.concat([d.dimensions[0]]);
    var traces = d.sources.map(function (s, i) {
      var vals = s.values.concat([s.values[0]]);
      var color = palette[i % palette.length];
      return {
        type: "scatterpolar",
        name: s.name,
        r: vals,
        theta: dims,
        fill: "toself",
        fillcolor: hexToRgba(color, 0.10),
        line: { color: color, width: 2 },
        marker: { size: 4, color: color },
      };
    });
    var layout = mergeLayout({
      height: 300,
      margin: { l: 40, r: 40, t: 20, b: 20 },
      polar: {
        bgcolor: "rgba(0,0,0,0)",
        radialaxis: {
          visible: true, range: [0, 1], showticklabels: false,
          gridcolor: theme.colors.grid, linecolor: theme.colors.border,
        },
        angularaxis: {
          gridcolor: theme.colors.grid, linecolor: theme.colors.border,
          color: theme.colors.text_muted, tickfont: { size: 10.5 },
        },
      },
    });
    Plotly.newPlot(el, traces, layout, config);
  })();

  // ---------- Emotional Signal (grouped vertical bars) ----------
  (function () {
    var el = document.getElementById("chart-emotional-signal");
    if (!el) return;
    var d = payload.emotionalSignal;
    var traces = d.sources.map(function (s, i) {
      return {
        type: "bar",
        name: s.name,
        x: d.emotions,
        y: s.values,
        marker: { color: palette[i % palette.length] },
        hovertemplate: "%{x}: %{y:.0%}<extra>" + s.name + "</extra>",
      };
    });
    var layout = mergeLayout({
      barmode: "group",
      bargap: 0.28,
      bargroupgap: 0.12,
      height: 300,
      margin: { l: 40, r: 16, t: 8, b: 40 },
      yaxis: Object.assign({}, theme.baseLayout.yaxis, { tickformat: ".0%" }),
    });
    Plotly.newPlot(el, traces, layout, config);
  })();

  // ---------- Dominant Themes (donut) ----------
  (function () {
    var el = document.getElementById("chart-topic-distribution");
    if (!el) return;
    var d = payload.topicDistribution;
    var donutColors = [
      "#4CC9F0", "#60A5FA", "#7DD3FC", "#A5B4FC",
      "#94A3B8", "#64748B", "#475569", "#334155",
    ];
    var trace = {
      type: "pie",
      labels: d.topics,
      values: d.values,
      hole: 0.62,
      sort: false,
      textinfo: "none",
      marker: { colors: donutColors, line: { color: theme.colors.surface, width: 2 } },
      hovertemplate: "%{label}: %{percent}<extra></extra>",
    };
    var layout = mergeLayout({
      height: 280,
      margin: { l: 8, r: 8, t: 8, b: 8 },
      showlegend: true,
      legend: Object.assign({}, theme.baseLayout.legend, {
        orientation: "v", x: 1, xanchor: "left", y: 0.5, yanchor: "middle", font: { size: 10.5 },
      }),
    });
    layout.margin.r = 120;
    Plotly.newPlot(el, [trace], layout, config);
  })();

  // ---------- Narrative Evolution (lines) ----------
  (function () {
    var el = document.getElementById("chart-narrative-evolution");
    if (!el) return;
    var d = payload.narrativeEvolution;
    var lineColors = { Political: "#4CC9F0", Economic: "#60A5FA", Social: "#4ADE80", Security: "#FBBF24" };
    var traces = d.series.map(function (s) {
      var color = lineColors[s.dimension] || theme.colors.neutral;
      return {
        type: "scatter",
        mode: "lines+markers",
        name: s.dimension,
        x: d.dates,
        y: s.values,
        line: { color: color, width: 2, shape: "spline" },
        marker: { size: 5, color: color },
        hovertemplate: "%{x} \u2014 %{y:.0%}<extra>" + s.dimension + "</extra>",
      };
    });
    var layout = mergeLayout({
      height: 280,
      margin: { l: 40, r: 16, t: 8, b: 36 },
      yaxis: Object.assign({}, theme.baseLayout.yaxis, { tickformat: ".0%" }),
    });
    Plotly.newPlot(el, traces, layout, config);
  })();

  function hexToRgba(hex, alpha) {
    var r = parseInt(hex.slice(1, 3), 16);
    var g = parseInt(hex.slice(3, 5), 16);
    var b = parseInt(hex.slice(5, 7), 16);
    return "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
  }

  // ---------- Analysis: Framing Scores (horizontal bar) ----------
  (function () {
    var el = document.getElementById("chart-framing-scores");
    if (!el) return;
    var d = payload.framingScores;
    var trace = {
      type: "bar",
      orientation: "h",
      x: d.map(function (r) { return r.value; }),
      y: d.map(function (r) { return r.label; }),
      marker: { color: theme.colors.accent },
      hovertemplate: "%{y}: %{x:.2f}<extra></extra>",
    };
    var layout = mergeLayout({
      height: 260,
      margin: { l: 110, r: 16, t: 8, b: 32 },
      xaxis: Object.assign({}, theme.baseLayout.xaxis, { range: [0, 1] }),
      yaxis: Object.assign({}, theme.baseLayout.yaxis, { autorange: "reversed" }),
    });
    Plotly.newPlot(el, [trace], layout, config);
  })();

  // ---------- Analysis: Emotion Distribution (vertical bar) ----------
  (function () {
    var el = document.getElementById("chart-emotion-distribution");
    if (!el) return;
    var d = payload.emotionDistribution;
    var trace = {
      type: "bar",
      x: d.map(function (r) { return r.label; }),
      y: d.map(function (r) { return r.value; }),
      marker: { color: theme.colors.accent_secondary },
      hovertemplate: "%{x}: %{y:.0%}<extra></extra>",
    };
    var layout = mergeLayout({
      height: 260,
      margin: { l: 40, r: 16, t: 8, b: 36 },
      yaxis: Object.assign({}, theme.baseLayout.yaxis, { tickformat: ".0%" }),
    });
    Plotly.newPlot(el, [trace], layout, config);
  })();

  // ---------- Analysis: Feature Contributions (diverging horizontal bar) ----------
  (function () {
    var el = document.getElementById("chart-feature-contributions");
    if (!el) return;
    var d = payload.featureContributions;
    var trace = {
      type: "bar",
      orientation: "h",
      x: d.map(function (r) { return r.value; }),
      y: d.map(function (r) { return r.label; }),
      marker: { color: d.map(function (r) { return r.value >= 0 ? theme.colors.positive : theme.colors.negative; }) },
      hovertemplate: "%{y}: %{x:+.2f}<extra></extra>",
    };
    var layout = mergeLayout({
      height: 220,
      margin: { l: 120, r: 16, t: 8, b: 32 },
      xaxis: Object.assign({}, theme.baseLayout.xaxis, { zeroline: true, zerolinecolor: theme.colors.border }),
      yaxis: Object.assign({}, theme.baseLayout.yaxis, { autorange: "reversed" }),
    });
    Plotly.newPlot(el, [trace], layout, config);
  })();

  // ---------- Trends: Semantic Similarity Over Time (lines) ----------
  (function () {
    var el = document.getElementById("chart-similarity-over-time");
    if (!el) return;
    var d = payload.similarityOverTime;
    var traces = d.series.map(function (s, i) {
      return {
        type: "scatter",
        mode: "lines+markers",
        name: s.name,
        x: d.dates,
        y: s.values,
        line: { color: palette[i % palette.length], width: 2, shape: "spline" },
        marker: { size: 5, color: palette[i % palette.length] },
        hovertemplate: "%{x} \u2014 %{y:.0%}<extra>" + s.name + "</extra>",
      };
    });
    var layout = mergeLayout({
      height: 280,
      margin: { l: 40, r: 16, t: 8, b: 36 },
      yaxis: Object.assign({}, theme.baseLayout.yaxis, { tickformat: ".0%" }),
    });
    Plotly.newPlot(el, traces, layout, config);
  })();

  // ---------- Trends: Sentiment Shift (stacked area) ----------
  (function () {
    var el = document.getElementById("chart-sentiment-shift");
    if (!el) return;
    var d = payload.sentimentShift;
    var colorFor = { Positive: theme.colors.positive, Neutral: theme.colors.neutral, Negative: theme.colors.negative };
    var traces = d.series.map(function (s) {
      return {
        type: "scatter",
        mode: "lines",
        name: s.name,
        x: d.dates,
        y: s.values,
        stackgroup: "one",
        line: { color: colorFor[s.name] || theme.colors.neutral, width: 1.5 },
        fillcolor: hexToRgba(colorFor[s.name] || "#94A3B8", 0.35),
        hovertemplate: "%{x} \u2014 %{y:.0%}<extra>" + s.name + "</extra>",
      };
    });
    var layout = mergeLayout({
      height: 280,
      margin: { l: 40, r: 16, t: 8, b: 36 },
      yaxis: Object.assign({}, theme.baseLayout.yaxis, { tickformat: ".0%", range: [0, 1] }),
    });
    Plotly.newPlot(el, traces, layout, config);
  })();

  // keep charts responsive on resize / sidebar toggle
  window.addEventListener("resize", function () {
    document.querySelectorAll(".js-plotly-plot").forEach(function (gd) {
      Plotly.Plots.resize(gd);
    });
  });
})();
