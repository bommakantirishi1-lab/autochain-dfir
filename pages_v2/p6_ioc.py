"""
IOC Intelligence Center — Enriched indicator analysis.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.graph_objects as go

from data_v2.mock_data import IOCS, CASES


_TYPE_ICONS = {
    "IP_ADDRESS": "🌐", "DOMAIN": "🔗", "URL": "🌍",
    "FILE_HASH_SHA256": "#️⃣", "FILE_HASH_MD5": "#️⃣",
    "EMAIL": "📧", "REGISTRY_KEY": "🔑",
}


def _score_color(score: float) -> str:
    if score >= 9: return "#FF4D4F"
    if score >= 7: return "#FA8C16"
    if score >= 5: return "#FADB14"
    return "#52C41A"


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🌐 IOC Intelligence Center</div>
        <div class="page-subtitle">Threat intel enrichment · VirusTotal + AbuseIPDB + EY TI Feed</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filters ────────────────────────────────────────────────────────────
    f1, f2, f3, f4 = st.columns([2, 1.5, 1.5, 1.5])
    with f1:
        search = st.text_input("🔍 Search IOCs", placeholder="IP, domain, hash, tag…", label_visibility="collapsed")
    with f2:
        case_options = ["All Cases"] + [c["id"] for c in CASES]
        case_sel = st.selectbox("Case", case_options, label_visibility="collapsed",
                                index=1 if st.session_state.get("selected_case_id") else 0)
    with f3:
        type_opts = ["All Types", "IP_ADDRESS", "DOMAIN", "URL", "FILE_HASH_SHA256", "FILE_HASH_MD5", "EMAIL", "REGISTRY_KEY"]
        type_sel = st.selectbox("Type", type_opts, label_visibility="collapsed")
    with f4:
        malicious_only = st.checkbox("🔴 Malicious only", value=False)

    # ── Filter ─────────────────────────────────────────────────────────────
    iocs = IOCS
    if search:
        q = search.lower()
        iocs = [i for i in iocs if q in i["value"].lower() or any(q in t for t in i["tags"])]
    if case_sel != "All Cases":
        iocs = [i for i in iocs if i["case_id"] == case_sel]
    if type_sel != "All Types":
        iocs = [i for i in iocs if i["type"] == type_sel]
    if malicious_only:
        iocs = [i for i in iocs if i["is_malicious"]]

    iocs = sorted(iocs, key=lambda x: x["threat_score"], reverse=True)

    # ── Summary stats ──────────────────────────────────────────────────────
    total = len(iocs)
    malicious = sum(1 for i in iocs if i["is_malicious"])
    avg_score = sum(i["threat_score"] for i in iocs) / max(total, 1)
    vt_detected = sum(1 for i in iocs if i.get("vt_detections", 0) > 0)

    s1, s2, s3, s4 = st.columns(4)
    for col, (lbl, val, color) in zip(
        [s1, s2, s3, s4],
        [("Total IOCs",        total,                      "#FFFFFF"),
         ("🔴 Malicious",      malicious,                  "#FF4D4F"),
         ("VT Detected",       vt_detected,                "#FA8C16"),
         ("Avg Threat Score",  f"{avg_score:.1f}/10",      _score_color(avg_score))],
    ):
        col.markdown(f"""
        <div class="ey-card" style="text-align:center;padding:14px">
            <div style="font-size:11px;color:#6B7280">{lbl}</div>
            <div style="font-size:26px;font-weight:700;color:{color}">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Charts row ─────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    chart1, chart2 = st.columns([1, 1])

    with chart1:
        st.markdown('<div class="section-title">📊 IOC Type Breakdown</div>', unsafe_allow_html=True)
        type_counts: dict[str, int] = {}
        for i in IOCS:
            t = i["type"].replace("FILE_HASH_", "").replace("_", " ").title()
            type_counts[t] = type_counts.get(t, 0) + 1
        fig1 = go.Figure(go.Pie(
            labels=list(type_counts.keys()), values=list(type_counts.values()),
            hole=0.5,
            marker_colors=["#FF4D4F","#FA8C16","#FADB14","#52C41A","#1890FF","#722ED1","#13C2C2"],
            textinfo="percent+label", textfont=dict(color="white", size=10),
            hovertemplate="%{label}: %{value}<extra></extra>",
        ))
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=200, margin=dict(l=0,r=0,t=0,b=0), showlegend=False,
        )
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    with chart2:
        st.markdown('<div class="section-title">🌡 Threat Score Distribution</div>', unsafe_allow_html=True)
        score_buckets = {"9-10 (Critical)": 0, "7-9 (High)": 0, "5-7 (Medium)": 0, "0-5 (Low)": 0}
        bucket_colors = ["#FF4D4F", "#FA8C16", "#FADB14", "#52C41A"]
        for i in IOCS:
            s = i["threat_score"]
            if s >= 9: score_buckets["9-10 (Critical)"] += 1
            elif s >= 7: score_buckets["7-9 (High)"] += 1
            elif s >= 5: score_buckets["5-7 (Medium)"] += 1
            else: score_buckets["0-5 (Low)"] += 1
        fig2 = go.Figure(go.Bar(
            x=list(score_buckets.keys()), y=list(score_buckets.values()),
            marker_color=bucket_colors, marker_line_width=0,
            text=list(score_buckets.values()), textposition="outside",
            textfont=dict(color="white", size=11),
            hovertemplate="%{x}: %{y}<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=200, margin=dict(l=0,r=0,t=8,b=0), showlegend=False,
            xaxis=dict(tickfont=dict(color="#9CA3AF", size=10), gridcolor="#1A2035"),
            yaxis=dict(tickfont=dict(color="#6B7280", size=10), gridcolor="#1A2035"),
            bargap=0.3,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ── IOC list ───────────────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">🎯 IOC Details — {len(iocs)} indicators</div>', unsafe_allow_html=True)

    if not iocs:
        st.markdown('<div style="text-align:center;padding:30px;color:#6B7280">No IOCs match your filters.</div>', unsafe_allow_html=True)
        return

    for ioc in iocs:
        score_color = _score_color(ioc["threat_score"])
        mal_badge = '<span class="badge badge-critical" style="font-size:9px">MALICIOUS</span>' if ioc["is_malicious"] else '<span class="badge badge-low" style="font-size:9px">CLEAN</span>'
        icon = _TYPE_ICONS.get(ioc["type"], "🔍")
        tag_html = "".join(f'<span class="tag ioc">{t}</span>' for t in ioc["tags"])

        # VT bar
        vt_pct = int(ioc.get("vt_detections", 0) / max(ioc.get("vt_total", 1), 1) * 100)
        vt_color = "#FF4D4F" if vt_pct > 60 else ("#FA8C16" if vt_pct > 30 else "#52C41A")

        # Abuse confidence bar
        abuse_conf = ioc.get("abuse_confidence", 0)
        abuse_color = "#FF4D4F" if abuse_conf > 80 else ("#FA8C16" if abuse_conf > 50 else "#52C41A")

        country_str = f"🌍 {ioc['country']}" if ioc.get("country") else ""
        asn_str = f"  ·  {ioc['asn']}" if ioc.get("asn") else ""

        with st.expander(f"{icon}  {ioc['type'].replace('_',' ').title()}  ·  {ioc['value'][:60]}{'…' if len(ioc['value'])>60 else ''}"):
            col_l, col_r = st.columns([2, 1])
            with col_l:
                st.markdown(f"""
                <div style="background:#0E1117;border:1px solid #1F2937;border-radius:8px;padding:14px">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
                        <div>
                            <div style="font-size:10px;color:#6B7280;margin-bottom:3px">{ioc['id']} · {ioc['type'].replace('_',' ')}</div>
                            <div style="font-family:monospace;font-size:13px;color:#E5E7EB;word-break:break-all">{ioc['value']}</div>
                            <div style="font-size:11px;color:#6B7280;margin-top:4px">{country_str}{asn_str}</div>
                        </div>
                        <div style="display:flex;gap:6px;flex-shrink:0">
                            {mal_badge}
                        </div>
                    </div>

                    <div style="margin:8px 0">{tag_html}</div>

                    <div style="margin-top:10px;display:grid;grid-template-columns:1fr 1fr;gap:8px">
                        <div>
                            <div style="font-size:10px;color:#6B7280;margin-bottom:3px">VirusTotal ({ioc.get('vt_detections',0)}/{ioc.get('vt_total',93)})</div>
                            <div class="ey-prog-wrap"><div class="ey-prog-fill" style="width:{vt_pct}%;background:{vt_color}"></div></div>
                            <div style="font-size:10px;color:{vt_color};margin-top:2px">{vt_pct}% engines detected</div>
                        </div>
                        <div>
                            <div style="font-size:10px;color:#6B7280;margin-bottom:3px">AbuseIPDB Confidence</div>
                            <div class="ey-prog-wrap"><div class="ey-prog-fill" style="width:{abuse_conf}%;background:{abuse_color}"></div></div>
                            <div style="font-size:10px;color:{abuse_color};margin-top:2px">{abuse_conf}% abuse confidence</div>
                        </div>
                    </div>

                    <div style="margin-top:8px">
                        <div style="font-size:10px;color:#6B7280">First seen: <span style="color:#9CA3AF;font-family:monospace">{ioc['first_seen'][:19].replace('T',' ')}</span>
                        · Case: <span class="tag" style="font-size:9px">{ioc['case_id']}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_r:
                st.markdown(f"""
                <div style="text-align:center;padding:20px;background:#0E1117;border:1px solid #1F2937;border-radius:8px;height:100%">
                    <div style="font-size:11px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:8px">Threat Score</div>
                    <div style="font-size:52px;font-weight:700;color:{score_color};line-height:1">{ioc['threat_score']:.1f}</div>
                    <div style="font-size:12px;color:#6B7280">/ 10.0</div>
                    <div style="margin-top:14px">
                        <div class="ey-prog-wrap" style="height:8px">
                            <div class="ey-prog-fill" style="width:{ioc['threat_score']*10:.0f}%;background:{score_color}"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
