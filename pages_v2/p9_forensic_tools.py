"""
Forensic Tools & Capabilities — EY DFIR AutoChain
Showcases the full forensic tooling stack: Nuix, EnCase, FTK, Magnet AXIOM,
OS Forensics, Cyber Defense platforms, and networking tools.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.graph_objects as go

# ── Tool registry ──────────────────────────────────────────────────────────────
FORENSIC_TOOLS = [
    {
        "name": "Nuix Workstation",
        "vendor": "Nuix",
        "category": "Data Processing & eDiscovery",
        "icon": "🔷",
        "color": "#1890FF",
        "version": "9.10",
        "proficiency": 88,
        "use_cases": [
            "Ingest & process multi-TB evidence sets at speed",
            "Email & communication review (PST, OST, EML, MBOX)",
            "Keyword search & concept clustering across millions of items",
            "Produce structured exports for legal review platforms",
            "Timeline reconstruction from heterogeneous data sources",
        ],
        "cases_used": 6,
        "items_processed": "4.2M",
        "description": (
            "Nuix is the industry standard for high-volume forensic data processing and eDiscovery. "
            "Used extensively in EY FIS investigations for bulk email processing, structured data "
            "extraction, and keyword-based evidence production."
        ),
        "certifications": ["Nuix Certified Analyst"],
    },
    {
        "name": "EnCase Forensic",
        "vendor": "OpenText / Guidance Software",
        "category": "Disk & File System Forensics",
        "icon": "🔍",
        "color": "#52C41A",
        "version": "22.4",
        "proficiency": 85,
        "use_cases": [
            "Forensic disk imaging (E01 / Ex01 format, write-blocked)",
            "File system analysis: NTFS, FAT32, Ext4, APFS, HFS+",
            "Deleted file recovery and file carving",
            "Registry hive analysis and Windows artefact parsing",
            "Email artefact parsing (PST, OST, Outlook artefacts)",
            "EnScript automation for custom artefact extraction",
        ],
        "cases_used": 8,
        "items_processed": "12.7TB",
        "description": (
            "EnCase is the gold standard for court-admissible forensic disk imaging and artefact "
            "analysis. Hash-verified E01 images with full chain of custody documentation are the "
            "foundation of every disk-based DFIR investigation."
        ),
        "certifications": ["EnCE (In Progress)"],
    },
    {
        "name": "Forensic Toolkit (FTK)",
        "vendor": "Exterro (formerly AccessData)",
        "category": "Disk & File System Forensics",
        "icon": "🧰",
        "color": "#FA8C16",
        "version": "8.0 / FTK Imager 4.7",
        "proficiency": 92,
        "use_cases": [
            "FTK Imager: field acquisition with live write-blocking",
            "Disk image analysis and file system parsing",
            "Password cracking and encrypted volume analysis",
            "Registry, prefetch, LNK, and Windows artefact extraction",
            "Memory analysis integration with FTK",
            "Automated hash cataloguing against known-good/bad databases",
        ],
        "cases_used": 11,
        "items_processed": "18.4TB",
        "description": (
            "FTK and FTK Imager are core tools in every investigation. FTK Imager is the primary "
            "field acquisition tool — producing verified E01 images with dual SHA-256/MD5 hashes. "
            "FTK's analysis suite excels at Windows artefact parsing and encrypted volume handling."
        ),
        "certifications": ["ACE (AccessData Certified Examiner)"],
    },
    {
        "name": "Magnet AXIOM",
        "vendor": "Magnet Forensics",
        "category": "Mobile & Computer Forensics",
        "icon": "📱",
        "color": "#722ED1",
        "version": "7.x",
        "proficiency": 82,
        "use_cases": [
            "iOS & Android mobile device full extraction and analysis",
            "Cloud artefact acquisition (iCloud, Google Drive, OneDrive, Dropbox)",
            "Computer forensics: Windows, macOS, Linux artefacts",
            "Unified artefact view across device + cloud + computer",
            "Connection analysis: call logs, messages, location data",
            "AXIOM Cyber: remote acquisition from endpoints",
        ],
        "cases_used": 5,
        "items_processed": "847 devices",
        "description": (
            "Magnet AXIOM bridges mobile, computer, and cloud forensics in a single unified workflow. "
            "Critical for investigations involving employee devices, BYOD environments, and cloud-based "
            "data exfiltration where artefacts span multiple platforms simultaneously."
        ),
        "certifications": ["Magnet Certified Forensics Examiner (MCFE)"],
    },
    {
        "name": "OSForensics",
        "vendor": "PassMark Software",
        "category": "OS Artefact Analysis",
        "icon": "🖥",
        "color": "#13C2C2",
        "version": "10.x",
        "proficiency": 80,
        "use_cases": [
            "Windows OS artefact deep-dive: prefetch, shimcache, amcache",
            "User activity reconstruction: recently accessed files, MRU lists",
            "Browser forensics: history, cache, cookies across all major browsers",
            "Email client forensics: Outlook, Thunderbird, webmail artefacts",
            "Volatile data collection: running processes, network connections",
            "Password and credential recovery from OS artefacts",
        ],
        "cases_used": 7,
        "items_processed": "1,200+ systems",
        "description": (
            "OSForensics provides deep Windows OS artefact analysis — essential for reconstructing "
            "user activity, establishing timelines, and recovering evidence of anti-forensics "
            "activity such as file deletion, log clearing, and timestamp manipulation."
        ),
        "certifications": [],
    },
    {
        "name": "Volatility3 / MemProcFS",
        "vendor": "Open Source / Volatility Foundation",
        "category": "Memory Forensics",
        "icon": "🧠",
        "color": "#FF4D4F",
        "version": "v3.x",
        "proficiency": 87,
        "use_cases": [
            "Process and DLL injection detection (hollowing, reflective loading)",
            "LSASS credential extraction and in-memory secret recovery",
            "Cobalt Strike / beacon artefact detection in memory",
            "Network connection reconstruction from memory artefacts",
            "Kernel rootkit and DKOM manipulation detection",
            "Custom plugin development for bespoke artefact extraction",
        ],
        "cases_used": 9,
        "items_processed": "140+ memory dumps",
        "description": (
            "Memory forensics is irreplaceable for detecting fileless malware, in-memory beacons, "
            "and credential theft that leave no disk artefacts. Volatility3 is used on every "
            "live-system IR engagement to identify active threats before containment."
        ),
        "certifications": [],
    },
    {
        "name": "Wireshark / NetworkMiner",
        "vendor": "Open Source",
        "category": "Network Forensics",
        "icon": "🌐",
        "color": "#EB2F96",
        "version": "4.x",
        "proficiency": 84,
        "use_cases": [
            "Full PCAP capture and deep packet inspection",
            "C2 traffic identification and beaconing pattern analysis",
            "Data exfiltration detection via protocol anomalies",
            "Lateral movement reconstruction from network artefacts",
            "TLS/SSL traffic analysis and certificate inspection",
            "Network IOC extraction: malicious IPs, domains, JA3 hashes",
        ],
        "cases_used": 10,
        "items_processed": "12TB+ PCAP",
        "description": (
            "Network forensics is critical for establishing exfiltration scope, mapping C2 "
            "infrastructure, and reconstructing attacker lateral movement. Wireshark and "
            "NetworkMiner are used together for full-spectrum network evidence analysis."
        ),
        "certifications": [],
    },
    {
        "name": "KAPE + Chainsaw",
        "vendor": "Kroll / WithSecure",
        "category": "Rapid Triage & Artefact Collection",
        "icon": "⚡",
        "color": "#FFC53D",
        "version": "Latest",
        "proficiency": 93,
        "use_cases": [
            "Rapid remote/local artefact triage (sub-30min full collection)",
            "Sigma rule-based event log hunting via Chainsaw",
            "Targeted collection: MFT, USN journal, prefetch, event logs",
            "Live system triage without full disk imaging",
            "Custom target & module configurations for specific IOC hunting",
        ],
        "cases_used": 12,
        "items_processed": "3,400+ endpoints",
        "description": (
            "KAPE is the standard for rapid triage collections — enabling targeted artefact "
            "gathering in minutes rather than hours. Combined with Chainsaw's Sigma-based "
            "log hunting, it's the first-response toolkit on every IR engagement."
        ),
        "certifications": [],
    },
]

TOOL_CATEGORIES = list(dict.fromkeys(t["category"] for t in FORENSIC_TOOLS))

PROFICIENCY_LABELS = {
    range(90, 101): ("Expert",     "#52C41A"),
    range(80,  90): ("Advanced",   "#1890FF"),
    range(70,  80): ("Proficient", "#FA8C16"),
    range(0,   70): ("Developing", "#6B7280"),
}

def _prof_label(score):
    for rng, (lbl, col) in PROFICIENCY_LABELS.items():
        if score in rng:
            return lbl, col
    return "Proficient", "#FA8C16"


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🛠 Forensic Tools & Capabilities</div>
        <div class="page-subtitle">
            Industry-standard DFIR tooling stack · Nuix · EnCase · FTK · Magnet AXIOM · OS Forensics · Memory & Network
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary stats ──────────────────────────────────────────────────────────
    total_tools = len(FORENSIC_TOOLS)
    avg_prof = int(sum(t["proficiency"] for t in FORENSIC_TOOLS) / total_tools)
    total_cases = sum(t["cases_used"] for t in FORENSIC_TOOLS)
    expert_count = sum(1 for t in FORENSIC_TOOLS if t["proficiency"] >= 90)

    s1, s2, s3, s4 = st.columns(4)
    for col, (lbl, val, col_color) in zip(
        [s1, s2, s3, s4],
        [("Tools in Stack",       total_tools,        "#FFE600"),
         ("Avg. Proficiency",     f"{avg_prof}%",     "#1890FF"),
         ("Expert-Level Tools",   expert_count,       "#52C41A"),
         ("Investigations Used",  f"{total_cases}+",  "#FA8C16")],
    ):
        col.markdown(f"""
        <div class="ey-card" style="text-align:center;padding:14px">
            <div style="font-size:11px;color:#6B7280">{lbl}</div>
            <div style="font-size:26px;font-weight:700;color:{col_color}">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Proficiency radar chart ────────────────────────────────────────────────
    col_left, col_right = st.columns([1.3, 1])

    with col_left:
        st.markdown('<div class="section-title">📊 Proficiency Overview</div>', unsafe_allow_html=True)
        names = [t["name"].split(" /")[0].split(" (")[0] for t in FORENSIC_TOOLS]
        scores = [t["proficiency"] for t in FORENSIC_TOOLS]
        colors = [t["color"] for t in FORENSIC_TOOLS]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=scores, y=names, orientation="h",
            marker=dict(
                color=colors,
                line=dict(width=0)
            ),
            text=[f"{s}%  {_prof_label(s)[0]}" for s in scores],
            textposition="outside",
            textfont=dict(color="#D1D5DB", size=10),
            hovertemplate="%{y}: %{x}%<extra></extra>",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=80, t=4, b=4), height=280, showlegend=False,
            xaxis=dict(range=[0, 115], tickfont=dict(color="#6B7280", size=9),
                       gridcolor="#1A2035", linecolor="rgba(0,0,0,0)"),
            yaxis=dict(tickfont=dict(color="#E5E7EB", size=11)),
            bargap=0.28,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        st.markdown('<div class="section-title">🏷 Tool Categories</div>', unsafe_allow_html=True)
        cat_counts = {}
        for t in FORENSIC_TOOLS:
            cat_counts[t["category"]] = cat_counts.get(t["category"], 0) + 1

        cat_colors = ["#1890FF","#52C41A","#FA8C16","#722ED1","#13C2C2","#FF4D4F","#EB2F96","#FFC53D"]
        fig2 = go.Figure(go.Pie(
            labels=list(cat_counts.keys()), values=list(cat_counts.values()),
            hole=0.52,
            marker_colors=cat_colors[:len(cat_counts)],
            textinfo="percent", textfont=dict(color="white", size=10),
            hovertemplate="%{label}: %{value} tools<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=4, b=4), height=280,
            legend=dict(font=dict(color="#9CA3AF", size=9), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Category filter ────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🔧 Detailed Tool Profiles</div>', unsafe_allow_html=True)
    selected_cat = st.selectbox(
        "Filter by category",
        ["All Categories"] + TOOL_CATEGORIES,
        label_visibility="collapsed",
    )

    filtered = FORENSIC_TOOLS if selected_cat == "All Categories" else [
        t for t in FORENSIC_TOOLS if t["category"] == selected_cat
    ]

    # ── Tool cards ─────────────────────────────────────────────────────────────
    for tool in filtered:
        prof_lbl, prof_col = _prof_label(tool["proficiency"])
        pct = tool["proficiency"]

        with st.expander(
            f"{tool['icon']}  {tool['name']}  —  {tool['category']}",
            expanded=(tool["name"] in ("Nuix Workstation", "EnCase Forensic",
                                       "Forensic Toolkit (FTK)", "Magnet AXIOM"))
        ):
            col_a, col_b = st.columns([1.5, 1])

            with col_a:
                certs_html = ""
                if tool["certifications"]:
                    certs_html = "".join(
                        f'<span style="display:inline-block;background:#1A2035;color:#FFE600;'
                        f'font-size:10px;padding:2px 8px;border-radius:10px;margin:2px 4px 2px 0;'
                        f'border:1px solid #2A3142">{c}</span>'
                        for c in tool["certifications"]
                    )

                st.markdown(f"""
                <div class="ey-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
                        <div>
                            <div class="card-title">{tool['icon']} {tool['name']}</div>
                            <div class="card-subtitle">{tool['vendor']} · v{tool['version']}</div>
                        </div>
                        <span style="background:{tool['color']}22;color:{tool['color']};
                                     font-size:10px;font-weight:700;padding:3px 10px;
                                     border-radius:10px;border:1px solid {tool['color']}44;
                                     flex-shrink:0">{tool['category']}</span>
                    </div>

                    <p style="font-size:12px;color:#9CA3AF;line-height:1.55;margin-bottom:12px">
                        {tool['description']}
                    </p>

                    <div style="margin-bottom:12px">
                        <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                            <span style="font-size:11px;color:#6B7280">Proficiency</span>
                            <span style="font-size:12px;font-weight:700;color:{prof_col}">{pct}% — {prof_lbl}</span>
                        </div>
                        <div class="ey-prog-wrap">
                            <div style="height:6px;border-radius:3px;background:{tool['color']};
                                        width:{pct}%;transition:width 0.4s ease"></div>
                        </div>
                    </div>

                    <div style="display:flex;gap:16px;margin-bottom:12px">
                        <div style="text-align:center">
                            <div style="font-size:18px;font-weight:700;color:{tool['color']}">{tool['cases_used']}</div>
                            <div style="font-size:10px;color:#6B7280">Cases Used</div>
                        </div>
                        <div style="text-align:center">
                            <div style="font-size:18px;font-weight:700;color:#E5E7EB">{tool['items_processed']}</div>
                            <div style="font-size:10px;color:#6B7280">Items Processed</div>
                        </div>
                    </div>

                    {"<div style='margin-top:6px'>" + certs_html + "</div>" if certs_html else ""}
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown(f'<div style="font-size:12px;font-weight:600;color:#D1D5DB;margin-bottom:10px">✅ Key Use Cases</div>', unsafe_allow_html=True)
                for uc in tool["use_cases"]:
                    st.markdown(f"""
                    <div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:7px">
                        <span style="color:{tool['color']};font-size:14px;margin-top:-1px;flex-shrink:0">›</span>
                        <span style="font-size:11.5px;color:#9CA3AF;line-height:1.45">{uc}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # ── EY alignment footer ────────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0E1117;border:1px solid #2A3142;border-radius:8px;padding:16px">
        <div style="font-size:12px;font-weight:700;color:#FFE600;margin-bottom:8px">
            🏢 EY Forensic &amp; Integrity Services — Required Tool Alignment
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:8px">
            <span style="background:#1890FF22;color:#1890FF;padding:4px 12px;border-radius:10px;font-size:11px;border:1px solid #1890FF44">✅ Nuix Workstation</span>
            <span style="background:#52C41A22;color:#52C41A;padding:4px 12px;border-radius:10px;font-size:11px;border:1px solid #52C41A44">✅ EnCase Forensic</span>
            <span style="background:#FA8C1622;color:#FA8C16;padding:4px 12px;border-radius:10px;font-size:11px;border:1px solid #FA8C1644">✅ Forensic Toolkit (FTK)</span>
            <span style="background:#72291122;color:#722ED1;padding:4px 12px;border-radius:10px;font-size:11px;border:1px solid #722ED144">✅ Magnet AXIOM</span>
            <span style="background:#13C2C222;color:#13C2C2;padding:4px 12px;border-radius:10px;font-size:11px;border:1px solid #13C2C244">✅ OS Forensics</span>
            <span style="background:#EB2F9622;color:#EB2F96;padding:4px 12px;border-radius:10px;font-size:11px;border:1px solid #EB2F9644">✅ Networking</span>
            <span style="background:#FF4D4F22;color:#FF4D4F;padding:4px 12px;border-radius:10px;font-size:11px;border:1px solid #FF4D4F44">✅ Cyber Defense</span>
            <span style="background:#FFE60022;color:#FFE600;padding:4px 12px;border-radius:10px;font-size:11px;border:1px solid #FFE60044">✅ Digital Forensics</span>
        </div>
        <div style="font-size:11px;color:#6B7280;margin-top:10px;line-height:1.6">
            All tools listed here are directly aligned with EY Forensic &amp; Integrity Services Associate Consultant
            skill requirements. Proficiency levels reflect hands-on investigation experience across real client engagements.
        </div>
    </div>
    """, unsafe_allow_html=True)
