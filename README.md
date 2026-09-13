# Suricata IDS & Splunk SOC Detection Pipeline

An end-to-end Network Intrusion Detection and Security Operations Center (SOC) lab integrating **Suricata IDS, Python, and Splunk SIEM** to detect, collect, forward, analyze, and investigate network security events generated from controlled attack scenarios.

The project simulates a small SOC environment where Kali Linux generates controlled network activity, Ubuntu runs Suricata as the network security sensor, and Splunk provides centralized security-event monitoring and analysis.

---

## 1. Project Overview

The objective of this project is to build and understand an end-to-end security monitoring pipeline rather than only configuring an IDS.

The pipeline covers:

1. Generating controlled network attack/test traffic from Kali Linux.
2. Monitoring the traffic using Suricata IDS on Ubuntu.
3. Creating custom Suricata detection rules.
4. Generating structured security events in Suricata EVE JSON format.
5. Incrementally collecting new EVE JSON events using Python.
6. Forwarding the events to Splunk through HTTP Event Collector (HEC).
7. Searching and analyzing the events using Splunk SPL queries.
8. Creating detections and alerts for security monitoring.
9. Mapping relevant detections to MITRE ATT&CK techniques.
10. Investigating the resulting security events in a SOC-style workflow.

---

## 2. Architecture

```text
                         Controlled Attack Traffic
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Kali Linux    │
                         │  Attack Host    │
                         └────────┬────────┘
                                  │
                         Network Traffic
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Ubuntu Linux  │
                         │                 │
                         │    Suricata     │
                         │      IDS        │
                         └────────┬────────┘
                                  │
                           EVE JSON Events
                                  │
                                  ▼
                    /var/log/suricata/eve.json
                                  │
                                  │ SFTP / SSH
                                  ▼
                         ┌─────────────────┐
                         │  Windows Host   │
                         │                 │
                         │ Python Collector│
                         └────────┬────────┘
                                  │
                           HTTPS / HEC
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Splunk      │
                         │      SIEM       │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
                  SPL          Alerts       Dashboards
                    │
                    ▼
             SOC Investigation
```

---

## 3. Lab Environment

The project uses three main systems:

| System | Role | Technology |
|---|---|---|
| Kali Linux VM | Attack / traffic generation host | Nmap, curl, ping, SSH, DNS utilities |
| Ubuntu Linux VM | Network security sensor | Suricata IDS |
| Windows Host | Collector and SIEM environment | Python, Splunk Enterprise Docker |

The virtual machines communicate through a controlled VMware NAT network.

### Network Flow

```text
Kali Linux
    ↓
Attack / Test Traffic
    ↓
Ubuntu Linux
    ↓
Suricata IDS
    ↓
EVE JSON
    ↓
Python Incremental Collector
    ↓
Splunk HEC
    ↓
Splunk SIEM
    ↓
Detection / Analysis / Investigation
```

---

## 4. Technologies Used

- **Suricata IDS**
- **Splunk Enterprise**
- **Python**
- **Splunk HTTP Event Collector (HEC)**
- **Splunk SPL**
- **Kali Linux**
- **Ubuntu Linux**
- **Docker**
- **VMware Workstation**
- **SSH / SFTP**
- **JSON / EVE JSON**

---

## 5. Suricata Detection Engineering

Suricata is used as the network intrusion detection sensor.
Custom detection rules are maintained in the configured local rules file.

---

## 6. Security Event Collection

Suricata generates structured security telemetry in EVE JSON format.
The Python collector retrieves newly generated events from the Ubuntu Suricata sensor.

Instead of repeatedly transferring the complete EVE JSON file, the collector maintains a persistent file offset and retrieves only newly appended events.

```text
EVE JSON
   ↓
Saved byte offset
   ↓
Read newly appended events
   ↓
Parse JSON
   ↓
Send to Splunk HEC
   ↓
Update offset after successful delivery
```

This provides an incremental event collection mechanism.

---

## 7. Python Incremental Log Collector

The collector is implemented in Python using:

- `paramiko` for SSH/SFTP communication
- `requests` for HTTP communication with Splunk HEC
- `python-dotenv` for environment configuration

### Collector Responsibilities

1. Connect to the Ubuntu Suricata sensor.
2. Access the EVE JSON log.
3. Read events from the previously processed file offset.
4. Parse individual JSON events.
5. Forward events to Splunk HEC.
6. Maintain the processing offset.
7. Handle incomplete JSON lines.
8. Detect basic log truncation/rotation conditions.
9. Avoid advancing the offset when event delivery fails.

The collector therefore acts as the bridge between the Suricata sensor and Splunk.

---

## 8. Splunk Integration

Splunk receives the Suricata security events through the **HTTP Event Collector (HEC)**.

```text
Suricata EVE JSON
       ↓
Python Collector
       ↓
HTTP POST
       ↓
Splunk HEC :8088
       ↓
Splunk Index
       ↓
SPL
```

Events can then be searched and analyzed using Splunk SPL.

Example:

```spl
index=suricata sourcetype="suricata:json"
event_type=alert
```

---

# 9. Attack Scenarios & Detection Coverage

The project uses controlled attack and security-testing scenarios generated from the Kali Linux VM.

The planned detection coverage includes:

| Scenario | Description | Protocol | Detection Concept | MITRE ATT&CK |
|---|---|---|---|---|
| ICMP Host Discovery | Ping / host discovery activity | ICMP | ICMP Echo Request | T1018 |
| TCP SYN Scan | TCP port reconnaissance | TCP | SYN flags + threshold | T1046 |
| TCP NULL/XMAS Scan | TCP flag-based reconnaissance | TCP | TCP flag inspection | T1046 |
| UDP Scan | UDP port reconnaissance | UDP | UDP traffic threshold | T1046 |
| SSH Password Guessing | Repeated SSH connection/authentication attempts | SSH/TCP | Repeated connection detection | T1110.001 |
| HTTP Directory Reconnaissance | Requests to administrative/common paths | HTTP/TCP | URI content matching | T1595.003 |
| HTTP Attack Patterns | Controlled traversal/injection patterns | HTTP/TCP | URI/content inspection | T1190 |
| Suspicious HTTP User-Agent | Scanner/tool identification | HTTP/TCP | User-Agent matching | T1595 |
| ICMP Flood | Excessive ICMP traffic | ICMP | Rate/threshold detection | T1498 |
| DNS Activity | Suspicious or high-volume DNS activity | DNS/UDP | DNS query inspection | T1046 / T1071.004 |

The final project metrics are maintained based on **implemented and successfully tested detections**, rather than planned rules.

Target coverage:

```text
8+ Attack Scenarios
12+ Custom Suricata Rules
6 Network/Application Protocols
8+ MITRE ATT&CK Techniques
```

---

# 10. MITRE ATT&CK Mapping

The project maps implemented and validated detection scenarios to relevant MITRE ATT&CK techniques.

| ATT&CK ID | Technique | Project Scenario |
|---|---|---|
| T1018 | Remote System Discovery | ICMP/network discovery |
| T1046 | Network Service Scanning | TCP/UDP/NULL scans |
| T1110.001 | Password Guessing | SSH password-guessing scenario |
| T1595 | Active Scanning | Network/web reconnaissance |
| T1595.003 | Wordlist Scanning | HTTP directory reconnaissance |
| T1190 | Exploit Public-Facing Application | Controlled web attack patterns |
| T1498 | Network Denial of Service | ICMP flood |
| T1071.004 | DNS | DNS-based activity |

Mappings are based on the behavior demonstrated by each controlled scenario and are reviewed against the corresponding ATT&CK technique.

---