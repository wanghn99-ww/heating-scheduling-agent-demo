# Heating Dispatch – Multi-Agent Negotiation Demo

A multi-agent negotiation prototype for urban heating dispatch, built with VibeCoding (AI-assisted programming).

---

## Scenario

Three agents with conflicting objectives negotiate a dispatch plan:

- **Welfare Agent** – Targets room temperature >= 22°C, willing to concede to reduce costs.
- **Economy Agent** – Targets room temperature >= 18°C (minimum), willing to accept slightly higher for social welfare.
- **Leader (Coordinator)** – Selects the proposal with the highest combined score each round.

---

## Mechanism

- **Welfare Score** – 100 if >= 18°C; exponential decay below 18°C.
- **Economic Score** – Exponential decay with increasing cost.
- **Combined Score** – Geometric mean of welfare and economic scores.
- **Negotiation** – 4 rounds. Each round both agents propose adjustments. Leader chooses among: current plan, welfare suggestion, economy suggestion.

---

## Run the Demo

`python demo.py`

---

## Output Example (Abridged)

总调度: 各位，今天室外 -5°C，共 3 个换热站。
【初始】采用 民生代表 的预案：出力 133.0 GJ/h，室温 22.4°C
--- 第 1 轮协商 ---
  民生代表: 建议升温，力争室温接近 22°C
  效益代表: 建议降温，控制成本
  总调度: 本轮采纳 效益建议，综合得分 22.7
--- 第 2 轮协商 ---
  ...（中间轮次省略）...
===== 最终调度预案 =====
热源出力: 119.0 GJ/h，室温 18.4°C，运行成本 110.80 万元
综合评分: 25.1

---

## Real-World Mapping

- **Heating dispatch coordination** -> Multi-agent task decomposition and governance.
- **Cross-chain trust research** -> Agent validation, conflict resolution, and trust protocols.

---

## Tech Stack

- Python 3.10+
- AI-assisted coding: DeepSeek / Copilot
- No external AI API dependencies

---

## Repository Structure

- demo.py – Main demo script
- README.md – This file

---

## Author

Wang Haonan – AI Application Architecture candidate
Background: cross-chain research + heating dispatch operations + VibeCoding
