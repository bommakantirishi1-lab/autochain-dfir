"""
MITRE ATT&CK Center — Interactive heatmap with technique details.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.graph_objects as go

from data_v2.mock_data import MITRE_COVERAGE, TACTIC_COLORS, CASES


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🛡 MITRE ATT&CK Center</div>
        <div class="page-subtitle">Adversary behavior mapping · Enterprise ATT&CK v14</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary stats ──────────────────────────────────────────────────────
    total_techniques = sum(len(v) for v in MITRE_COVERAGE.values())
    total_detections = sum(t["count"] for tactics in MITRE_COVERAGE.values() for t in tactics)
    tactics_covered = len(MITRE_COVERAGE)
    avg_conf = sum(t["conf"] for tactics in MITRE_COVERAGE.values() for t in tactics) / max(total_techniques, 1)

    s1, s2, s3, s4 = st.columns(4)
    for col, (lbl, val, color) in zip(
        [s1, s2, s3, s4],
        [("Techniques Detected",  total_techniques,         "#FF4D4F"),
         ("Total Detections",     total_detections,         "#FA8C16"),
         ("Tactics Covered",      f"{tactics_covered}/12",  "#FFE600"),
         ("Avg Confidence",       f"{avg_conf:.0f}%",       "#52C41A")],
    ):
        col.markdown(f"""
        <div class="ey-card" style="text-align:center;padding:14px">
            <div style="font-size:11px;color:#6B7280">{lbl}</div>
            <div style="font-size:26px;font-weight:700;color:{color}">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── ATT&CK Heatmap (Plotly) ────────────────────────────────────────────
    st.markdown('<div class="section-title">🔥 ATT&CK Technique Heatmap</div>', unsafe_allow_html=True)

    tactics_ordered = list(MITRE_COVERAGE.keys())
    max_per_tactic = max(len(v) for v in MITRE_COVERAGE.values())

    z_matrix: list[list[float]] = []
    text_matrix: list[list[str]] = []
    hover_matrix: list[list[str]] = []

    for tactic in tactics_ordered:
        techniques = MITRE_COVERAGE[tactic]
        row_z, row_text, row_hover = [], [], []
        for i in range(max_per_tactic):
            if i < len(techniques):
                t = techniques[i]
                row_z.append(t["count"])
                row_text.append(f"<b>{t['id']}</b><br>{t['name'][:18]}{'…' if len(t['name'])>18 else ''}")
                row_hover.append(f"<b>{t['id']}: {t['name']}</b><br>Detections: {t['count']}<br>Confidence: {t['conf']}%<br>Cases: {', '.join(t['cases'][:3])}")
            else:
                row_z.append(0)
                row_text.append("")
                row_hover.append("")
        z_matrix.append(row_z)
        text_matrix.append(row_text)
        hover_matrix.append(row_hover)

    fig = go.Figure(go.Heatmap(
        z=z_matrix,
        x=[f"Slot {i+1}" for i in range(max_per_tactic)],
        y=tactics_ordered,
        colorscale=[[0,"#1A1F2B"],[0.01,"#1A2035"],[0.2,"rgba(114,46,209,0.4)"],
                    [0.5,"rgba(250,140,22,0.6)"],[1.0,"rgba(255,77,79,0.9)"]],
        text=text_matrix,
        texttemplate="%{text}",
        textfont=dict(size=9, color="white"),
        hovertext=hover_matrix,
        hovertemplate="%{hovertext}<extra></extra>",
        showscale=False,
        zmin=0, zmax=6,
        xgap=3, ygap=3,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(
            tickfont=dict(color="#D1D5DB", size=11),
            side="left",
        ),
        font=dict(color="white"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Tactic bar chart ───────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    col_bar, col_detail = st.columns([1, 1.5])

    with col_bar:
        st.markdown('<div class="section-title">📊 Detection Coverage by Tactic</div>', unsafe_allow_html=True)
        tactic_totals = [(t, sum(x["count"] for x in MITRE_COVERAGE[t])) for t in tactics_ordered]
        fig2 = go.Figure(go.Bar(
            y=[t for t, _ in tactic_totals],
            x=[v for _, v in tactic_totals],
            orientation="h",
            marker_color=[TACTIC_COLORS.get(t, "#6B7280") for t, _ in tactic_totals],
            marker_line_width=0,
            text=[v for _, v in tactic_totals],
            textposition="outside",
            textfont=dict(color="white", size=10),
            hovertemplate="%{y}: %{x} detections<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=380, margin=dict(l=0, r=30, t=0, b=0), showlegend=False,
            xaxis=dict(tickfont=dict(color="#6B7280", size=10), gridcolor="#1A2035"),
            yaxis=dict(tickfont=dict(color="#D1D5DB", size=10)),
            bargap=0.25,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with col_detail:
        st.markdown('<div class="section-title">🔍 Technique Detail Browser</div>', unsafe_allow_html=True)
        sel_tactic = st.selectbox("Select tactic", tactics_ordered, label_visibility="collapsed")
        techniques = MITRE_COVERAGE.get(sel_tactic, [])
        for tech in techniques:
            conf_color = "#52C41A" if tech["conf"] >= 90 else ("#FA8C16" if tech["conf"] >= 70 else "#6B7280")
            color = TACTIC_COLORS.get(sel_tactic, "#6B7280")
            case_badges = "".join(f'<span class="tag" style="font-size:9px">{c}</span>' for c in tech["cases"])
            st.markdown(f"""
            <div style="padding:12px;border:1px solid #2A3142;border-radius:8px;margin-bottom:8px;
                        background:#141922;border-left:3px solid {color}">
                <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div>
                        <span class="tag technique" style="font-size:11px">{tech['id']}</span>
                        <div style="font-size:13px;font-weight:600;color:#FFFFFF;margin-top:5px">{tech['name']}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:20px;font-weight:700;color:{color}">{tech['count']}</div>
                        <div style="font-size:10px;color:#6B7280">detections</div>
                    </div>
                </div>
                <div style="margin-top:8px">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                        <span style="font-size:11px;color:#6B7280">Confidence:</span>
                        <div class="ey-prog-wrap" style="flex:1;height:4px">
                            <div class="ey-prog-fill" style="width:{tech['conf']}%;background:{conf_color}"></div>
                        </div>
                        <span style="font-size:11px;color:{conf_color};font-weight:600">{tech['conf']}%</span>
                    </div>
                    <div style="font-size:10px;color:#6B7280">Cases: {case_badges}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Top techniques ─────────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Top 10 Most Observed Techniques Across All Cases</div>', unsafe_allow_html=True)

    all_techs = []
    for tactic, techniques in MITRE_COVERAGE.items():
        for t in techniques:
            all_techs.append({**t, "tactic": tactic})
    top10 = sorted(all_techs, key=lambda x: x["count"], reverse=True)[:10]

    col_names = st.columns(10)
    for col, tech in zip(col_names, top10):
        color = TACTIC_COLORS.get(tech["tactic"], "#6B7280")
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:10px 6px;background:#141922;border-radius:8px;
                        border:1px solid #2A3142;border-top:3px solid {color}">
                <div style="font-size:9px;font-family:monospace;color:{color};margin-bottom:3px">{tech['id']}</div>
                <div style="font-size:10px;color:#9CA3AF;margin-bottom:6px;line-height:1.2">{tech['name'][:20]}</div>
                <div style="font-size:18px;font-weight:700;color:#FFFFFF">{tech['count']}</div>
                <div style="font-size:9px;color:#6B7280">cases</div>
            </div>
            """, unsafe_allow_html=True)
