"""
Cross-Case Correlation — Shared IOC matrix, actor links, STIX 2.1 export.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.graph_objects as go

from data_v2.mock_data import CASES, IOCS, THREAT_ACTORS, MITRE_COVERAGE, TACTIC_COLORS


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🔗 Cross-Case Correlation</div>
        <div class="page-subtitle">Shared IOC matrix · Threat actor linkage · STIX 2.1 export</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌐 IOC Overlap Matrix", "🕵 Actor Attribution Graph", "📤 STIX 2.1 Export"])

    # ── Tab 1: IOC Overlap Matrix ──────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-title">Shared IOC Overlap Between Cases</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:12px;color:#6B7280;margin-bottom:14px">
        IOCs appearing in multiple cases indicate infrastructure reuse, shared tooling, or related threat actors.
        Heatmap intensity = number of shared IOCs between case pairs.
        </div>
        """, unsafe_allow_html=True)

        # Build cross-case IOC matrix
        case_ids = [c["id"] for c in CASES]
        case_iocs: dict[str, set] = {cid: set() for cid in case_ids}
        for ioc in IOCS:
            if ioc["case_id"] in case_iocs:
                case_iocs[ioc["case_id"]].add(ioc["value"])

        # Simulated cross-case overlaps for richer demo
        _SIMULATED_SHARED = {
            ("CASE-2024-001", "CASE-2024-005"): 4,  # ALPHV / Lazarus share TOR exit nodes
            ("CASE-2024-001", "CASE-2024-006"): 2,
            ("CASE-2024-002", "CASE-2024-007"): 3,  # APT29 / spearphish infrastructure
            ("CASE-2024-003", "CASE-2024-006"): 1,
            ("CASE-2024-005", "CASE-2024-008"): 2,
            ("CASE-2024-004", "CASE-2024-007"): 1,
        }

        n = len(case_ids)
        z = [[0] * n for _ in range(n)]
        for i, ci in enumerate(case_ids):
            for j, cj in enumerate(case_ids):
                if i == j:
                    z[i][j] = len(case_iocs.get(ci, set()))
                else:
                    key1 = (ci, cj)
                    key2 = (cj, ci)
                    shared = len(case_iocs[ci] & case_iocs[cj])
                    shared += _SIMULATED_SHARED.get(key1, 0) + _SIMULATED_SHARED.get(key2, 0)
                    z[i][j] = shared

        short_ids = [cid.replace("CASE-2024-", "C-") for cid in case_ids]
        hover_text = []
        for i, ci in enumerate(case_ids):
            row = []
            for j, cj in enumerate(case_ids):
                if i == j:
                    row.append(f"<b>{ci}</b><br>Self ({z[i][j]} IOCs)")
                elif z[i][j] > 0:
                    row.append(f"<b>{ci} ↔ {cj}</b><br>{z[i][j]} shared IOC(s)")
                else:
                    row.append(f"{ci} ↔ {cj}<br>No shared IOCs")
            hover_text.append(row)

        fig = go.Figure(go.Heatmap(
            z=z, x=short_ids, y=short_ids,
            hovertext=hover_text,
            hovertemplate="%{hovertext}<extra></extra>",
            colorscale=[[0, "#1A1F2B"], [0.01, "#141F3D"],
                        [0.3, "rgba(30,90,200,0.6)"],
                        [0.6, "rgba(255,165,0,0.7)"],
                        [1.0, "rgba(255,77,79,0.95)"]],
            showscale=True,
            xgap=3, ygap=3,
            colorbar=dict(
                tickfont=dict(color="#9CA3AF", size=10),
                title=dict(text="Shared IOCs", font=dict(color="#9CA3AF", size=10)),
            ),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=400, margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(tickfont=dict(color="#D1D5DB", size=11), side="bottom"),
            yaxis=dict(tickfont=dict(color="#D1D5DB", size=11), autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Shared IOC detail table
        st.markdown('<div class="section-title" style="margin-top:8px">Significant Cross-Case Links</div>', unsafe_allow_html=True)
        _LINKS = [
            ("CASE-2024-001", "CASE-2024-005", "185.220.101.47", "Tor exit node used as C2 by both ALPHV and Lazarus Group"),
            ("CASE-2024-001", "CASE-2024-005", "94.102.49.80", "Shared bulletproof hosting provider (Frantech Solutions)"),
            ("CASE-2024-001", "CASE-2024-006", "MITRE T1486", "Shared ransomware deployment tactic — GPO vssadmin delete"),
            ("CASE-2024-002", "CASE-2024-007", "MITRE T1566.002", "Spearphishing template overlap — same PDF lure structure"),
            ("CASE-2024-001", "CASE-2024-006", "malware_hash_shared", "FIN7 and ALPHV both used BlackBasta loader stub"),
        ]
        for src, dst, ioc, reason in _LINKS:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px;border:1px solid #1F2937;border-radius:8px;margin-bottom:6px;background:#141922">
                <span class="tag" style="font-size:11px">{src}</span>
                <span style="color:#6B7280;font-size:14px">↔</span>
                <span class="tag" style="font-size:11px">{dst}</span>
                <span class="tag technique" style="font-size:10px;font-family:monospace">{ioc}</span>
                <span style="font-size:12px;color:#9CA3AF;flex:1">{reason}</span>
                <span class="badge badge-high" style="font-size:9px">LINKED</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Actor Attribution Graph ────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Threat Actor Attribution Network</div>', unsafe_allow_html=True)

        col_graph, col_actors = st.columns([1.6, 1])
        with col_graph:
            # Build a Plotly network graph using scatter + lines
            # Nodes: cases + actors; Edges: attribution links
            node_x, node_y, node_text, node_color, node_size, node_hover = [], [], [], [], [], []
            edge_x, edge_y = [], []

            _CASE_POS = {
                "CASE-2024-001": (0.1, 0.9), "CASE-2024-002": (0.35, 0.75),
                "CASE-2024-003": (0.6, 0.85), "CASE-2024-004": (0.85, 0.75),
                "CASE-2024-005": (0.15, 0.45), "CASE-2024-006": (0.45, 0.35),
                "CASE-2024-007": (0.7, 0.5), "CASE-2024-008": (0.9, 0.35),
            }
            _ACTOR_POS = {
                "ALPHV/BlackCat": (0.1, 0.15), "APT29 (Cozy Bear)": (0.35, 0.2),
                "Unknown / Insider": (0.6, 0.15), "Lazarus Group": (0.25, 0.05),
                "FIN7": (0.7, 0.1), "Unknown Actor": (0.85, 0.2),
            }
            _ACTOR_COLORS = {
                "ALPHV/BlackCat": "#FF4D4F", "APT29 (Cozy Bear)": "#722ED1",
                "Unknown / Insider": "#FA8C16", "Lazarus Group": "#1890FF",
                "FIN7": "#13C2C2", "Unknown Actor": "#6B7280",
            }

            # Case-actor edges
            _LINKS_GA = [
                ("CASE-2024-001", "ALPHV/BlackCat", 95),
                ("CASE-2024-002", "APT29 (Cozy Bear)", 87),
                ("CASE-2024-003", "Unknown / Insider", 92),
                ("CASE-2024-004", "Lazarus Group", 78),
                ("CASE-2024-005", "Lazarus Group", 83),
                ("CASE-2024-006", "FIN7", 76),
                ("CASE-2024-007", "APT29 (Cozy Bear)", 61),
                ("CASE-2024-008", "Unknown Actor", 55),
                ("CASE-2024-001", "FIN7", 42),  # secondary attribution
            ]

            for case_id, actor, conf in _LINKS_GA:
                cx, cy = _CASE_POS[case_id]
                ax, ay = _ACTOR_POS[actor]
                edge_x += [cx, ax, None]
                edge_y += [cy, ay, None]

            # Add edges
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=edge_x, y=edge_y,
                mode="lines",
                line=dict(width=1.5, color="rgba(100,116,139,0.4)"),
                hoverinfo="none",
                showlegend=False,
            ))

            # Case nodes
            for case in CASES:
                cx, cy = _CASE_POS[case["id"]]
                risk_color = {"CRITICAL": "#FF4D4F", "HIGH": "#FA8C16", "MEDIUM": "#FADB14", "LOW": "#52C41A"}.get(case["risk"], "#6B7280")
                node_x.append(cx); node_y.append(cy)
                node_text.append(case["id"].replace("CASE-2024-", "C-"))
                node_color.append(risk_color)
                node_size.append(22)
                node_hover.append(f"<b>{case['id']}</b><br>{case['title'][:40]}<br>Risk: {case['risk']}")

            # Actor nodes
            for actor_name, (ax, ay) in _ACTOR_POS.items():
                node_x.append(ax); node_y.append(ay)
                node_text.append(actor_name.split()[0])
                node_color.append(_ACTOR_COLORS.get(actor_name, "#6B7280"))
                node_size.append(30)
                node_hover.append(f"<b>{actor_name}</b><br>Threat Actor Node")

            fig2.add_trace(go.Scatter(
                x=node_x, y=node_y,
                mode="markers+text",
                marker=dict(size=node_size, color=node_color,
                            line=dict(width=2, color="#0E1117")),
                text=node_text,
                textposition="bottom center",
                textfont=dict(color="white", size=10),
                hovertext=node_hover,
                hovertemplate="%{hovertext}<extra></extra>",
                showlegend=False,
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=380, margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(visible=False, range=[-0.05, 1.05]),
                yaxis=dict(visible=False, range=[-0.05, 1.05]),
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        with col_actors:
            st.markdown('<div class="section-title">Actor Profiles</div>', unsafe_allow_html=True)
            for actor in THREAT_ACTORS:
                color = actor["color"]
                conf = actor["confidence"]
                st.markdown(f"""
                <div style="padding:10px;border:1px solid #1F2937;border-radius:8px;margin-bottom:8px;
                            border-left:3px solid {color};background:#141922">
                    <div style="display:flex;justify-content:space-between">
                        <div>
                            <div style="font-size:12px;font-weight:700;color:#FFFFFF">{actor['name']}</div>
                            <div style="font-size:10px;color:#6B7280">{actor['type']} · {actor['origin']}</div>
                        </div>
                        <div style="font-size:16px;font-weight:700;color:{color}">{conf}%</div>
                    </div>
                    <div class="ey-prog-wrap" style="margin-top:6px;height:3px">
                        <div class="ey-prog-fill" style="width:{conf}%;background:{color}"></div>
                    </div>
                    <div style="font-size:10px;color:#6B7280;margin-top:4px">
                        {len(actor['cases'])} case · {actor['ttps_matched']} TTPs
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 3: STIX 2.1 Export ────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">STIX 2.1 Threat Intelligence Export</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:12px;color:#6B7280;margin-bottom:16px">
        STIX (Structured Threat Information eXpression) 2.1 bundles are compatible with MISP, OpenCTI, Splunk ES, Microsoft Sentinel, and IBM QRadar.
        </div>
        """, unsafe_allow_html=True)

        # Export options
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            case_export = st.selectbox("Case", ["All Cases"] + [c["id"] for c in CASES], label_visibility="visible")
        with ec2:
            obj_types = st.multiselect("Object Types", ["Indicators", "Threat Actors", "Attack Patterns", "Malware", "Relationships"], default=["Indicators", "Threat Actors"])
        with ec3:
            tlp = st.selectbox("TLP Marking", ["TLP:RED", "TLP:AMBER", "TLP:GREEN", "TLP:WHITE"])

        # Preview STIX bundle
        _STIX_SAMPLE = """{
  "type": "bundle",
  "id": "bundle--a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "spec_version": "2.1",
  "created": "2024-11-15T03:47:22.000Z",
  "objects": [
    {
      "type": "indicator",
      "spec_version": "2.1",
      "id": "indicator--185220101-47",
      "created": "2024-11-15T03:47:22.000Z",
      "modified": "2024-11-15T03:47:22.000Z",
      "name": "ALPHV C2 IP - 185.220.101.47",
      "description": "ALPHV BlackCat ransomware C2 infrastructure",
      "indicator_types": ["malicious-activity", "compromised"],
      "pattern": "[ipv4-addr:value = '185.220.101.47']",
      "pattern_type": "stix",
      "valid_from": "2024-11-14T22:30:00Z",
      "confidence": 95,
      "labels": ["ransomware", "c2", "alphv"],
      "object_marking_refs": ["marking-definition--TLP-RED"],
      "external_references": [
        {"source_name": "EY DFIR", "external_id": "IOC-2024-001"},
        {"source_name": "VirusTotal", "url": "https://virustotal.com/gui/ip-address/185.220.101.47"}
      ]
    },
    {
      "type": "threat-actor",
      "spec_version": "2.1",
      "id": "threat-actor--alphv-blackcat",
      "created": "2024-11-15T03:47:22.000Z",
      "modified": "2024-11-15T03:47:22.000Z",
      "name": "ALPHV/BlackCat",
      "description": "Russian-nexus ransomware-as-a-service group",
      "threat_actor_types": ["crime-syndicate"],
      "aliases": ["BlackCat", "Noberus"],
      "sophistication": "expert",
      "resource_level": "government",
      "primary_motivation": "financial-gain",
      "confidence": 95
    },
    {
      "type": "attack-pattern",
      "spec_version": "2.1",
      "id": "attack-pattern--T1490",
      "created": "2024-11-15T03:47:22.000Z",
      "modified": "2024-11-15T03:47:22.000Z",
      "name": "Inhibit System Recovery",
      "description": "ALPHV used vssadmin to delete shadow copies prior to encryption",
      "external_references": [
        {"source_name": "mitre-attack", "external_id": "T1490",
         "url": "https://attack.mitre.org/techniques/T1490"}
      ]
    }
  ]
}"""

        st.markdown("""
        <div style="background:#0D1117;border:1px solid #1F2937;border-radius:8px;padding:4px 0;margin-bottom:12px">
            <div style="padding:8px 14px;border-bottom:1px solid #1F2937;display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:12px;font-weight:600;color:#9CA3AF">STIX 2.1 Bundle Preview</span>
                <span style="font-size:10px;color:#52C41A">● JSON Valid</span>
            </div>
        """, unsafe_allow_html=True)
        st.code(_STIX_SAMPLE, language="json")
        st.markdown("</div>", unsafe_allow_html=True)

        # Export stats
        total_iocs_export = len([i for i in IOCS if case_export == "All Cases" or i["case_id"] == case_export])
        st.markdown(f"""
        <div style="display:flex;gap:16px;padding:12px;background:#141922;border-radius:8px;margin-bottom:16px">
            <span style="font-size:12px;color:#6B7280">📦 <b style="color:#FFFFFF">{total_iocs_export}</b> indicators</span>
            <span style="font-size:12px;color:#6B7280">🕵 <b style="color:#FFFFFF">{len(THREAT_ACTORS)}</b> threat actors</span>
            <span style="font-size:12px;color:#6B7280">🔗 <b style="color:#FFFFFF">23</b> relationships</span>
            <span style="font-size:12px;color:#6B7280">⚔️ <b style="color:#FFFFFF">41</b> attack patterns</span>
            <span style="font-size:12px;color:#FFE600">{tlp}</span>
        </div>
        """, unsafe_allow_html=True)

        st.info("📤 In a production deployment, Export buttons would download the STIX bundle as a .json file. MISP, OpenCTI, and Sentinel imports are also supported via the EY DFIR Platform API.", icon="ℹ️")
