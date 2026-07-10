# Global Crisis Command Center (GCCC)
## Project Summary

**Hackathon:** Neuro SAN Studio Hackathon 2026
**Author:** Sharmi VP
**Repository:** https://github.com/SharmiVP/gccc-neuro
**Date:** July 10, 2026

---

## 1. Problem Statement

Humanitarian crises rarely occur in isolation. A prolonged drought triggers food insecurity. Food insecurity compounds with existing armed conflict. Conflict disrupts healthcare access, accelerating disease outbreaks. The cascade effect of compounding crises is one of the most dangerous — and least monitored — phenomena in global humanitarian response.

Traditional crisis monitoring systems operate in silos:

- Climate agencies track weather events independently
- Health organizations monitor disease outbreaks separately
- Food security analysts assess famine risk in isolation
- Conflict monitors report on armed violence without cross-domain context

The result is **slow, fragmented, and reactive crisis response** — often arriving too late to prevent catastrophic humanitarian outcomes.

**The core problem:** No unified intelligence system exists that can simultaneously monitor all four crisis domains in real time, detect cascade chains across domains, and generate coordinated priority response plans.

---

## 2. Solution: Global Crisis Command Center (GCCC)

GCCC is an **AI-powered humanitarian intelligence system** built on Neuro SAN's multi-agent AAOSA (Agent-to-Agent Orchestration and Synthesis Architecture) framework.

It deploys a hierarchy of specialized AI agents that work in parallel across four crisis domains — climate, health, food security, and geopolitical conflict — to detect compounding emergencies and generate actionable response plans in under 60 seconds.

### Key Capabilities

| Capability | Description |
|---|---|
| **Real-time monitoring** | Live API calls to NASA EONET, WHO, IPC/FAO, ReliefWeb |
| **Parallel multi-domain** | All 4 crisis domains assessed simultaneously |
| **Cross-domain synthesis** | Cascade chain detection (e.g. Climate → Food → Conflict → Health) |
| **Intelligent routing** | AAOSA delegates only to relevant agents per query |
| **Graceful degradation** | Structured response even when APIs are partially unavailable |
| **Cost-efficient** | Full 4-domain analysis for under $0.02 using gpt-4o-mini |

---

## 3. System Architecture

GCCC is structured as a 3-tier agent hierarchy:

```
global_crisis_command_center
│
└── crisis_command_center  [Tier 1: Master Orchestrator]
    │
    ├── climate_crisis_hq  [Tier 2: Domain HQ]
    │   └── disaster_monitor         [Tier 3: Live Tool — NASA EONET API]
    │
    ├── health_epi_hq      [Tier 2: Domain HQ]
    │   └── outbreak_detector        [Tier 3: Live Tool — WHO Disease Alerts]
    │
    ├── food_agriculture_hq [Tier 2: Domain HQ]
    │   └── famine_risk_assessor     [Tier 3: Live Tool — IPC/FAO Data]
    │
    ├── geopolitical_conflict_hq [Tier 2: Domain HQ]
    │   └── conflict_monitor         [Tier 3: Live Tool — ACLED/ReliefWeb]
    │
    └── cross_domain_synthesizer [Tier 2: Cascade Detector]
```

**Tier 1 — Master Orchestrator:** `crisis_command_center` receives user queries, determines which domain HQs to engage, and synthesizes final responses.

**Tier 2 — Domain HQs:** Four specialized HQ agents, each expert in their domain. They receive delegated queries, invoke their leaf tools, and return structured domain assessments.

**Tier 3 — Live Tools:** Five Python-coded tools that make real-time API calls to authoritative humanitarian data sources and return structured JSON.

**Cross-Domain Synthesizer:** A special Tier 2 agent that activates when queries require analysis across multiple domains. It identifies cascade chains and compounding risk patterns.

### Technology Stack

| Component | Technology |
|---|---|
| Agent Framework | Neuro SAN Studio (AAOSA) |
| LLM | gpt-4o-mini via GitHub Models API |
| Agent Config | HOCON (`.hocon`) declarative format |
| Coded Tools | Python 3.13 |
| UI | NSFlow (built-in Neuro SAN Studio UI) |
| Climate Data | NASA EONET REST API |
| Health Data | WHO Disease Outbreak News |
| Food Data | IPC / FAO Food Security Portal |
| Conflict Data | ACLED / ReliefWeb API |

---

## 4. Live Test Results

All tests were conducted on **July 10, 2026** using `gpt-4o-mini` via GitHub Models API on a local development machine (Windows, Python 3.13).

### Test 1 — Single Domain Query
**Query:** *"What climate disasters are currently active globally?"*

- Agents fired: `crisis_command_center → climate_crisis_hq → disaster_monitor`
- Result: **6,850 active climate events** retrieved live from NASA EONET including wildfires in North Carolina, Minnesota, Washington, Texas, California, and Oregon with real magnitude and source data
- Tokens: 11,118 | Cost: $0.0028 | Time: 42.6s

### Test 2 — Multi-Domain Regional Query
**Query:** *"What is the current humanitarian situation in Somalia?"*

- Agents fired: All 4 domain HQs in parallel
- Result: Structured assessment across conflict, food security, and health domains with contextual synthesis
- Tokens: 43,609 | Cost: $0.0073 | Time: 24.8s

### Test 3 — Cross-Domain Compounding Query ⭐ Best Demo
**Query:** *"Are there any regions where a climate disaster is compounding with food insecurity and conflict right now?"*

- Agents fired: `cross_domain_synthesizer` + `food_agriculture_hq` + `geopolitical_conflict_hq`
- Result: Identified **9 active compounding crisis zones** — Afghanistan, DRC, Ethiopia, Haiti, Myanmar, Nigeria, Somalia, Sudan, Yemen — with cascade chain analysis
- Tokens: 25,846 | Cost: $0.0047 | Time: **17.1 seconds**

### Test 4 — Full East Africa Analysis
**Query:** *"Analyze all active crises in East Africa across climate, health, food and conflict domains. Identify any compounding emergencies and give me a priority response plan."*

- Agents fired: **All 6 agents** (complete system deployment)
- Result: Full 5-point priority response plan with domain-by-domain assessment
- Tokens: 103,944 | Cost: $0.0178 | Time: 52.9s | API requests: **78**

### Token Usage Summary

| Test | Tokens | Cost |
|---|---|---|
| Test 1 — Climate | 11,118 | $0.0028 |
| Test 2 — Somalia | 43,609 | $0.0073 |
| Test 3 — Compounding | 25,846 | $0.0047 |
| Test 4 — East Africa | 103,944 | $0.0178 |
| **Grand Total** | **184,517** | **$0.0326** |

> All 4 tests combined cost **3.26 cents** — demonstrating exceptional cost efficiency for real-time humanitarian intelligence.

---

## 5. What Makes GCCC Unique

### 1. Compounding Crisis Detection
Unlike single-domain tools, GCCC explicitly models the **cascade relationship** between crisis types. The `cross_domain_synthesizer` agent is specifically designed to identify when climate shocks, food insecurity, armed conflict, and health emergencies are co-occurring and mutually reinforcing in the same region.

### 2. Real-Time Live Data
Every response is grounded in **live API data** — not static training knowledge. The system queries NASA, WHO, IPC, and ReliefWeb in real time, ensuring responses reflect current ground truth.

### 3. AAOSA Intelligent Routing
The AAOSA framework ensures agents are only invoked when relevant. A climate-only query activates just 3 agents. A cross-domain query activates all 6. This makes the system both accurate and cost-efficient.

### 4. Structured for Action
Every response follows a structured format: domain assessment → compounding risk identification → priority response plan. This is designed for humanitarian decision-makers who need actionable intelligence, not raw data.

---

## 6. How to Run

```bash
# Clone and setup
git clone https://github.com/SharmiVP/gccc-neuro.git
cd gccc-neuro
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

# Configure
cp .env.example .env
# Set GITHUB_TOKEN in .env

# Run
python -m neuro_san_studio run
# Open http://localhost:4173 → select gccc/global_crisis_command_center
```

---

## 7. Future Enhancements

| Enhancement | Description |
|---|---|
| **Alert broadcasting** | `crisis_alert_broadcaster` tool for SMS/email alerts to field teams |
| **Historical trend analysis** | Compare current crisis levels to historical baselines |
| **Severity scoring** | Automated 1–10 compounding severity index per region |
| **Additional data sources** | UNHCR displacement data, World Bank economic indicators |
| **Dashboard UI** | Real-time crisis map visualization layer on top of NSFlow |
| **Scheduled monitoring** | Periodic automated scans with change-detection alerts |

---

## 8. Conclusion

GCCC demonstrates that the AAOSA multi-agent framework is exceptionally well-suited for **complex, multi-domain real-world intelligence tasks**. By decomposing humanitarian crisis monitoring into specialized agents that collaborate intelligently, GCCC achieves in seconds what would require hours of manual cross-domain research.

The system is production-ready in architecture, cost-efficient at scale ($0.0178 for a full 4-domain analysis), and extensible to additional crisis domains and data sources.

Most importantly, GCCC addresses a genuine gap in humanitarian response infrastructure — the ability to detect and act on **compounding crises before they become catastrophes**.

---

*Built with Neuro SAN Studio · Powered by GitHub Models (gpt-4o-mini) · July 2026*
