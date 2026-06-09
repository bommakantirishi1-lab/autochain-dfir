"""
EY DFIR AutoChain — Enterprise CSS Design System
Dark theme inspired by Microsoft Defender XDR + CrowdStrike Falcon aesthetics.
"""

GLOBAL_CSS = """
/* ── Reset & Base ──────────────────────────────────────────────────────────── */
* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background-color: #0E1117 !important;
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}

/* ── Hide Streamlit chrome ─────────────────────────────────────────────────── */
#MainMenu, footer, header, [data-testid="stDecoration"],
.stDeployButton, [data-testid="manage-app-button"] { visibility: hidden !important; display: none !important; }

/* ── Sidebar ───────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0D1117 100%) !important;
    border-right: 1px solid #1F2937 !important;
    min-width: 220px !important;
}
[data-testid="stSidebar"] > div:first-child { background: transparent !important; padding-top: 16px !important; }

.sidebar-brand {
    display: flex; align-items: center; gap: 12px;
    padding: 8px 0 20px;
}
.brand-logo {
    font-size: 22px; background: #FFE600; border-radius: 8px;
    width: 38px; height: 38px; display: flex; align-items: center;
    justify-content: center; flex-shrink: 0; font-style: normal;
}
.brand-title { font-size: 14px; font-weight: 700; color: #FFFFFF; letter-spacing: 0.3px; }
.brand-subtitle { font-size: 10px; color: #6B7280; margin-top: 1px; letter-spacing: 0.5px; text-transform: uppercase; }

.sidebar-divider { border-top: 1px solid #1F2937; margin: 10px 0; }

/* Nav radio — enterprise nav menu */
[data-testid="stSidebar"] [data-testid="stRadio"] { width: 100%; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div:first-child { display: none; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div { gap: 1px !important; flex-direction: column !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 8px !important; padding: 9px 14px !important;
    cursor: pointer !important; width: 100% !important;
    transition: all 0.15s ease !important;
    display: flex !important; align-items: center !important; gap: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label span {
    color: #9CA3AF !important; font-size: 13px !important; font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #9CA3AF !important; font-size: 13px !important; font-weight: 500 !important; margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: rgba(255,255,255,0.05) !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover span,
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover p { color: #FFFFFF !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: rgba(255,230,0,0.08) !important;
    border-left: 3px solid #FFE600 !important; padding-left: 11px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p { color: #FFE600 !important; }

.sidebar-status { padding: 4px 0; }
.status-item { display: flex; align-items: center; gap: 8px; padding: 3px 0; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.status-dot.online { background: #52C41A; box-shadow: 0 0 5px #52C41A80; }
.status-dot.warning { background: #FADB14; box-shadow: 0 0 5px #FADB1480; animation: blink 2s infinite; }
.status-dot.error { background: #FF4D4F; box-shadow: 0 0 5px #FF4D4F80; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.status-label { font-size: 11px; color: #6B7280; }
.sidebar-footer { font-size: 10px; color: #2D3748; text-align: center; padding: 10px 0 4px; border-top: 1px solid #1F2937; margin-top: 8px; }

/* ── Page header ───────────────────────────────────────────────────────────── */
.page-header { padding: 4px 0 20px; }
.page-title {
    font-size: 24px; font-weight: 700; color: #FFFFFF;
    display: flex; align-items: center; gap: 10px; line-height: 1.2;
}
.page-subtitle { font-size: 13px; color: #6B7280; margin-top: 5px; }

/* ── Section header ────────────────────────────────────────────────────────── */
.section-title {
    font-size: 14px; font-weight: 600; color: #D1D5DB;
    margin-bottom: 12px; display: flex; align-items: center; gap: 6px;
    padding-bottom: 8px; border-bottom: 1px solid #1F2937;
}

/* ── KPI Cards ─────────────────────────────────────────────────────────────── */
.kpi-card {
    background: linear-gradient(135deg, #1A1F2B 0%, #1C2132 100%);
    border: 1px solid #2A3142; border-radius: 12px; padding: 18px 16px;
    position: relative; overflow: hidden; transition: all 0.2s;
    height: 100%;
}
.kpi-card:hover { border-color: #3D4F70; transform: translateY(-1px); box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; border-radius:12px 12px 0 0; }
.kpi-card.accent-yellow::before { background: linear-gradient(90deg,#FFE600,#FFF176); }
.kpi-card.accent-red::before    { background: linear-gradient(90deg,#FF4D4F,#FF7875); }
.kpi-card.accent-orange::before { background: linear-gradient(90deg,#FA8C16,#FFA940); }
.kpi-card.accent-blue::before   { background: linear-gradient(90deg,#1890FF,#69C0FF); }
.kpi-card.accent-green::before  { background: linear-gradient(90deg,#52C41A,#95DE64); }
.kpi-card.accent-purple::before { background: linear-gradient(90deg,#722ED1,#9254DE); }
.kpi-card.accent-teal::before   { background: linear-gradient(90deg,#13C2C2,#5CDBD3); }

.kpi-icon { font-size: 20px; margin-bottom: 10px; display: block; }
.kpi-label { font-size: 10px; color: #6B7280; text-transform: uppercase; letter-spacing: 0.9px; font-weight: 600; margin-bottom: 5px; }
.kpi-value { font-size: 28px; font-weight: 700; color: #FFFFFF; line-height: 1; margin-bottom: 6px; }
.kpi-trend { font-size: 11px; display: flex; align-items: center; gap: 3px; }
.kpi-trend.up { color: #52C41A; } .kpi-trend.down { color: #FF4D4F; } .kpi-trend.neutral { color: #6B7280; }

/* ── Generic Card ──────────────────────────────────────────────────────────── */
.ey-card {
    background: #1A1F2B; border: 1px solid #2A3142; border-radius: 12px;
    padding: 20px; transition: border-color 0.2s;
}
.ey-card:hover { border-color: #3A4560; }
.card-title { font-size: 14px; font-weight: 600; color: #FFFFFF; margin-bottom: 4px; }
.card-subtitle { font-size: 12px; color: #6B7280; }

/* ── Case Cards ────────────────────────────────────────────────────────────── */
.case-card {
    background: #1A1F2B; border: 1px solid #2A3142; border-radius: 12px;
    padding: 18px 20px; margin-bottom: 10px; transition: all 0.18s; cursor: pointer;
}
.case-card:hover { border-color: rgba(255,230,0,0.4); background: #1C2132; box-shadow: 0 2px 12px rgba(255,230,0,0.06); }
.case-card.selected { border-color: #FFE600; background: #1E2535; box-shadow: 0 0 0 1px rgba(255,230,0,0.2); }
.case-id { font-size: 10px; color: #6B7280; font-family: 'JetBrains Mono', 'Fira Code', monospace; letter-spacing: 0.5px; }
.case-title { font-size: 15px; font-weight: 600; color: #FFFFFF; margin: 4px 0 10px; line-height: 1.3; }
.case-tags { display: flex; flex-wrap: wrap; gap: 4px; margin: 8px 0; }
.case-stats { display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }
.case-stat { background: #0E1117; border: 1px solid #1F2937; border-radius: 8px; padding: 6px 12px; text-align: center; min-width: 60px; }
.case-stat-value { font-size: 16px; font-weight: 700; color: #FFFFFF; }
.case-stat-label { font-size: 9px; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 1px; }

/* ── Risk / Status Badges ──────────────────────────────────────────────────── */
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.2px; white-space: nowrap;
}
.badge-critical { background: rgba(255,77,79,0.15);  color: #FF4D4F; border: 1px solid rgba(255,77,79,0.3); }
.badge-high     { background: rgba(250,140,22,0.15); color: #FA8C16; border: 1px solid rgba(250,140,22,0.3); }
.badge-medium   { background: rgba(250,219,20,0.15); color: #FADB14; border: 1px solid rgba(250,219,20,0.3); }
.badge-low      { background: rgba(82,196,26,0.15);  color: #52C41A; border: 1px solid rgba(82,196,26,0.3); }
.badge-info     { background: rgba(24,144,255,0.15); color: #40A9FF; border: 1px solid rgba(24,144,255,0.3); }
.badge-open     { background: rgba(24,144,255,0.12); color: #40A9FF; border: 1px solid rgba(24,144,255,0.25); }
.badge-active   { background: rgba(250,140,22,0.12); color: #FA8C16; border: 1px solid rgba(250,140,22,0.25); }
.badge-contained{ background: rgba(250,219,20,0.12); color: #FADB14; border: 1px solid rgba(250,219,20,0.25); }
.badge-resolved { background: rgba(82,196,26,0.12);  color: #52C41A; border: 1px solid rgba(82,196,26,0.25); }
.badge-closed   { background: rgba(107,114,128,0.12);color: #9CA3AF; border: 1px solid rgba(107,114,128,0.25); }

/* ── Tags / Chips ──────────────────────────────────────────────────────────── */
.tag {
    display: inline-block; background: #1F2937; color: #9CA3AF;
    padding: 2px 8px; border-radius: 4px; font-size: 10px;
    margin-right: 4px; margin-bottom: 3px; font-family: monospace;
}
.tag.technique { background: rgba(114,46,209,0.15); color: #B37FEB; border: 1px solid rgba(114,46,209,0.2); }
.tag.ioc       { background: rgba(255,77,79,0.1);  color: #FF7875; border: 1px solid rgba(255,77,79,0.15); }
.tag.c2        { background: rgba(255,77,79,0.1);  color: #FF4D4F; border: 1px solid rgba(255,77,79,0.2); }
.tag.actor     { background: rgba(250,140,22,0.1); color: #FA8C16; border: 1px solid rgba(250,140,22,0.2); }

/* ── Metric rows ───────────────────────────────────────────────────────────── */
.metric-row { display:flex; justify-content:space-between; padding:9px 0; border-bottom:1px solid #1A2035; align-items:center; }
.metric-row:last-child { border-bottom: none; }
.metric-key { font-size: 12px; color: #6B7280; }
.metric-val { font-size: 12px; color: #FFFFFF; font-weight: 500; font-family: monospace; }

/* ── Progress bars ─────────────────────────────────────────────────────────── */
.ey-prog-wrap { background: #0E1117; border-radius: 4px; height: 5px; overflow: hidden; }
.ey-prog-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
.ey-prog-fill.yellow { background: linear-gradient(90deg,#FFE600,#FFF176); }
.ey-prog-fill.red    { background: linear-gradient(90deg,#FF4D4F,#FF7875); }
.ey-prog-fill.orange { background: linear-gradient(90deg,#FA8C16,#FFA940); }
.ey-prog-fill.green  { background: linear-gradient(90deg,#52C41A,#73D13D); }
.ey-prog-fill.blue   { background: linear-gradient(90deg,#1890FF,#69C0FF); }
.ey-prog-fill.purple { background: linear-gradient(90deg,#722ED1,#9254DE); }

/* ── Alert feed ────────────────────────────────────────────────────────────── */
.alert-item {
    display: flex; gap: 12px; align-items: flex-start; padding: 11px 12px;
    border-radius: 8px; margin-bottom: 6px; border: 1px solid #1F2937;
    background: #141922; transition: border-color 0.2s;
}
.alert-item:hover { border-color: #2A3142; }
.alert-icon { font-size: 16px; flex-shrink: 0; padding-top: 1px; }
.alert-body { flex: 1; }
.alert-title { font-size: 12px; font-weight: 500; color: #E5E7EB; line-height: 1.3; }
.alert-desc { font-size: 11px; color: #6B7280; margin-top: 2px; line-height: 1.3; }
.alert-time { font-size: 10px; color: #374151; white-space: nowrap; flex-shrink: 0; }

/* ── Chain of Custody ──────────────────────────────────────────────────────── */
.custody-timeline { padding: 8px 0; }
.custody-step { display: flex; gap: 16px; position: relative; padding-bottom: 20px; }
.custody-step:not(:last-child)::after {
    content: ''; position: absolute; left: 15px; top: 34px;
    bottom: 0; width: 2px; background: linear-gradient(180deg,#FFE600 0%,#2A3142 100%);
}
.custody-dot {
    width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 14px; flex-shrink: 0; z-index: 1;
    background: #1F2937; border: 2px solid #2A3142;
}
.custody-dot.done { background: #FFE600; border-color: #FFE600; }
.custody-dot.verified { background: #52C41A; border-color: #52C41A; }
.custody-dot.pending  { background: #1A1F2B; border-color: #6B7280; }
.custody-content { flex: 1; padding-top: 4px; }
.custody-action { font-size: 13px; font-weight: 600; color: #FFFFFF; }
.custody-meta { font-size: 11px; color: #6B7280; margin-top: 2px; line-height: 1.4; }
.hash-display {
    font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #52C41A;
    background: #0A0D14; padding: 5px 8px; border-radius: 4px; margin-top: 6px;
    word-break: break-all; border: 1px solid #1A2035;
}
.integrity-badge {
    display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px;
    border-radius: 20px; font-size: 11px; font-weight: 600;
    background: rgba(82,196,26,0.12); color: #52C41A; border: 1px solid rgba(82,196,26,0.3);
    margin-top: 6px;
}
.integrity-badge.fail { background: rgba(255,77,79,0.12); color: #FF4D4F; border-color: rgba(255,77,79,0.3); }

/* ── Timeline event rows ───────────────────────────────────────────────────── */
.tl-event-row {
    display: flex; gap: 10px; padding: 10px 8px; border-radius: 7px;
    transition: background 0.15s; align-items: flex-start; margin-bottom: 2px;
    border-bottom: 1px solid #141922;
}
.tl-event-row:hover { background: rgba(255,255,255,0.03); }
.tl-event-row.anomaly { border-left: 2px solid #FF4D4F; }
.tl-ts { font-size: 10px; color: #6B7280; font-family: monospace; width: 100px; flex-shrink: 0; padding-top: 2px; line-height: 1.4; }
.tl-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 4px; }
.tl-body { flex: 1; }
.tl-title { font-size: 13px; font-weight: 500; color: #E5E7EB; line-height: 1.3; }
.tl-detail { font-size: 11px; color: #6B7280; margin-top: 2px; font-family: monospace; line-height: 1.4; }
.tl-tags { display: flex; gap: 4px; margin-top: 5px; flex-wrap: wrap; }
.tl-risk { font-size: 12px; font-weight: 700; flex-shrink: 0; width: 28px; text-align: right; padding-top: 2px; }

/* ── MITRE heatmap cells ───────────────────────────────────────────────────── */
.mitre-cell {
    background: #1A1F2B; border: 1px solid #2A3142; border-radius: 6px;
    padding: 6px 8px; font-size: 10px; color: #9CA3AF; cursor: pointer;
    transition: all 0.15s; text-align: center; min-height: 44px;
    display: flex; flex-direction: column; justify-content: center;
}
.mitre-cell:hover { border-color: #FFE600; color: #FFFFFF; }
.mitre-cell.hit-low    { background: rgba(82,196,26,0.1);  border-color: rgba(82,196,26,0.3);  color: #52C41A; }
.mitre-cell.hit-medium { background: rgba(250,140,22,0.15);border-color: rgba(250,140,22,0.3); color: #FA8C16; }
.mitre-cell.hit-high   { background: rgba(255,77,79,0.15); border-color: rgba(255,77,79,0.3);  color: #FF4D4F; }
.mitre-cell.hit-critical{ background: rgba(255,77,79,0.25);border-color: #FF4D4F; color: #FF4D4F; font-weight:700; }

/* ── Report preview ────────────────────────────────────────────────────────── */
.report-section {
    background: #141922; border: 1px solid #2A3142; border-radius: 8px;
    padding: 16px 20px; margin-bottom: 10px;
}
.report-section-title { font-size: 13px; font-weight: 600; color: #FFE600; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.report-section-body { font-size: 12px; color: #9CA3AF; line-height: 1.6; }

/* ── IOC table rows ────────────────────────────────────────────────────────── */
.ioc-row {
    display: flex; align-items: center; gap: 10px; padding: 10px 8px;
    border-bottom: 1px solid #141922; transition: background 0.15s;
}
.ioc-row:hover { background: rgba(255,255,255,0.02); }
.ioc-value { font-family: monospace; font-size: 11px; color: #E5E7EB; flex: 1; word-break: break-all; }
.ioc-score { font-size: 13px; font-weight: 700; width: 32px; text-align: center; }

/* ── Inputs & Controls ─────────────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background: #1A1F2B !important; border-color: #2A3142 !important; color: #FFFFFF !important;
}
[data-testid="stTextInput"] > div > div > input {
    background: #1A1F2B !important; border-color: #2A3142 !important; color: #FFFFFF !important;
}
[data-testid="stMultiSelect"] > div > div {
    background: #1A1F2B !important; border-color: #2A3142 !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] { background: #FFE600 !important; }

/* ── Buttons ───────────────────────────────────────────────────────────────── */
/* Sidebar nav buttons */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    background: transparent !important; border: none !important;
    border-left: 3px solid transparent !important; border-radius: 0 6px 6px 0 !important;
    color: #9CA3AF !important; font-size: 13px !important; font-weight: 400 !important;
    text-align: left !important; padding: 8px 14px !important;
    width: 100% !important; cursor: pointer !important;
    transition: all 0.15s ease !important; box-shadow: none !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: rgba(255,255,255,0.05) !important; color: #FFFFFF !important;
    border-color: transparent !important;
}

/* Global buttons */
.stButton > button {
    background: #1A1F2B !important; border: 1px solid #2A3142 !important;
    color: #D1D5DB !important; border-radius: 8px !important; transition: all 0.15s !important;
    font-size: 13px !important;
}
.stButton > button:hover { border-color: #FFE600 !important; color: #FFE600 !important; background: #1C2535 !important; }
.stButton > button[kind="primary"] { background: #FFE600 !important; color: #0E1117 !important; border-color: #FFE600 !important; font-weight: 700 !important; }
.stButton > button[kind="primary"]:hover { background: #FFF176 !important; }

/* ── Tabs ──────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #2A3142 !important; gap: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #6B7280 !important; border-radius: 6px 6px 0 0 !important; }
.stTabs [aria-selected="true"] { color: #FFE600 !important; border-bottom: 2px solid #FFE600 !important; background: rgba(255,230,0,0.05) !important; }

/* ── Expander ──────────────────────────────────────────────────────────────── */
[data-testid="stExpander"] { background: #141922 !important; border: 1px solid #2A3142 !important; border-radius: 8px !important; }
[data-testid="stExpander"] summary { color: #D1D5DB !important; }

/* ── Divider ───────────────────────────────────────────────────────────────── */
hr { border-color: #1F2937 !important; margin: 16px 0 !important; }

/* ── Scrollbar ─────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0E1117; }
::-webkit-scrollbar-thumb { background: #2A3142; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3D4F70; }

/* ── Plotly chart containers ───────────────────────────────────────────────── */
.js-plotly-plot .plotly .main-svg { background: transparent !important; }

/* ── Markdown text ─────────────────────────────────────────────────────────── */
.stMarkdown p { color: #D1D5DB !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #FFFFFF !important; }
"""
