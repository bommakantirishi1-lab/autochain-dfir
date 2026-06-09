"""
Executive Report Center — EY-branded report builder with PDF/DOCX preview.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from data_v2.mock_data import CASES, DASHBOARD_STATS


_REPORT_TEMPLATES = {
    "Executive Summary": {
        "desc": "C-suite brief (2–3 pages). Key findings, business impact, immediate actions.",
        "sections": ["Executive Overview", "Business Impact Assessment", "Key Findings", "Recommended Actions", "Risk Summary"],
        "audience": "CEO / Board",
        "icon": "📊",
    },
    "Technical Investigation": {
        "desc": "Full IR report (15–25 pages). TTPs, IOCs, forensic timeline, evidence chain.",
        "sections": ["Case Summary", "Investigation Timeline", "ATT&CK Mapping", "IOC Repository", "Evidence Inventory", "Forensic Findings", "Containment Actions", "Remediation Plan"],
        "audience": "CISO / Security Team",
        "icon": "🔬",
    },
    "Regulatory Disclosure": {
        "desc": "Breach notification report. GDPR / HIPAA / PCI-DSS compliant format.",
        "sections": ["Incident Description", "Data Subject Impact", "Notification Timeline", "Regulatory Obligations", "Remediation Measures", "Contact Information"],
        "audience": "Legal / Compliance",
        "icon": "⚖️",
    },
    "Threat Intelligence": {
        "desc": "Actor profile, TTP analysis, IOC digest, STIX 2.1 appendix.",
        "sections": ["Threat Actor Profile", "TTP Analysis", "IOC Repository", "Infrastructure Analysis", "STIX 2.1 Appendix"],
        "audience": "Threat Intel / SOC",
        "icon": "🎯",
    },
}

_EY_COVER = """
<div style="background:linear-gradient(135deg,#1A1F2B 0%,#0E1117 100%);border:1px solid #2A3142;
            border-radius:12px;padding:32px;min-height:340px;position:relative;overflow:hidden">
    <div style="position:absolute;top:0;right:0;width:180px;height:180px;
                background:radial-gradient(circle,rgba(255,230,0,0.08) 0%,transparent 70%)"></div>

    <!-- EY Logo area -->
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:32px">
        <div style="background:#FFE600;padding:6px 14px;border-radius:4px">
            <span style="font-size:22px;font-weight:900;color:#2E2E38;letter-spacing:1px">EY</span>
        </div>
        <div style="border-left:2px solid #2A3142;padding-left:12px">
            <div style="font-size:11px;color:#9CA3AF;letter-spacing:0.5px">FORENSIC &amp; INTEGRITY SERVICES</div>
            <div style="font-size:10px;color:#6B7280">Digital Forensics &amp; Incident Response</div>
        </div>
    </div>

    <div style="margin-bottom:8px">
        <div style="font-size:10px;color:#FFE600;text-transform:uppercase;letter-spacing:2px;margin-bottom:6px">
            PRIVILEGED &amp; CONFIDENTIAL — ATTORNEY-CLIENT PRIVILEGE
        </div>
        <div style="font-size:26px;font-weight:700;color:#FFFFFF;line-height:1.2;margin-bottom:6px">
            {report_title}
        </div>
        <div style="font-size:14px;color:#9CA3AF;margin-bottom:20px">{case_id}</div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px">
        <div>
            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:3px">Client</div>
            <div style="font-size:13px;color:#E5E7EB">{client}</div>
        </div>
        <div>
            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:3px">Prepared By</div>
            <div style="font-size:13px;color:#E5E7EB">{investigator}</div>
        </div>
        <div>
            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:3px">Date</div>
            <div style="font-size:13px;color:#E5E7EB">{date}</div>
        </div>
        <div>
            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:3px">Classification</div>
            <div style="font-size:13px;color:#FF4D4F;font-weight:600">{tlp}</div>
        </div>
        <div>
            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:3px">Risk Rating</div>
            <div style="font-size:13px;color:{risk_color};font-weight:600">{risk}</div>
        </div>
        <div>
            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:3px">Report Version</div>
            <div style="font-size:13px;color:#E5E7EB">v1.0 — FINAL</div>
        </div>
    </div>
</div>
"""


def _section_preview(title: str, content: str, index: int) -> str:
    return f"""
    <div class="report-section">
        <div style="font-size:10px;color:#FFE600;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.7px">
            {index:02d}
        </div>
        <div class="report-section-title">{title}</div>
        <div style="font-size:12px;color:#9CA3AF;line-height:1.6">{content}</div>
    </div>
    """


_SECTION_CONTENT = {
    "Executive Overview": "During the investigation period, our team identified a sophisticated ransomware intrusion by the ALPHV/BlackCat group affecting 847 domain-joined systems. The attacker achieved persistence via scheduled tasks and registry autoruns within 30 minutes of initial access. A total of 2.3 GB of patient data was exfiltrated prior to ransomware deployment.",
    "Business Impact Assessment": "The incident resulted in total encrypted systems across 3 hospital campuses, direct financial impact estimated at $4.2M (ransom demand + downtime), potential HIPAA penalties of $500K–$1.9M, and operational disruption spanning 14 hours affecting 2,400 staff.",
    "Key Findings": "1. Initial access via CVE-2024-21413 Excel exploit · 2. MFA fatigue attack on VPN · 3. DCSync credential dumping (847 NTLM hashes) · 4. Cobalt Strike C2 on port 443 · 5. Data exfil via C2 channel · 6. Ransomware deployed via GPO at 03:00 UTC.",
    "Recommended Actions": "IMMEDIATE: Rotate all AD credentials and revoke Kerberos tickets · Isolate affected endpoints · Block IOC list at perimeter · SHORT-TERM: Deploy EDR on all endpoints · Implement MFA for all admin accounts · Patch CVE-2024-21413 · STRATEGIC: Zero-trust network architecture · Privileged Access Workstations · 24/7 MDR service.",
    "Risk Summary": "Residual risk rating after containment: HIGH. Priority remediation items: 12 critical, 8 high. Estimated remediation timeline: 30–45 days for full recovery.",
    "Case Summary": "DFIR engagement initiated 2024-11-14 at 22:47 UTC following encrypted file detection. EY DFIR team deployed within 2 hours. 4 investigators assigned. Investigation scope: 847 systems, 12 servers, 3 domain controllers.",
    "Investigation Timeline": "T+0h: Initial detection · T+2h: EY DFIR engaged · T+4h: Threat actor TTPs identified · T+6h: Containment initiated · T+8h: All C2 communications blocked · T+14h: AD credential rotation complete · T+72h: Business operations restored.",
    "ATT&CK Mapping": "12 of 12 ATT&CK tactics identified across the kill chain. Dominant technique clusters: Execution (T1059.001 PowerShell), Persistence (T1053.005 Scheduled Task), Credential Access (T1003.001 LSASS Memory), Impact (T1490 Inhibit System Recovery, T1486 Data Encrypted for Impact).",
    "IOC Repository": "Full IOC list: 4 malicious IPs, 3 C2 domains, 3 malware SHA256 hashes, 1 malicious URL, 1 weaponized email, 1 registry persistence key. All IOCs provided in STIX 2.1 format in Appendix A.",
    "Evidence Inventory": "3 evidence items acquired: DC Memory Dump (32GB, SHA256 verified), Security Event Logs 90-day (4.2GB, SHA256 verified), Disk Image WORKSTATION-047 (512GB). Full chain of custody maintained per ACPO / ISO 27037.",
    "Forensic Findings": "Memory forensics confirmed Cobalt Strike beacon at PID 4892 · Prefetch analysis confirmed Mimikatz execution at 23:17 UTC · Registry artefacts confirmed 2 persistence mechanisms · Network forensics confirmed 42-minute exfil window over port 443.",
    "Containment Actions": "All affected systems isolated · AD passwords for 847 accounts rotated · Kerberos tickets invalidated · C2 IPs blocked at firewall · Malicious scheduled tasks removed · Registry autorun keys deleted.",
    "Remediation Plan": "Phase 1 (Week 1): Restore from clean backups, patch CVE-2024-21413. Phase 2 (Month 1): MFA everywhere, EDR deployment, network segmentation. Phase 3 (Quarter 1): Zero-trust architecture, PAW deployment, IR retainer.",
    "Threat Actor Profile": "ALPHV/BlackCat: Russian-nexus RaaS group active since 2021. Known for triple-extortion (encrypt + exfil + DDoS). Targets: healthcare, critical infrastructure. Estimated victims: 500+. Estimated revenue: $300M+. Attribution confidence: 95%.",
    "TTP Analysis": "ALPHV characteristically uses: (1) Initial access via N-day exploits or credential stuffing; (2) Cobalt Strike or Brute Ratel for C2; (3) DCSync for mass credential theft; (4) Exfil before encryption; (5) GPO for mass ransomware deployment. All 5 observed in this incident.",
    "Infrastructure Analysis": "C2 infrastructure hosted on bulletproof providers (Frantech/LeaseWeb) in RO/NL. TLS certificates impersonating legitimate services. Fast-flux DNS. Infrastructure TTL: 24–72 hours — consistent with ALPHV operational security.",
    "STIX 2.1 Appendix": "STIX 2.1 bundle included as digital attachment (stix_bundle_case2024001.json). Compatible with: MISP 2.4+, OpenCTI 5.0+, Microsoft Sentinel, Splunk ES 7.0+, IBM QRadar 7.5+. TLP:RED — authorized recipients only.",
    "Incident Description": "On 2024-11-14 at approximately 22:30 UTC, Meridian Healthcare experienced a ransomware attack by the ALPHV/BlackCat threat group. The attack resulted in the exfiltration of approximately 780,000 patient records and encryption of 847 systems. This constitutes a breach of Protected Health Information (PHI) under HIPAA.",
    "Data Subject Impact": "Affected data categories: Patient names, DoB, SSN, medical record numbers, insurance information, treatment history. Estimated 780,000 data subjects affected. Geographic scope: 3 states (CA, NV, AZ).",
    "Notification Timeline": "T+72h: Legal counsel engaged · T+96h: HHS OCR notified (HIPAA 60-day clock started) · T+7d: State AG notifications filed (CA, NV, AZ) · T+14d: Individual patient notifications via certified mail.",
    "Regulatory Obligations": "HIPAA Breach Notification Rule: Media notice published, HHS OCR notified. CCPA: CA AG notification filed. GDPR: Not applicable (no EU data subjects identified). PCI-DSS: Preliminary forensic report submitted to acquiring bank.",
    "Remediation Measures": "Identity: Full AD credential rotation, MFA rollout, PAM deployment. Network: EDR on all endpoints, microsegmentation. Data: Enhanced DLP, data classification program. Process: IR playbook update, tabletop exercise scheduled.",
    "Contact Information": "EY DFIR Engagement Lead: J. Nakamura CISM CISSP · EY Forensic Services, Pacific Region · Engagement Ref: EY-DFIR-2024-MH-001 · Client CISO: Brian Chen · Legal Counsel: TBD",
}


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📄 Executive Report Center</div>
        <div class="page-subtitle">EY-branded reports · PDF / DOCX / STIX 2.1 export</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Report builder sidebar ─────────────────────────────────────────────
    col_builder, col_preview = st.columns([1, 1.5])

    with col_builder:
        st.markdown('<div class="section-title">📋 Report Builder</div>', unsafe_allow_html=True)

        # Template selector
        template_name = st.selectbox("Report Template", list(_REPORT_TEMPLATES.keys()))
        template = _REPORT_TEMPLATES[template_name]
        st.markdown(f"""
        <div style="background:#141922;border:1px solid #2A3142;border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="font-size:22px;margin-bottom:4px">{template['icon']}</div>
            <div style="font-size:12px;color:#9CA3AF">{template['desc']}</div>
            <div style="font-size:11px;color:#6B7280;margin-top:4px">Audience: <span style="color:#FFE600">{template['audience']}</span></div>
        </div>
        """, unsafe_allow_html=True)

        # Case selector
        case_options = [c["id"] for c in CASES]
        sel_idx = 0
        if st.session_state.get("selected_case_id") and st.session_state["selected_case_id"] in case_options:
            sel_idx = case_options.index(st.session_state["selected_case_id"])
        case_id = st.selectbox("Case", case_options, index=sel_idx)
        case = next((c for c in CASES if c["id"] == case_id), CASES[0])

        # Classification
        tlp = st.selectbox("Classification", ["TLP:RED — Restricted", "TLP:AMBER — Limited", "TLP:GREEN — Community", "TLP:WHITE — Public"])
        tlp_short = tlp.split(" ")[0]

        # Sections to include
        st.markdown('<div style="font-size:12px;color:#9CA3AF;margin-bottom:4px">Include Sections:</div>', unsafe_allow_html=True)
        selected_sections = []
        for s in template["sections"]:
            if st.checkbox(s, value=True, key=f"sec_{template_name}_{s}"):
                selected_sections.append(s)

        # Export format
        st.markdown('<div style="font-size:12px;color:#9CA3AF;margin:8px 0 4px">Export Format:</div>', unsafe_allow_html=True)
        fmt_cols = st.columns(3)
        pdf_btn = fmt_cols[0].button("📄 PDF", use_container_width=True, type="primary")
        docx_btn = fmt_cols[1].button("📝 DOCX", use_container_width=True)
        json_btn = fmt_cols[2].button("🔗 STIX", use_container_width=True)

        if pdf_btn or docx_btn or json_btn:
            fmt = "PDF" if pdf_btn else ("DOCX" if docx_btn else "STIX 2.1 JSON")
            st.success(f"✅ **{fmt}** report generated for **{case_id}** · {len(selected_sections)} sections · {tlp_short}")
            st.markdown(f"""
            <div style="background:#141922;border:1px solid #52C41A;border-radius:8px;padding:10px;margin-top:8px">
                <div style="font-size:11px;color:#52C41A;margin-bottom:4px">Report Generated Successfully</div>
                <div style="font-family:monospace;font-size:11px;color:#9CA3AF">
                    EY_DFIR_{case_id.replace('-','_')}_{template_name.replace(' ','_')}.{fmt.split()[0].lower()}
                </div>
                <div style="font-size:10px;color:#6B7280;margin-top:4px">
                    {len(selected_sections)} sections · {tlp_short} · {fmt}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.info("In a production deployment, this would download the actual file. The report engine uses ReportLab (PDF) and python-docx (DOCX).", icon="ℹ️")

    # ── Live report preview ────────────────────────────────────────────────
    with col_preview:
        st.markdown('<div class="section-title">👁 Live Preview</div>', unsafe_allow_html=True)

        risk_colors = {"CRITICAL": "#FF4D4F", "HIGH": "#FA8C16", "MEDIUM": "#FADB14", "LOW": "#52C41A"}
        cover_html = _EY_COVER.format(
            report_title=f"{template_name} Report",
            case_id=case_id,
            client=case["client"],
            investigator=case["investigator"],
            date="2024-11-15",
            tlp=tlp_short,
            risk=case["risk"],
            risk_color=risk_colors.get(case["risk"], "#FFFFFF"),
        )
        st.markdown(cover_html, unsafe_allow_html=True)

        # Section previews
        st.markdown('<div style="margin-top:12px"></div>', unsafe_allow_html=True)
        for i, section in enumerate(selected_sections, 1):
            content = _SECTION_CONTENT.get(section, "Section content will be auto-generated from case data and investigation findings.")
            st.markdown(_section_preview(section, content, i), unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div style="background:#141922;border:1px solid #1F2937;border-radius:8px;padding:12px;margin-top:12px;
                    display:flex;justify-content:space-between;align-items:center">
            <div style="font-size:10px;color:#6B7280">
                © 2024 Ernst &amp; Young LLP · Forensic &amp; Integrity Services · All rights reserved
            </div>
            <div style="display:flex;align-items:center;gap:8px">
                <div style="background:#FFE600;padding:2px 8px;border-radius:3px">
                    <span style="font-size:11px;font-weight:700;color:#2E2E38">EY</span>
                </div>
                <span style="font-size:10px;color:#6B7280">Building a better working world</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Recent reports table ───────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📁 Recent Reports</div>', unsafe_allow_html=True)

    _RECENT_REPORTS = [
        ("EY_DFIR_CASE_2024_001_Executive_Summary.pdf",    "CASE-2024-001", "Executive Summary",     "J. Nakamura", "2024-11-15 09:14", "TLP:RED",   "2.4 MB", "#FF4D4F"),
        ("EY_DFIR_CASE_2024_001_Technical_Investigation.pdf","CASE-2024-001","Technical Investigation","J. Nakamura", "2024-11-15 11:32", "TLP:RED",   "8.1 MB", "#FF4D4F"),
        ("EY_DFIR_CASE_2024_002_Executive_Summary.pdf",    "CASE-2024-002", "Executive Summary",     "S. Okonkwo",  "2024-11-10 14:05", "TLP:AMBER", "1.8 MB", "#FA8C16"),
        ("EY_DFIR_CASE_2024_001_STIX_Bundle.json",         "CASE-2024-001", "Threat Intelligence",   "J. Nakamura", "2024-11-15 12:00", "TLP:RED",   "124 KB", "#FF4D4F"),
        ("EY_DFIR_CASE_2024_003_Regulatory_Disclosure.docx","CASE-2024-003","Regulatory Disclosure",  "M. Rodriguez","2024-11-08 16:44", "TLP:AMBER", "890 KB", "#FA8C16"),
    ]

    st.markdown("""
    <div style="background:#0E1117;border:1px solid #1F2937;border-radius:8px;overflow:hidden">
        <div style="display:grid;grid-template-columns:3fr 1fr 1.2fr 1fr 1.2fr 0.8fr 0.6fr 0.8fr;
                    padding:8px 12px;border-bottom:1px solid #1F2937;background:#141922">
            <span style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px">Filename</span>
            <span style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px">Case</span>
            <span style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px">Template</span>
            <span style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px">Author</span>
            <span style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px">Generated</span>
            <span style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px">TLP</span>
            <span style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px">Size</span>
            <span style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px">Actions</span>
        </div>
    """, unsafe_allow_html=True)

    for fname, cid, tmpl, author, gen, tlp_r, size, tlp_c in _RECENT_REPORTS:
        ext_icon = "📄" if fname.endswith(".pdf") else ("📝" if fname.endswith(".docx") else "🔗")
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:3fr 1fr 1.2fr 1fr 1.2fr 0.8fr 0.6fr 0.8fr;
                    padding:10px 12px;border-bottom:1px solid #0F1523;align-items:center">
            <span style="font-size:11px;color:#E5E7EB;font-family:monospace">{ext_icon} {fname[:40]}{'…' if len(fname)>40 else ''}</span>
            <span class="tag" style="font-size:9px">{cid.replace('CASE-2024-','C-')}</span>
            <span style="font-size:11px;color:#9CA3AF">{tmpl}</span>
            <span style="font-size:11px;color:#9CA3AF">{author}</span>
            <span style="font-size:10px;color:#6B7280;font-family:monospace">{gen}</span>
            <span style="font-size:10px;color:{tlp_c};font-weight:600">{tlp_r.split(':')[1]}</span>
            <span style="font-size:11px;color:#6B7280">{size}</span>
            <span style="font-size:11px;color:#FFE600;cursor:pointer">⬇ Download</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
