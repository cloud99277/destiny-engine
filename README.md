[简体中文](README.md) | [English](README_EN.md)

<div align="center">

# 🔮 destiny-engine

**赛博算命终极形态——中西合璧双核命理大模型 Agent 技能**

[![Author](https://img.shields.io/badge/Author-Cloud927-blue?style=flat-square)](https://github.com/cloud99277)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

## ✨ 特点

- ☯️ **中西双引擎排盘** — 东方 `lunar-python` 引擎秒排四柱、大运、十二长生；西方 `kerykeion` 星历引擎精准计算日月升及宫位。
- ⚖️ **西方古典占星内核** — 抛弃现代占星的鸡汤废话，底层强制接入《托勒密四部星经》与威廉·莉莉的“行星庙旺落陷 (Essential Dignities)”古典尊贵度法则，推演极其硬核。
- 🤖 **Agent 原生指令** — 完美适配 OpenClaw 等大模型环境，彻底解决 AI 算命的数学计算幻觉。
- 📚 **经典命理深度解析** — 强制结合《渊海子平》、《穷通宝典》等九本经典，进行宏观运势（东方）与微观心理（西方）的千字级融合分析。全新引入**情感与亲密关系（金星月亮 x 夫妻宫）专属模块**，直击灵魂。
- 🛠️ **全自动交互框架** — 引导式多步数据收集，内置时辰对照、纳音、藏干等多维数据库。

## 🚀 快速开始

### 📦 安装

确保环境中已安装双引擎依赖库：

```bash
# 核心依赖
pip3 install lunar-python
pip3 install kerykeion
```

将仓库 clone 到你的 Agent Skill 目录（如 `~/.ai-skills/` 或 `~/.openclaw/skills/`）：

```bash
git clone https://github.com/cloud99277/destiny-engine ~/.ai-skills/destiny-engine
```

### 📖 使用说明

在 OpenClaw 或任意支持 AgentSkills 的对话界面，输入以下指令即可召唤：

> “帮我算一下八字” / “算八字” / “看命盘” / “bazi”

Skill 会自动进入交互收集流（性别、出生地经纬度、公历/农历时间），之后调用 `destiny_calc.py` 给出极其详尽的 JSON，并自动撰写“八步破局法”中西定调分析大报告。

## ⚙️ 配置

核心脚本位于 `scripts/destiny_calc.py`，你也可以直接在命令行单独调用双核引擎（支持传入经纬度、时区用于星历计算）：

```bash
python3 scripts/destiny_calc.py -y 1998 -m 7 -d 31 -H 4 -M 0 -g 1 --lat 27.76 --lng 107.48 --tz "Asia/Shanghai"
```

## 🏗️ 架构

| 模块 | 职责 |
|------|------|
| `SKILL.md` | 大模型控制 Prompt（八步解析体系，强制中西典籍双轨推演） |
| `destiny_calc.py` | 本地核心计算器，整合 NASA JPL 星历与传统阴阳历算法 |
| `references/` | 古典命理规则的检索基础库（包含《子平真诠》等东方命理典籍，以及《托勒密四部星经》行星庙旺落陷等西方古典占星法则） |

## 🙏 致谢

- 基于开源项目 [jinchenma94/bazi-skill](https://github.com/jinchenma94/bazi-skill) 演进
- `lunar-python` 强大的传统历法支持
- `kerykeion` 优雅的西方星历封装

---

<div align="center">

**Made with ❤️ by [Cloud927](https://github.com/cloud99277)**

*Part of the Agent Toolchain ecosystem*

</div>
