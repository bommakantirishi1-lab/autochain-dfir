# AutoChain DFIR

**Enterprise Digital Forensics & Incident Response automation platform**
Modelled on Big4 forensic workflows — ACPO/ISO 27037 evidence standards, MITRE ATT&CK, STIX 2.1.

---

## 🚀 Quick Start — Single Command

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

**No other servers required.** The app is fully self-contained with realistic mock data.

---

## 🌐 Online Deployment

### Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Set **Main file path**: `app.py`
4. Click **Deploy** — done

### Hugging Face Spaces

1. Create a new Space → **Streamlit** SDK
2. Upload all files (or connect GitHub repo)
3. Ensure `requirements.txt` is present
4. The app starts automatically

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install streamlit plotly pandas
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"]
```

---

## 🏗 Enterprise App Structure

```
ey_dfir_autochain/
├── app.py                    # ← Main entry point (streamlit run app.py)
├── .streamlit/
│   └── config.toml           # Dark theme configuration
├── theme/
│   └── styles.py             # Global CSS design system
├── data_v2/
│   └── mock_data.py          # Realistic mock DFIR data
├── pages_v2/
│   ├── p1_dashboard.py       # Investigation Command Center
│   ├── p2_cases.py           # Case Command Center
│   ├── p3_timeline.py        # Supertimeline (ATT&CK-aligned)
│   ├── p4_evidence.py        # Evidence Chain of Custody
│   ├── p5_mitre.py           # MITRE ATT&CK Center
│   ├── p6_ioc.py             # IOC Intelligence Center
│   ├── p7_correlation.py     # Cross-Case Correlation
│   └── p8_reports.py         # Executive Report Center
└── requirements.txt
```

---

## 📊 Features

| Module | Description |
|--------|-------------|
| 🏠 **Command Center** | KPI dashboard · Risk donut · ATT&CK tactic bar · Live alert feed |
| 📁 **Case Management** | 8 realistic cases · Full filter/search · Threat actor attribution |
| ⏱ **Supertimeline** | ATT&CK kill chain · Plotly scatter timeline · Executive narrative |
| 🗄 **Evidence Custody** | Chain of custody · SHA-256 integrity · ACPO/ISO 27037 compliant |
| 🛡 **MITRE ATT&CK** | Enterprise v14 heatmap · 12 tactics · 40+ techniques |
| 🌐 **IOC Intelligence** | VirusTotal + AbuseIPDB enrichment · Threat score gauges |
| 🔗 **Correlation** | Cross-case IOC matrix · Actor attribution graph · STIX 2.1 export |
| 📄 **Report Center** | EY-branded templates · PDF/DOCX/STIX export simulation |

---

## 🎨 Design System

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#0E1117` | App background |
| Card | `#1A1F2B` | Card surfaces |
| Border | `#2A3142` | Dividers |
| Primary | `#FFE600` | EY yellow, CTAs |
| Critical | `#FF4D4F` | Critical risk |
| High | `#FA8C16` | High risk |
| Medium | `#FADB14` | Medium risk |
| Low | `#52C41A` | Low risk / success |

---

## 🧪 Original Platform (100 Tests)

The `tests/` directory contains the original 100-test suite for the FastAPI backend:

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

To run the original FastAPI backend:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 &
streamlit run streamlit_app.py --server.port 8502
```

---

## 📋 Case Scenarios Included

1. **CASE-2024-001** — ALPHV/BlackCat Ransomware (Meridian Healthcare) — CRITICAL
2. **CASE-2024-002** — APT29 Supply Chain Compromise — CRITICAL
3. **CASE-2024-003** — BEC Financial Fraud ($2.1M) — HIGH
4. **CASE-2024-004** — Insider Threat (IP Exfiltration) — HIGH
5. **CASE-2024-005** — Lazarus Group Crypto Exchange Heist ($47M) — CRITICAL
6. **CASE-2024-006** — FIN7 POS Malware (RetailChain) — HIGH
7. **CASE-2024-007** — Spearphishing Campaign (100 executives) — MEDIUM
8. **CASE-2024-008** — APT28 LOTL Government Network — CRITICAL

---

## ⚖️ Legal Notice

This platform and all mock data are created for demonstration and job application purposes only.  
All case details, client names, and threat actor scenarios are fictitious.  
© 2024 — Built for EY Forensic & Integrity Services DFIR Engineer application.
