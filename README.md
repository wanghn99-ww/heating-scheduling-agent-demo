# Heating Dispatch Multi-Agent Negotiation Demo

A multi-agent negotiation prototype for urban heating dispatch, built with VibeCoding.

## Scenario
Three agents with conflicting objectives negotiate a dispatch plan:
- **Welfare Agent**: Targets ≥22°C, willing to concede to reduce costs.
- **Economy Agent**: Targets ≥18°C, willing to accept slightly higher temperatures for social welfare.
- **Leader (Coordinator)**: Selects the plan with the highest combined score each round.

## Mechanism
- **Welfare Score**: Exponential decay below 18°C.
- **Economic Score**: Exponential decay with cost.
- **Combined Score**: Geometric mean of welfare and economic scores.
- **Negotiation**: 4 rounds of bidirectional concessions, moving toward the middle.

## Run
```bash
python demo.py
