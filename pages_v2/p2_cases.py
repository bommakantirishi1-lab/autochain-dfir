"""
Case Command Center — Rich card-based investigation management.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.graph_objects as go

from data_v2.mock_data import CASES, THREAT_ACTORS


def _risk_badge(risk: str) -> str:
    return f'<span class="badge badge-{risk.lower()}">{risk}</span>'

def _status_badge(status: str) -> str:
    return f'<span class="badge badge-{status.lower()}">{status}</span>'

def _conf_bar(conf: int, color: str = "yellow") -> str:
    return f"""
    <div style="display:flex;align-items:center;gap:8px">
        <div class="ey-prog-wrap" style="flex:1;height:5px">
            <div class="ey-prog-fill {color}" style="width:{conf}%"></div>
        </div>
        <span style="font-size:11px;color:#9CA3AF;width:36px;text-align:right">{conf}%</span>
    </div>
    """


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📁 Case Command Center</div>
        <div class="page-subtitle">Active investigations · Select a case to view details</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter bar ─────────────────────────────────────────────────────────
    f1, f2, f3, f4, f5 = st.columns([2, 1.2, 1.2, 1.2, 1.2])
    with f1:
        search = st.text_input("🔍 Search cases", placeholder="Case ID, title, client, tags…", label_visibility="collapsed")
    with f2:
        risk_filter = st.selectbox("Risk", ["All Risks", "CRITICAL", "HIGH", "MEDIUM", "LOW"], label_visibility="collapsed")
    with f3:
        status_filter = st.selectbox("Status", ["All Status", "ACTIVE", "CONTAINED", "RESOLVED", "CLOSED"], label_visibility="collapsed")
    with f4:
        type_filter = st.selectbox("Type", ["All Types", "Ransomware", "APT / Espionage", "BEC / Financial Fraud", "Insider Threat", "APT / Financial Crime", "Financial Crime / POS", "Phishing / Credential Theft", "APT / Living-off-the-Land"], label_visibility="collapsed")
    with f5:
        inv_filter = st.selectbox("Investigator", ["All Investigators", "J. Nakamura", "S. Okonkwo", "M. Rodriguez", "A. Petrov"], label_visibility="collapsed")

    # ── Filter logic ───────────────────────────────────────────────────────
    filtered = CASES
    if search:
        q = search.lower()
        filtered = [c for c in filtered if q in c["id"].lower() or q in c["title"].lower()
                    or q in (c["client"] or "").lower() or any(q in t for t in c["tags"])]
    if risk_filter != "All Risks":
        filtered = [c for c in filtered if c["risk"] == risk_filter]
    if status_filter != "All Status":
        filtered = [c for c in filtered if c["status"] == status_filter]
    if type_filter != "All Types":
        filtered = [c for c in filtered if c["type"] == type_filter]
    if inv_filter != "All Investigators":
        filtered = [c for c in filtered if c["investigator"] == inv_filter]

    # ── Summary bar ────────────────────────────────────────────────────────
    total_ev = sum(c["evidence_count"] for c in filtered)
    total_ioc = sum(c["ioc_count"] for c in filtered)
    total_ev_tl = sum(c["timeline_events"] for c in filtered)
    st.markdown(f"""
    <div style="display:flex;gap:20px;padding:10px 0 14px;border-bottom:1px solid #1F2937;margin-bottom:16px">
        <span style="font-size:12px;color:#6B7280">{len(filtered)} cases shown</span>
        <span style="font-size:12px;color:#6B7280">📦 {total_ev:,} evidence items</span>
        <span style="font-size:12px;color:#6B7280">🎯 {total_ioc:,} IOCs</span>
        <span style="font-size:12px;color:#6B7280">⏱ {total_ev_tl:,} timeline events</span>
    </div>
    """, unsafe_allow_html=True)

    if not filtered:
        st.markdown('<div style="text-align:center;padding:40px;color:#6B7280">No cases match your filters.</div>', unsafe_allow_html=True)
        return

    # ── Case cards ─────────────────────────────────────────────────────────
    selected_id = st.session_state.get("selected_case_id")

    for case in filtered:
        rc = case["risk"].lower()
        sc = case["status"].lower()
        is_selected = (case["id"] == selected_id)
        card_class = "case-card selected" if is_selected else "case-card"

        # Attribution confidence color
        conf_color = "red" if case["attribution_confidence"] >= 80 else ("orange" if case["attribution_confidence"] >= 60 else "blue")

        # TTP tags
        ttp_html = "".join(f'<span class="tag technique">{t}</span>' for t in case["ttps"][:5])
        if len(case["ttps"]) > 5:
            ttp_html += f'<span class="tag" style="color:#6B7280">+{len(case["ttps"])-5}</span>'

        tag_html = "".join(f'<span class="tag">{t}</span>' for t in case["tags"][:4])

        # Click to expand
        with st.expander(f"", expanded=is_selected):
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
                    <div>
                        <div class="case-id">{case['id']} · {case['type']} · 📅 {case['incident_date']}</div>
                        <div class="case-title">{case['title']}</div>
                    </div>
                    <div style="display:flex;gap:6px;flex-shrink:0;margin-left:12px">
                        {_risk_badge(case['risk'])}
                        {_status_badge(case['status'])}
                    </div>
                </div>

                <div style="font-size:12px;color:#9CA3AF;line-height:1.5;margin-bottom:10px">
                    {case['description']}
                </div>

                <div style="margin-bottom:10px">{tag_html}</div>

                <div class="case-stats">
                    <div class="case-stat">
                        <div class="case-stat-value">{case['evidence_count']}</div>
                        <div class="case-stat-label">Evidence</div>
                    </div>
                    <div class="case-stat">
                        <div class="case-stat-value">{case['ioc_count']}</div>
                        <div class="case-stat-label">IOCs</div>
                    </div>
                    <div class="case-stat">
                        <div class="case-stat-value">{case['timeline_events']:,}</div>
                        <div class="case-stat-label">Events</div>
                    </div>
                    <div class="case-stat">
                        <div class="case-stat-value">{case['dwell_days']}d</div>
                        <div class="case-stat-label">Dwell</div>
                    </div>
                    <div class="case-stat">
                        <div class="case-stat-value">{case['affected_systems']:,}</div>
                        <div class="case-stat-label">Systems</div>
                    </div>
                </div>

                <div style="margin-top:14px;padding-top:12px;border-top:1px solid #1F2937">
                    <div style="display:flex;gap:32px;flex-wrap:wrap">
                        <div>
                            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px">Attribution</div>
                            <div style="font-size:13px;font-weight:600;color:#E5E7EB">{case['attribution']}</div>
                            {_conf_bar(case['attribution_confidence'], conf_color)}
                        </div>
                        <div>
                            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px">Investigator</div>
                            <div style="font-size:13px;color:#E5E7EB">{case['investigator']}</div>
                        </div>
                        <div>
                            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px">Client</div>
                            <div style="font-size:13px;color:#E5E7EB">{case['client']}</div>
                        </div>
                        <div>
                            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px">Damage</div>
                            <div style="font-size:13px;color:#FF7875">{case['damage']}</div>
                        </div>
                    </div>
                </div>

                <div style="margin-top:12px">
                    <div style="font-size:10px;color:#6B7280;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.7px">Detected ATT&CK Techniques</div>
                    {ttp_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            ba, bb, bc, bd = st.columns(4)
            with ba:
                if st.button("⏱ View Timeline", key=f"tl_{case['id']}", use_container_width=True):
                    st.session_state["selected_case_id"] = case["id"]
                    st.session_state["_page_module"] = "p3_timeline"
                    st.rerun()
            with bb:
                if st.button("🗄 Evidence", key=f"ev_{case['id']}", use_container_width=True):
                    st.session_state["selected_case_id"] = case["id"]
                    st.session_state["_page_module"] = "p4_evidence"
                    st.rerun()
            with bc:
                if st.button("🎯 IOC Intel", key=f"ioc_{case['id']}", use_container_width=True):
                    st.session_state["selected_case_id"] = case["id"]
                    st.session_state["_page_module"] = "p6_ioc"
                    st.rerun()
            with bd:
                if st.button("📄 Generate Report", key=f"rpt_{case['id']}", use_container_width=True, type="primary"):
                    st.session_state["selected_case_id"] = case["id"]
                    st.session_state["_page_module"] = "p8_reports"
                    st.rerun()

    # ── Threat actor summary ───────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🕵 Attributed Threat Actors</div>', unsafe_allow_html=True)
    ta_cols = st.columns(len(THREAT_ACTORS))
    for col, actor in zip(ta_cols, THREAT_ACTORS):
        with col:
            conf = actor["confidence"]
            prog_col = "red" if conf >= 80 else ("orange" if conf >= 60 else "blue")
            st.markdown(f"""
            <div class="ey-card" style="text-align:center;padding:16px">
                <div style="font-size:13px;font-weight:700;color:#FFFFFF;margin-bottom:3px">{actor['name']}</div>
                <div style="font-size:10px;color:#6B7280;margin-bottom:8px">{actor['type']}</div>
                <span class="tag actor">{actor['origin']}</span>
                <div style="margin:10px 0">
                    <div style="font-size:22px;font-weight:700;color:{actor['color']}">{conf}%</div>
                    <div style="font-size:10px;color:#6B7280">Attribution Confidence</div>
                </div>
                <div class="ey-prog-wrap">
                    <div class="ey-prog-fill {prog_col}" style="width:{conf}%"></div>
                </div>
                <div style="font-size:10px;color:#6B7280;margin-top:8px">
                    {len(actor['cases'])} case · {actor['ttps_matched']} TTPs matched
                </div>
            </div>
            """, unsafe_allow_html=True)
