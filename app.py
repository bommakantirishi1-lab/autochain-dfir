"""
EY DFIR AutoChain — Enterprise Streamlit Application
Single-server app: streamlit run app.py
"""
from __future__ import annotations
import importlib
import sys
from pathlib import Path

import streamlit as st

# ── Path setup ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# ── Page config (MUST be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="EY DFIR AutoChain",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "**EY DFIR AutoChain** · Enterprise Digital Forensics & Incident Response Platform\n\nBuilt by EY Forensic & Integrity Services · v2.0 Enterprise",
    },
)

# ── CSS injection ────────────────────────────────────────────────────────────
from theme.styles import GLOBAL_CSS  # noqa: E402
st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)

# ── Navigation config ────────────────────────────────────────────────────────
_PAGES = [
    ("p1_dashboard",  "🏠  Command Center",       "LIVE"),
    ("p2_cases",      "📁  Case Management",       ""),
    ("p3_timeline",   "⏱   Supertimeline",         ""),
    ("p4_evidence",   "🗄   Evidence Custody",      ""),
    ("p5_mitre",      "🛡   MITRE ATT&CK",          ""),
    ("p6_ioc",        "🌐  IOC Intelligence",       ""),
    ("p7_correlation","🔗  Correlation",            ""),
    ("p8_reports",    "📄  Report Center",          ""),
    ("p9_forensic_tools", "🛠   Forensic Tools",    "NEW"),
]

_PAGE_LABELS = [label for _, label, _ in _PAGES]
_PAGE_MODULES = {label: module for module, label, _ in _PAGES}
_PAGE_STATUS = {label: status for _, label, status in _PAGES}
_DEFAULT_LABEL = _PAGE_LABELS[0]

# ── Session state defaults ───────────────────────────────────────────────────
if "_page_label" not in st.session_state:
    st.session_state["_page_label"] = _DEFAULT_LABEL
if "_page_module" not in st.session_state:
    st.session_state["_page_module"] = "p1_dashboard"
if "selected_case_id" not in st.session_state:
    st.session_state["selected_case_id"] = "CASE-2024-001"

# Handle programmatic navigation (from action buttons)
if st.session_state.get("_page_module"):
    mod = st.session_state["_page_module"]
    for module, label, _ in _PAGES:
        if module == mod:
            st.session_state["_page_label"] = label
            break

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand header
    st.markdown("""
    <div class="sidebar-brand">
        <div style="display:flex;align-items:center;gap:10px">
            <div style="background:#FFE600;padding:4px 10px;border-radius:4px;flex-shrink:0">
                <span style="font-size:16px;font-weight:900;color:#2E2E38;letter-spacing:1px">EY</span>
            </div>
            <div>
                <div style="font-size:13px;font-weight:700;color:#FFFFFF;line-height:1.2">DFIR AutoChain</div>
                <div style="font-size:10px;color:#6B7280">Forensic &amp; Integrity Services</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Status indicators
    st.markdown("""
    <div style="padding:0 4px;margin-bottom:12px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
            <div style="display:flex;align-items:center;gap:6px">
                <div class="status-dot pulse"></div>
                <span style="font-size:11px;color:#9CA3AF">Platform</span>
            </div>
            <span style="font-size:10px;color:#52C41A;font-weight:600">ONLINE</span>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
            <div style="display:flex;align-items:center;gap:6px">
                <div class="status-dot" style="background:#FA8C16"></div>
                <span style="font-size:11px;color:#9CA3AF">Active Cases</span>
            </div>
            <span style="font-size:10px;color:#FA8C16;font-weight:600">5 OPEN</span>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between">
            <div style="display:flex;align-items:center;gap:6px">
                <div class="status-dot" style="background:#FF4D4F"></div>
                <span style="font-size:11px;color:#9CA3AF">Threat Level</span>
            </div>
            <span style="font-size:10px;color:#FF4D4F;font-weight:600">CRITICAL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.7px;padding:0 4px;margin-bottom:6px">Navigation</div>', unsafe_allow_html=True)

    # Navigation — st.button rows (reliable across all Streamlit versions)
    current_label = st.session_state["_page_label"]
    for module, label, status_tag in _PAGES:
        is_active = (label == current_label)
        badge = f' <span style="font-size:9px;background:#FF4D4F;color:#fff;padding:1px 5px;border-radius:3px;margin-left:4px">{status_tag}</span>' if status_tag else ""
        btn_style = (
            "background:rgba(255,230,0,0.10);border-left:3px solid #FFE600;"
            "color:#FFE600;font-weight:600;"
        ) if is_active else (
            "background:transparent;border-left:3px solid transparent;"
            "color:#9CA3AF;font-weight:400;"
        )
        clicked = st.button(
            label,
            key=f"nav_{module}",
            use_container_width=True,
        )
        if clicked and not is_active:
            st.session_state["_page_label"] = label
            st.session_state["_page_module"] = module
            st.rerun()

    st.markdown('<div class="sidebar-divider" style="margin-top:12px"></div>', unsafe_allow_html=True)

    # Active case indicator
    if st.session_state.get("selected_case_id"):
        st.markdown(f"""
        <div style="background:#1A1F2B;border:1px solid #2A3142;border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="font-size:10px;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px">Active Case</div>
            <div style="font-size:12px;font-weight:700;color:#FFE600">{st.session_state['selected_case_id']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Platform info
    st.markdown("""
    <div style="position:absolute;bottom:16px;left:16px;right:16px">
        <div style="font-size:10px;color:#374151;text-align:center;line-height:1.5">
            EY DFIR AutoChain v2.0<br>
            Enterprise Edition<br>
            © 2024 Ernst &amp; Young LLP
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Dynamic page routing ──────────────────────────────────────────────────────
current_module = _PAGE_MODULES.get(st.session_state["_page_label"], "p1_dashboard")

try:
    page = importlib.import_module(f"pages_v2.{current_module}")
    if hasattr(page, "render"):
        page.render()
    else:
        st.error(f"Page module `{current_module}` has no `render()` function.")
except ImportError as e:
    st.error(f"Could not load page: {e}")
    st.code(str(e))
except Exception as e:
    st.error(f"Page error: {e}")
    import traceback
    st.code(traceback.format_exc())
