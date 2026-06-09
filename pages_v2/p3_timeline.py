"""
Supertimeline — ATT&CK-aligned interactive timeline with narrative.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from data_v2.mock_data import TIMELINE_EVENTS, TACTIC_COLORS, CASES


_PHASE_ORDER = [
    "Initial Access", "Execution", "Persistence", "Privilege Escalation",
    "Defense Evasion", "Credential Access", "Discovery",
    "Lateral Movement", "Collection", "Command and Control", "Exfiltration", "Impact",
]

_NARRATIVE = """
**Phase 1 — Initial Access** *(T+0h)*
Attacker sent a highly targeted spearphishing email impersonating the HR department of Meridian Healthcare. A malicious `.xlsx` attachment exploited CVE-2024-21413 to achieve remote code execution on WORKSTATION-047. Simultaneously, a VPN account belonging to B. Chen was accessed from Bulgaria after a successful MFA fatigue attack (11 push notifications).

**Phase 2 — Execution & Evasion** *(T+0.3h)*
An encoded PowerShell stager was executed, downloading the ALPHV loader from the C2 infrastructure at `185.220.101.47`. AMSI was bypassed by patching `AmsiScanBuffer` in memory, rendering Windows Defender ineffective.

**Phase 3 — Persistence** *(T+0.5h)*
Two persistence mechanisms were established: a registry autorun key pointing to `svchost32.exe`, and a daily scheduled task disguised as 'WindowsDefenderUpdate'. Both survived reboot and operated under SYSTEM context.

**Phase 4 — Privilege Escalation & Credential Theft** *(T+0.8h)*
The attacker leveraged `SeImpersonatePrivilege` to impersonate the SYSTEM token. Mimikatz was executed against LSASS memory, extracting 6 credential sets including domain administrator hashes.

**Phase 5 — Lateral Movement to Domain Controller** *(T+1.5h)*
Using a Pass-the-Hash attack with the harvested administrator NTLM hash, the attacker authenticated to DC-MERIDIAN-01. A DCSync attack dumped the entire Active Directory credential store — 847 NTLM hashes including the `krbtgt` account, enabling Golden Ticket creation.

**Phase 6 — Infrastructure Expansion** *(T+2.5h)*
A Cobalt Strike beacon was installed as a Windows service on the Domain Controller, establishing persistent HTTPS C2 communications with `194.165.16.98:443` using an Amazon-impersonating TLS certificate.

**Phase 7 — Data Staging & Exfiltration** *(T+9h)*
Patient records were staged and archived using 7-Zip (AES-256) across 14 hospital servers — 780,000 records totaling 2.3 GB. The archive was exfiltrated over the Cobalt Strike C2 channel over 42 minutes.

**Phase 8 — Ransomware Deployment** *(T+11h)*
Shadow copies were deleted via GPO push (`vssadmin delete shadows /all`) across all 847 domain-joined systems. ALPHV BlackCat ransomware was deployed and began encrypting simultaneously at 03:00 UTC, maximizing impact before staff arrival.
"""


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">⏱ Supertimeline</div>
        <div class="page-subtitle">ATT&CK-aligned unified event timeline · 4 artifact sources merged</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter bar ─────────────────────────────────────────────────────────
    fc1, fc2, fc3, fc4 = st.columns([1.5, 1.5, 1.5, 1])
    with fc1:
        case_options = ["All Cases"] + [c["id"] for c in CASES]
        case_sel = st.selectbox("Case", case_options, label_visibility="collapsed",
                                index=1 if st.session_state.get("selected_case_id") else 0)
    with fc2:
        tactic_options = ["All Tactics"] + _PHASE_ORDER
        tactic_sel = st.selectbox("Tactic", tactic_options, label_visibility="collapsed")
    with fc3:
        host_options = ["All Hosts"] + sorted({e["host"] for e in TIMELINE_EVENTS})
        host_sel = st.selectbox("Host", host_options, label_visibility="collapsed")
    with fc4:
        anomaly_only = st.checkbox("🔴 Anomalies only", value=False)

    # ── Apply filters ──────────────────────────────────────────────────────
    events = TIMELINE_EVENTS
    if case_sel != "All Cases":
        events = [e for e in events if e["case_id"] == case_sel]
    if tactic_sel != "All Tactics":
        events = [e for e in events if e["tactic"] == tactic_sel]
    if host_sel != "All Hosts":
        events = [e for e in events if e["host"] == host_sel]
    if anomaly_only:
        events = [e for e in events if e["is_anomaly"]]

    # ── ATT&CK Kill Chain Progress ─────────────────────────────────────────
    st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)
    detected_tactics = {e["tactic"] for e in TIMELINE_EVENTS if e["case_id"] == (case_sel if case_sel != "All Cases" else "CASE-2024-001")}
    phase_cols = st.columns(len(_PHASE_ORDER))
    for col, phase in zip(phase_cols, _PHASE_ORDER):
        color = TACTIC_COLORS.get(phase, "#6B7280")
        detected = phase in detected_tactics
        opacity = "1" if detected else "0.2"
        short = phase.replace(" ", "\n").replace("Command and\nControl", "C2").replace("Privilege\nEscalation", "Priv.Esc").replace("Defense\nEvasion", "Def.Eva")
        col.markdown(f"""
        <div style="text-align:center;opacity:{opacity}">
            <div style="background:{color};height:4px;border-radius:2px;margin-bottom:3px"></div>
            <div style="font-size:8px;color:{color if detected else '#6B7280'};line-height:1.2;font-weight:{'700' if detected else '400'}">{phase.split()[0]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin:10px 0'></div>", unsafe_allow_html=True)

    # ── Statistics row ─────────────────────────────────────────────────────
    total = len(events)
    anomalies = sum(1 for e in events if e["is_anomaly"])
    tactics_seen = len({e["tactic"] for e in events})
    hosts_seen = len({e["host"] for e in events})
    avg_risk = sum(e["risk"] for e in events) / max(total, 1)

    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    for col, (lbl, val, color) in zip(
        [sc1, sc2, sc3, sc4, sc5],
        [("Total Events", total, "#FFFFFF"), ("🔴 Anomalies", anomalies, "#FF4D4F"),
         ("Tactics", tactics_seen, "#FA8C16"), ("Hosts", hosts_seen, "#1890FF"),
         ("Avg Risk", f"{avg_risk:.1f}/10", "#FFE600")],
    ):
        col.markdown(f"""
        <div class="ey-card" style="text-align:center;padding:12px 8px">
            <div style="font-size:11px;color:#6B7280">{lbl}</div>
            <div style="font-size:22px;font-weight:700;color:{color}">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Plotly scatter timeline ────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if events:
        df = pd.DataFrame(events)
        df["color"] = df["tactic"].map(TACTIC_COLORS).fillna("#6B7280")
        df["symbol"] = df["is_anomaly"].map({True: "diamond", False: "circle"})
        df["size"] = df["risk"] * 3 + 4

        fig = go.Figure()
        for tactic in _PHASE_ORDER:
            mask = df["tactic"] == tactic
            if not mask.any():
                continue
            sub = df[mask]
            fig.add_trace(go.Scatter(
                x=sub["ts"], y=sub["risk"],
                mode="markers",
                name=tactic,
                marker=dict(
                    size=sub["size"],
                    color=TACTIC_COLORS.get(tactic, "#6B7280"),
                    symbol=sub["symbol"],
                    opacity=0.85,
                    line=dict(width=1, color="rgba(255,255,255,0.2)"),
                ),
                text=sub["desc"],
                customdata=sub[["technique", "host", "user", "source"]].values,
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Technique: %{customdata[0]}<br>"
                    "Host: %{customdata[1]}<br>"
                    "User: %{customdata[2]}<br>"
                    "Source: %{customdata[3]}<br>"
                    "Risk: %{y:.1f}/10"
                    "<extra></extra>"
                ),
            ))

        # Threat threshold line
        fig.add_hline(y=8.0, line_dash="dot", line_color="#FF4D4F",
                      annotation_text="High Risk Threshold (8.0)", annotation_font_color="#FF4D4F",
                      annotation_font_size=10)

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0E1117",
            height=360,
            margin=dict(l=0, r=0, t=8, b=0),
            xaxis=dict(
                title=None, tickfont=dict(color="#6B7280", size=10),
                gridcolor="#1A2035", linecolor="#2A3142",
                showgrid=True,
            ),
            yaxis=dict(
                title="Risk Score", range=[0, 10.5],
                tickfont=dict(color="#6B7280", size=10),
                gridcolor="#1A2035", linecolor="#2A3142",
                showgrid=True,
            ),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
                font=dict(color="#9CA3AF", size=10), bgcolor="rgba(0,0,0,0)",
                itemsizing="constant",
            ),
            font=dict(color="white"),
            hovermode="closest",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "modeBarButtonsToRemove": ["lasso2d", "select2d"]})
    else:
        st.markdown('<div style="text-align:center;padding:40px;color:#6B7280">No events match the current filters.</div>', unsafe_allow_html=True)

    # ── Event list ─────────────────────────────────────────────────────────
    tabs = st.tabs(["📋 Event List", "📖 Executive Narrative", "📊 Tactic Breakdown"])

    with tabs[0]:
        sorted_events = sorted(events, key=lambda e: e["risk"], reverse=True)
        for ev in sorted_events[:25]:
            color = TACTIC_COLORS.get(ev["tactic"], "#6B7280")
            anomaly_border = "border-left:2px solid #FF4D4F;" if ev["is_anomaly"] else ""
            risk_color = "#FF4D4F" if ev["risk"] >= 9 else ("#FA8C16" if ev["risk"] >= 7 else "#FADB14" if ev["risk"] >= 5 else "#52C41A")
            ts_disp = ev["ts"][:16].replace("T", " ")
            st.markdown(f"""
            <div class="tl-event-row" style="{anomaly_border}">
                <div class="tl-ts">{ts_disp}</div>
                <div class="tl-dot" style="background:{color}"></div>
                <div class="tl-body">
                    <div class="tl-title">{ev['desc']}</div>
                    <div class="tl-detail">{ev['detail']}</div>
                    <div class="tl-tags">
                        <span class="tag technique">{ev['technique']} · {ev['tactic']}</span>
                        <span class="tag">{ev['host']}</span>
                        <span class="tag">{ev['source']}</span>
                        {'<span class="badge badge-critical" style="font-size:9px;padding:1px 6px">ANOMALY</span>' if ev['is_anomaly'] else ''}
                    </div>
                </div>
                <div class="tl-risk" style="color:{risk_color}">{ev['risk']:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        if len(sorted_events) > 25:
            st.markdown(f'<div style="text-align:center;padding:10px;color:#6B7280;font-size:12px">Showing top 25 of {len(sorted_events)} events by risk score</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown(f"""
        <div class="ey-card" style="max-width:900px">
            <div style="font-size:13px;color:#FFE600;font-weight:600;margin-bottom:12px">
                🤖 AI-Generated Attacker Narrative — {case_sel if case_sel != 'All Cases' else 'CASE-2024-001'}
            </div>
            <div style="font-size:13px;color:#D1D5DB;line-height:1.7">
        """, unsafe_allow_html=True)
        for line in _NARRATIVE.strip().split("\n"):
            if line.startswith("**Phase"):
                st.markdown(f'<div style="font-weight:700;color:#FFE600;margin-top:14px;margin-bottom:4px">{line.replace("**","")}</div>', unsafe_allow_html=True)
            elif line.strip():
                st.markdown(f'<div style="color:#D1D5DB;font-size:13px;line-height:1.6;margin-bottom:4px">{line}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with tabs[2]:
        tactic_data: dict[str, dict] = {}
        for ev in TIMELINE_EVENTS:
            t = ev["tactic"]
            if t not in tactic_data:
                tactic_data[t] = {"count": 0, "anomalies": 0, "max_risk": 0}
            tactic_data[t]["count"] += 1
            if ev["is_anomaly"]: tactic_data[t]["anomalies"] += 1
            tactic_data[t]["max_risk"] = max(tactic_data[t]["max_risk"], ev["risk"])

        for tactic in _PHASE_ORDER:
            if tactic not in tactic_data:
                continue
            d = tactic_data[tactic]
            color = TACTIC_COLORS.get(tactic, "#6B7280")
            pct = int(d["count"] / max(len(TIMELINE_EVENTS), 1) * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #1A2035">
                <div style="width:180px;font-size:12px;color:{color};font-weight:600">{tactic}</div>
                <div style="flex:1">
                    <div class="ey-prog-wrap">
                        <div class="ey-prog-fill" style="width:{min(pct*3,100)}%;background:{color}"></div>
                    </div>
                </div>
                <div style="width:50px;text-align:right;font-size:12px;color:#FFFFFF">{d['count']} evt</div>
                <div style="width:70px;text-align:right;font-size:11px;color:#FF7875">{d['anomalies']} anom</div>
                <div style="width:60px;text-align:right;font-size:11px;color:#FFE600">⚠ {d['max_risk']:.0f}/10</div>
            </div>
            """, unsafe_allow_html=True)
