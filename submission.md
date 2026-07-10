# 🌍 Global Crisis Command Center (GCCC)
### Neuro SAN Studio Hackathon Submission

---

## 🎯 Problem Statement

Humanitarian crises rarely occur in isolation. A drought triggers food insecurity, which compounds with existing conflict, which then accelerates disease outbreaks. Traditional monitoring systems operate in silos — climate teams don't talk to health teams, food security analysts don't have real-time conflict data.

**The result:** Slow, fragmented, and reactive crisis response.

---

## 💡 Solution

**GCCC** is an AI-powered humanitarian intelligence system built on Neuro SAN's multi-agent AAOSA framework. It detects **compounding global crises** in real time and generates **coordinated priority response plans** by deploying specialized agents across four crisis domains simultaneously.

---

## 🏗️ Architecture

```
global_crisis_command_center
│
├── crisis_command_center          ← Master orchestrator (AAOSA front man)
│   │
│   ├── climate_crisis_hq          ← Climate domain HQ
│   │   └── disaster_monitor       ← NASA EONET API: live wildfire/flood/storm data
│   │
│   ├── health_epi_hq              ← Health domain HQ
│   │   └── outbreak_detector      ← WHO alerts: disease outbreaks, epidemics
│   │
│   ├── food_agriculture_hq        ← Food security domain HQ
│   │   └── famine_risk_assessor   ← IPC/FAO: famine risk classifications
│   │
│   ├── geopolitical_conflict_hq   ← Conflict domain HQ
│   │   └── conflict_monitor       ← ACLED/ReliefWeb: active conflict zones
│   │
│   └── cross_domain_synthesizer   ← Detects cascade chains across all 4 domains
```

---

## 📁 Key Files

| File | Description |
|------|-------------|
| [`registries/gccc/global_crisis_command_center.hocon`](registries/gccc/global_crisis_command_center.hocon) | Full 6-agent AAOSA network definition |
| [`coded_tools/gccc/disaster_monitor.py`](coded_tools/gccc/disaster_monitor.py) | NASA EONET live disaster data tool |
| [`coded_tools/gccc/outbreak_detector.py`](coded_tools/gccc/outbreak_detector.py) | WHO disease outbreak detection tool |
| [`coded_tools/gccc/famine_risk_assessor.py`](coded_tools/gccc/famine_risk_assessor.py) | IPC famine risk assessment tool |
| [`coded_tools/gccc/conflict_monitor.py`](coded_tools/gccc/conflict_monitor.py) | Active conflict zone monitoring tool |
| [`coded_tools/gccc/crisis_alert_broadcaster.py`](coded_tools/gccc/crisis_alert_broadcaster.py) | Cross-domain alert synthesis tool |
| [`registries/gccc/manifest.hocon`](registries/gccc/manifest.hocon) | Network registration manifest |
| [`config/llm_config.hocon`](config/llm_config.hocon) | LLM config (GitHub Models / gpt-4o-mini) |

---

## ✅ Live Test Results

All tests run on **July 10, 2026** using `gpt-4o-mini` via GitHub Models API.

### Test 1 — Single Domain (Climate)
> *"What climate disasters are currently active globally?"*

- ✅ `disaster_monitor` hit NASA EONET API live
- ✅ Returned **6,850 active climate events** with real wildfire data
- 📊 Tokens: 11,118 | Cost: $0.0028 | Time: 42.6s

### Test 2 — Multi-Domain Regional (Somalia)
> *"What is the current humanitarian situation in Somalia?"*

- ✅ All 4 HQ agents fired in parallel
- ✅ Food security, conflict, health domains all assessed
- 📊 Tokens: 43,609 | Cost: $0.0073 | Time: 24.8s

### Test 3 — Cross-Domain Compounding ⭐
> *"Are there any regions where climate disaster is compounding with food insecurity and conflict?"*

- ✅ `cross_domain_synthesizer` fired automatically
- ✅ Identified **9 compounding crisis zones**: Afghanistan, DRC, Ethiopia, Haiti, Myanmar, Nigeria, Somalia, Sudan, Yemen
- 📊 Tokens: 25,846 | Cost: $0.0047 | Time: 17.1s

---

## 🌟 What Makes GCCC Unique

| Feature | Description |
|---------|-------------|
| **Real-time data** | Live API calls to NASA EONET, WHO, IPC, ReliefWeb |
| **Parallel multi-domain** | All 4 crisis domains assessed simultaneously |
| **Cross-domain synthesis** | Unique cascade chain detection (Climate→Food→Conflict→Health) |
| **AAOSA routing** | Intelligent agent delegation — only relevant agents fire per query |
| **Graceful degradation** | Returns best available response even when some APIs are unavailable |
| **Cost-efficient** | All tests under $0.02 total using gpt-4o-mini |

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- GitHub Copilot Pro (for GitHub Models API access)
- PowerShell (Windows) or bash (Mac/Linux)

### Setup

```powershell
# 1. Clone and navigate
git clone https://github.com/SharmiVP/gccc-neuro.git
cd gccc-neuro

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
# source venv/bin/activate    # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env and set your GITHUB_TOKEN

# 5. Configure LLM (already set to GitHub Models)
# config/llm_config.hocon is pre-configured for gpt-4o-mini

# 6. Run the server
python -m neuro_san_studio run
```

### Access UI
Open `http://localhost:4173` → Select `gccc/global_crisis_command_center`

---

## 🔑 Environment Variables

```env
GITHUB_TOKEN=your_github_personal_access_token
```

> **Note:** `.env` is gitignored. Never commit your token.

---

## 📊 Token Usage Summary

| Test | Tokens | Cost |
|------|--------|------|
| Test 1 — Climate | 11,118 | $0.0028 |
| Test 2 — Somalia | 43,609 | $0.0073 |
| Test 3 — Compounding | 25,846 | $0.0047 |
| **Total** | **80,573** | **$0.0148** |

---

## 👩‍💻 Author

**Sharmi VP**
GitHub: [@SharmiVP](https://github.com/SharmiVP)

---

*Built with ❤️ using [Neuro SAN Studio](https://github.com/cognizant-ai-lab/neuro-san-studio)*
