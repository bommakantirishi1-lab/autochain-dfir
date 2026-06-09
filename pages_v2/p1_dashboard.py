"""
Investigation Command Center — EY DFIR AutoChain Enterprise
Executive dashboard: KPIs, sparklines, alert feed, case overview.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.graph_objects as go

from data_v2.mock_data import (
    CASES, DASHBOARD_STATS, RECENT_ALERTS,
    TIMELINE_EVENTS, IOCS, TACTIC_COLORS,
)

_ACCENT = {
    "yellow": "#FFE600", "red": "#FF4D4F", "orange": "#FA8C16",
    "blue": "#1890FF", "green": "#52C41A", "purple": "#722ED1", "teal": "#13C2C2",
}

def _sparkline(data: list[float], color: str = "#FFE600", height: int = 38) -> go.Figure:
    fig = go.Figure()
    hex_c = color.lstrip("#")
    r, g, b = int(hex_c[0:2],16), int(hex_c[2:4],16), int(hex_c[4:6],16)
    fig.add_trace(go.Scatter(
        y=data, mode="lines",
        line=dict(color=color, width=2, shape="spline"),
        fill="tozeroy", fillcolor=f"rgba({r},{g},{b},0.10)",
        hoverinfo="skip",
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=height, showlegend=False,
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
    )
    return fig


def _kpi_card(icon, label, value, trend, delta, color, spark_data):
    trend_color = "#52C41A" if trend == "up" else ("#6B7280" if trend == "neutral" else "#FF4D4F")
    arrow = "↑" if trend == "up" else ("→" if trend == "neutral" else "↓")
    st.markdown(f"""
    <div class="kpi-card accent-{color}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-trend {'up' if trend=='up' else 'neutral'}" style="color:{trend_color}">
            {arrow} {delta} <span style="color:#374151;font-size:10px"> vs last week</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(
        _sparkline(spark_data, _ACCENT.get(color, "#FFE600")),
        use_container_width=True, config={"displayModeBar": False},
    )


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📊 Investigation Command Center</div>
        <div class="page-subtitle">
            Real-time DFIR operations overview · EY Forensic &amp; Integrity Services
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ────────────────────────────────────────────────────────────
    kpi_defs = [
        ("active_cases",        "🔴", "Active Cases",      "red"),
        ("open_investigations", "📂", "Investigations",    "orange"),
        ("evidence_volume",     "💾", "Evidence Volume",   "blue"),
        ("timeline_events",     "⏱", "Timeline Events",   "purple"),
        ("iocs_discovered",     "🎯", "IOCs Found",        "yellow"),
        ("actor_matches",       "🕵", "Actor Matches",     "teal"),
        ("hours_saved",         "⚡", "Analyst Hrs Saved", "green"),
    ]
    cols = st.columns(7)
    for col, (key, icon, label, color) in zip(cols, kpi_defs):
        s = DASHBOARD_STATS[key]
        with col:
            _kpi_card(icon, label, s["value"], s["trend"], s["delta"], color, s["spark"])

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Row 2: Risk donut + Tactic bar ─────────────────────────────────────
    col_a, col_b = st.columns([1, 2])

    with col_a:
        st.markdown('<div class="section-title">🔴 Case Risk Distribution</div>', unsafe_allow_html=True)
        risk_map = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for c in CASES:
            risk_map[c["risk"]] = risk_map.get(c["risk"], 0) + 1
        colors_pie = ["#FF4D4F", "#FA8C16", "#FADB14", "#52C41A"]
        fig_donut = go.Figure(go.Pie(
            labels=list(risk_map.keys()), values=list(risk_map.values()),
            hole=0.60, marker_colors=colors_pie,
            textinfo="label+value", textfont=dict(color="white", size=11),
            hovertemplate="%{label}: %{value} cases<extra></extra>",
        ))
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0), height=210, showlegend=False,
            annotations=[dict(
                text=f"<b>{len(CASES)}</b><br><span style='font-size:12px'>Cases</span>",
                x=0.5, y=0.5, font=dict(size=18, color="white"), showarrow=False,
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        st.markdown('<div class="section-title">📈 ATT&CK Tactic Activity (Current Cases)</div>', unsafe_allow_html=True)
        tactic_counts: dict[str, int] = {}
        for ev in TIMELINE_EVENTS:
            t = ev["tactic"]
            tactic_counts[t] = tactic_counts.get(t, 0) + 1
        sorted_t = sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)
        fig_bar = go.Figure(go.Bar(
            x=[t for t, _ in sorted_t],
            y=[v for _, v in sorted_t],
            marker_color=[TACTIC_COLORS.get(t, "#6B7280") for t, _ in sorted_t],
            marker_line_width=0,
            hovertemplate="%{x}: %{y} events<extra></extra>",
        ))
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=8, b=0), height=210, showlegend=False,
            xaxis=dict(tickfont=dict(color="#6B7280", size=10), gridcolor="#1F2937", linecolor="#1F2937"),
            yaxis=dict(tickfont=dict(color="#6B7280", size=10), gridcolor="#1A2035", linecolor="rgba(0,0,0,0)"),
            bargap=0.28, font=dict(color="white"),
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # ── Row 3: Alert feed + Active cases ───────────────────────────────────
    col_c, col_d = st.columns([1.25, 1])

    with col_c:
        st.markdown('<div class="section-title">🚨 Live Alert Feed</div>', unsafe_allow_html=True)
        for alert in RECENT_ALERTS:
            st.markdown(f"""
            <div class="alert-item">
                <div class="alert-icon">{alert['icon']}</div>
                <div class="alert-body">
                    <div class="alert-title">{alert['title']}</div>
                    <div class="alert-desc">{alert['desc']}</div>
                </div>
                <div class="alert-time">{alert['time']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="section-title">⚡ Investigation Status</div>', unsafe_allow_html=True)
        for case in CASES[:6]:
            rc = case["risk"].lower()
            prog = case["attribution_confidence"]
            prog_col = {"critical": "red", "high": "orange", "medium": "yellow", "low": "green"}.get(rc, "blue")
            st.markdown(f"""
            <div style="padding:9px 0;border-bottom:1px solid #1A2035;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:5px">
                    <div style="flex:1;min-width:0">
                        <div style="font-size:10px;color:#6B7280;font-family:monospace">{case['id']}</div>
                        <div style="font-size:12px;font-weight:600;color:#E5E7EB;margin-top:2px;
                                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
                            {case['title'][:48]}{'…' if len(case['title'])>48 else ''}
                        </div>
                    </div>
                    <span class="badge badge-{rc}" style="margin-left:8px;flex-shrink:0">{case['risk']}</span>
                </div>
                <div style="display:flex;align-items:center;gap:8px">
                    <div class="ey-prog-wrap" style="flex:1">
                        <div class="ey-prog-fill {prog_col}" style="width:{prog}%"></div>
                    </div>
                    <span style="font-size:10px;color:#6B7280;flex-shrink:0">{prog}% attr.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align:right;margin-top:8px"><span style="font-size:12px;color:#FFE600">View all {len(CASES)} cases →</span></div>',
            unsafe_allow_html=True,
        )

    # ── Forensic Tools Stack Banner ────────────────────────────────────────
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0E1117;border:1px solid #2A3142;border-radius:8px;padding:12px 16px;margin-bottom:4px">
        <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px">
            🛠 Active Forensic Tooling Stack
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center">
            <span style="background:#1890FF18;color:#1890FF;padding:4px 12px;border-radius:10px;font-size:11px;font-weight:600;border:1px solid #1890FF33">🔷 Nuix 9.10</span>
            <span style="background:#52C41A18;color:#52C41A;padding:4px 12px;border-radius:10px;font-size:11px;font-weight:600;border:1px solid #52C41A33">🔍 EnCase 22.4</span>
            <span style="background:#FA8C1618;color:#FA8C16;padding:4px 12px;border-radius:10px;font-size:11px;font-weight:600;border:1px solid #FA8C1633">🧰 FTK Imager 4.7</span>
            <span style="background:#722ED118;color:#722ED1;padding:4px 12px;border-radius:10px;font-size:11px;font-weight:600;border:1px solid #722ED133">📱 Magnet AXIOM 7</span>
            <span style="background:#13C2C218;color:#13C2C2;padding:4px 12px;border-radius:10px;font-size:11px;font-weight:600;border:1px solid #13C2C233">🖥 OSForensics</span>
            <span style="background:#FF4D4F18;color:#FF4D4F;padding:4px 12px;border-radius:10px;font-size:11px;font-weight:600;border:1px solid #FF4D4F33">🧠 Volatility3</span>
            <span style="background:#EB2F9618;color:#EB2F96;padding:4px 12px;border-radius:10px;font-size:11px;font-weight:600;border:1px solid #EB2F9633">🌐 Wireshark</span>
            <span style="background:#FFC53D18;color:#FFC53D;padding:4px 12px;border-radius:10px;font-size:11px;font-weight:600;border:1px solid #FFC53D33">⚡ KAPE + Chainsaw</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 4: IOC distribution + Case types + Investigator load ──────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    col_e, col_f, col_g = st.columns(3)

    with col_e:
        st.markdown('<div class="section-title">🎯 IOC Type Distribution</div>', unsafe_allow_html=True)
        ioc_types: dict[str, int] = {}
        for ioc in IOCS:
            t = ioc["type"].replace("FILE_HASH_", "").replace("_", " ").title()
            ioc_types[t] = ioc_types.get(t, 0) + 1
        fig_ioc = go.Figure(go.Pie(
            labels=list(ioc_types.keys()), values=list(ioc_types.values()),
            hole=0.50,
            marker_colors=["#FF4D4F","#FA8C16","#FADB14","#52C41A","#1890FF","#722ED1","#13C2C2"],
            textinfo="percent", textfont=dict(color="white", size=10),
            hovertemplate="%{label}: %{value}<extra></extra>",
        ))
        fig_ioc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0), height=180,
            legend=dict(font=dict(color="#9CA3AF", size=9), bgcolor="rgba(0,0,0,0)", x=0.75, y=0.5),
        )
        st.plotly_chart(fig_ioc, use_container_width=True, config={"displayModeBar": False})

    with col_f:
        st.markdown('<div class="section-title">👤 Investigator Workload</div>', unsafe_allow_html=True)
        inv_load: dict[str, int] = {}
        for c in CASES:
            if c["status"] in ("ACTIVE", "CONTAINED"):
                inv_load[c["investigator"]] = inv_load.get(c["investigator"], 0) + 1
        fig_inv = go.Figure(go.Bar(
            y=list(inv_load.keys()), x=list(inv_load.values()), orientation="h",
            marker_color="#FFE600", marker_line_width=0,
            text=list(inv_load.values()), textposition="outside",
            textfont=dict(color="#FFFFFF", size=11),
            hovertemplate="%{y}: %{x} cases<extra></extra>",
        ))
        fig_inv.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=30, t=8, b=0), height=180, showlegend=False,
            xaxis=dict(tickfont=dict(color="#6B7280", size=10), gridcolor="#1A2035"),
            yaxis=dict(tickfont=dict(color="#D1D5DB", size=11)),
            bargap=0.35,
        )
        st.plotly_chart(fig_inv, use_container_width=True, config={"displayModeBar": False})

    with col_g:
        st.markdown('<div class="section-title">📂 Case Type Breakdown</div>', unsafe_allow_html=True)
        case_types: dict[str, int] = {}
        for c in CASES:
            ct = c["type"].split("/")[0].strip()
            case_types[ct] = case_types.get(ct, 0) + 1
        fig_ct = go.Figure(go.Bar(
            y=list(case_types.keys()), x=list(case_types.values()), orientation="h",
            marker_color="#1890FF", marker_line_width=0,
            text=list(case_types.values()), textposition="outside",
            textfont=dict(color="#FFFFFF", size=11),
            hovertemplate="%{y}: %{x} cases<extra></extra>",
        ))
        fig_ct.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=30, t=8, b=0), height=180, showlegend=False,
            xaxis=dict(tickfont=dict(color="#6B7280", size=10), gridcolor="#1A2035"),
            yaxis=dict(tickfont=dict(color="#D1D5DB", size=11)),
            bargap=0.35,
        )
        st.plotly_chart(fig_ct, use_container_width=True, config={"displayModeBar": False})
