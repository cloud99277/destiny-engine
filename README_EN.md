[简体中文](README.md) | [English](README_EN.md)

<div align="center">

# 🔮 destiny-engine

**The Ultimate Cyber Fortune Telling Agent Skill — East Meets West Dual-Core Destiny Engine**

[![Author](https://img.shields.io/badge/Author-Cloud927-blue?style=flat-square)](https://github.com/cloud99277)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

## ✨ Features

- ☯️ **Dual-Engine Chart Generation** — Utilizes `lunar-python` for accurate Eastern Bazi (Four Pillars, Dayun) and `kerykeion` for precise Western Astrology (Sun, Moon, Ascendant, Houses).
- ⚖️ **Traditional Hellenistic Core** — Abandons modern astrology fluff. Strictly enforces Ptolemy's *Tetrabiblos* and Essential Dignities (Rulership, Exaltation, Detriment, Fall) to ensure rigorous and ruthless chart reading.
- 📈 **100-Year Life K-Line Chart** — Built-in `k_line_chart.py` visual module that quantifies 100 years of destiny momentum into a stock-market style candlestick chart (Green for up, Red for down). Perfect for social media virality!
- 🤖 **Agent-Native Prompts** — Tailor-made for OpenClaw and LLM agents to completely eliminate the "math hallucinations" usually present in AI fortune-telling.
- 📚 **Deep Classical Analysis** — Forces the model to use 9 classical texts (e.g., *Yuanhai Ziping*, *Qiongtong Baodian*) for a massive, multi-faceted integration of macroscopic Eastern destiny trends and microscopic Western psychology. Newly introduced **Intimate Relationship Module (Venus/Moon x Day Pillar)** to pierce right through your soul.
- 🛠️ **Automated Interactive Workflow** — Guides the user step-by-step to collect required details, fetching extensive metadata like NaYin, hidden stems, and DiShi.

## 🚀 Quick Start

### 📦 Installation

Ensure both engine dependencies are installed:

```bash
# Core Dependencies
pip3 install lunar-python
pip3 install kerykeion
```

Clone the repository into your Agent Skill directory (e.g. `~/.ai-skills/` or `~/.openclaw/skills/`):

```bash
git clone https://github.com/cloud99277/destiny-engine ~/.ai-skills/destiny-engine
```

### 📖 Usage

Summon the skill in OpenClaw or any AgentSkills-compatible chat by typing:

> "Calculate my Bazi" / "Read my birth chart" / "bazi"

The skill interactively collects your data (gender, location, time), calls `destiny_calc.py`, and automatically generates the "8-Step Breakthrough" unified destiny report.

## ⚙️ Options

The core script is `scripts/destiny_calc.py`. You can execute it directly via CLI (supports latitude/longitude and timezone for Western ephemeris calculations):

```bash
python3 scripts/destiny_calc.py -y 1998 -m 7 -d 31 -H 4 -M 0 -g 1 --lat 27.76 --lng 107.48 --tz "Asia/Shanghai"
```

## 🏗️ Architecture

| Module | Responsibility |
|--------|----------------|
| `SKILL.md` | Core LLM Prompt (8-step framework, dual-track classical text enforcement) |
| `destiny_calc.py` | Local calculator merging NASA JPL ephemeris and traditional lunar algorithms |
| `references/` | Baseline textual rules containing Eastern texts and Western Traditional rules (Essential Dignities, Ptolemaic principles) |

## 🙏 Acknowledgments

- Inspired by the open-source project [jinchenma94/bazi-skill](https://github.com/jinchenma94/bazi-skill)
- `lunar-python` for robust traditional calendar support
- `kerykeion` for elegant Western astrology wrappers

---

<div align="center">

**Made with ❤️ by [Cloud927](https://github.com/cloud99277)**

*Part of the Agent Toolchain ecosystem*

</div>
