"""
Evidence Chain of Custody — Visual lifecycle timeline with integrity verification.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from data_v2.mock_data import EVIDENCE, CASES


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🗄 Evidence Chain of Custody</div>
        <div class="page-subtitle">Court-admissible integrity verification · ACPO / ISO 27037 compliant</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Case selector ──────────────────────────────────────────────────────
    c1, c2 = st.columns([2, 2])
    with c1:
        case_options = [c["id"] for c in CASES]
        selected_case = st.selectbox("Case", case_options,
                                     index=0 if not st.session_state.get("selected_case_id")
                                     else (case_options.index(st.session_state["selected_case_id"])
                                           if st.session_state["selected_case_id"] in case_options else 0),
                                     label_visibility="collapsed")
    with c2:
        st.markdown("""
        <div style="display:flex;gap:16px;align-items:center;padding-top:6px">
            <div style="display:flex;align-items:center;gap:6px">
                <div style="width:10px;height:10px;border-radius:50%;background:#FFE600"></div>
                <span style="font-size:11px;color:#6B7280">In Progress</span>
            </div>
            <div style="display:flex;align-items:center;gap:6px">
                <div style="width:10px;height:10px;border-radius:50%;background:#52C41A"></div>
                <span style="font-size:11px;color:#6B7280">Verified</span>
            </div>
            <div style="display:flex;align-items:center;gap:6px">
                <div style="width:10px;height:10px;border-radius:50%;background:#2A3142;border:2px solid #6B7280"></div>
                <span style="font-size:11px;color:#6B7280">Pending</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Filter evidence for selected case ──────────────────────────────────
    case_evidence = [ev for ev in EVIDENCE if ev["case_id"] == selected_case]

    if not case_evidence:
        st.markdown(f'<div style="text-align:center;padding:40px;color:#6B7280">No evidence found for {selected_case}</div>', unsafe_allow_html=True)
        return

    # ── Summary stats ──────────────────────────────────────────────────────
    total_items = len(case_evidence)
    intact = sum(1 for e in case_evidence if e["integrity"])
    total_events = sum(len(e["custody_chain"]) for e in case_evidence)
    chain_confidence = int(intact / max(total_items, 1) * 100)

    s1, s2, s3, s4 = st.columns(4)
    for col, (lbl, val, color) in zip(
        [s1, s2, s3, s4],
        [("Evidence Items", total_items, "#FFE600"),
         ("✅ Integrity Verified", intact, "#52C41A"),
         ("Custody Events", total_events, "#1890FF"),
         ("Chain Confidence", f"{chain_confidence}%", "#52C41A" if chain_confidence == 100 else "#FA8C16")],
    ):
        col.markdown(f"""
        <div class="ey-card" style="text-align:center;padding:14px">
            <div style="font-size:11px;color:#6B7280">{lbl}</div>
            <div style="font-size:26px;font-weight:700;color:{color}">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Evidence items ─────────────────────────────────────────────────────
    for ev_item in case_evidence:
        integrity_ok = ev_item["integrity"]
        integrity_label = "✅ INTEGRITY VERIFIED" if integrity_ok else "❌ INTEGRITY FAILED"
        integrity_class = "" if integrity_ok else "fail"

        with st.expander(f"{ev_item['icon']}  {ev_item['id']} — {ev_item['description']}", expanded=True):
            col_a, col_b = st.columns([1.2, 1])

            with col_a:
                # Metadata panel
                st.markdown(f"""
                <div class="ey-card">
                    <div class="card-title">{ev_item['icon']} {ev_item['type']}</div>
                    <div class="card-subtitle" style="margin-bottom:12px">{ev_item['description']}</div>

                    <div class="metric-row">
                        <span class="metric-key">Evidence ID</span>
                        <span class="metric-val" style="font-family:monospace">{ev_item['id']}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-key">Size</span>
                        <span class="metric-val">{ev_item['size']}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-key">Acquisition Tool</span>
                        <span class="metric-val">{ev_item['tool']}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-key">Acquired By</span>
                        <span class="metric-val">{ev_item['acquired_by']}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-key">Acquired At</span>
                        <span class="metric-val">{ev_item['acquired_at'][:19].replace('T',' ')}</span>
                    </div>

                    <div style="margin-top:12px">
                        <div style="font-size:10px;color:#6B7280;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.7px">SHA-256 Hash</div>
                        <div class="hash-display">SHA256: {ev_item['sha256']}</div>
                        <div class="hash-display" style="margin-top:4px">MD5: {ev_item['md5']}</div>
                    </div>

                    <div class="integrity-badge {integrity_class}" style="margin-top:12px">
                        {integrity_label}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                # Chain of custody timeline
                st.markdown('<div style="font-size:13px;font-weight:600;color:#D1D5DB;margin-bottom:14px">📜 Chain of Custody</div>', unsafe_allow_html=True)
                st.markdown('<div class="custody-timeline">', unsafe_allow_html=True)

                for i, step in enumerate(ev_item["custody_chain"]):
                    is_last = (i == len(ev_item["custody_chain"]) - 1)
                    dot_class = "done" if step["action"] in ("ACQUIRED", "HASHED", "TRANSFERRED", "ANALYZED", "ARCHIVED") and step["verified"] else ("verified" if step["verified"] else "pending")
                    ts_disp = step["ts"][:19].replace("T", " ")

                    after_style = "" if is_last else ""
                    st.markdown(f"""
                    <div class="custody-step">
                        <div class="custody-dot {dot_class}">{step['icon']}</div>
                        <div class="custody-content">
                            <div class="custody-action">{step['action']}</div>
                            <div class="custody-meta">
                                <strong style="color:#E5E7EB">{step['by']}</strong> · {step['role']} · <span style="font-family:monospace">{ts_disp}</span>
                            </div>
                            <div class="custody-meta" style="margin-top:3px;color:#9CA3AF">{step['note']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # Chain confidence gauge
                n_verified = sum(1 for s in ev_item["custody_chain"] if s["verified"])
                pct = int(n_verified / len(ev_item["custody_chain"]) * 100)
                st.markdown(f"""
                <div style="margin-top:12px;padding:12px;background:#0E1117;border-radius:8px;border:1px solid #1F2937">
                    <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                        <span style="font-size:11px;color:#6B7280">Chain Confidence</span>
                        <span style="font-size:13px;font-weight:700;color:{'#52C41A' if pct==100 else '#FA8C16'}">{pct}%</span>
                    </div>
                    <div class="ey-prog-wrap">
                        <div class="ey-prog-fill {'green' if pct==100 else 'orange'}" style="width:{pct}%"></div>
                    </div>
                    <div style="font-size:10px;color:#6B7280;margin-top:5px">
                        {n_verified}/{len(ev_item['custody_chain'])} custody events verified · {'✅ Court-admissible' if pct==100 else '⚠ Review required'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Legal disclaimer ───────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0E1117;border:1px solid #1F2937;border-radius:8px;padding:14px 16px">
        <div style="font-size:11px;color:#6B7280;line-height:1.6">
            <strong style="color:#9CA3AF">⚖️ Legal Notice:</strong>
            All digital evidence was acquired, handled, and maintained in accordance with ACPO Good Practice Guide for Digital Evidence (v5),
            ISO/IEC 27037:2012 (Identification, Collection, Acquisition and Preservation of Digital Evidence),
            and EY Forensic & Integrity Services Evidence Handling Procedures.
            SHA-256 hash verification confirms bit-for-bit integrity at all chain of custody transfer points.
            This evidence is suitable for presentation in civil and criminal proceedings.
        </div>
    </div>
    """, unsafe_allow_html=True)
