---
name: peter-lynch
description: "Peter Lynch GARP (Growth At A Reasonable Price). Buy what you know; use the PEG ratio (P/E ÷ earnings growth) to find growth stocks priced fairly. PEG ≤ 1 = reasonable. yfinance-based PEG scanner."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, stocks, peter-lynch, garp, peg, growth, value, swing-trading]
---

# Peter Lynch — GARP / PEG (v1.0)

> **Goal:** combine growth + value. Lynch (Fidelity Magellan, ~29%/yr for 13 yrs) bought
> ordinary businesses he understood, at a price that made sense vs their growth.

## 0. Plain English
A stock's P/E should be *lower than or equal to its earnings growth rate*. That ratio is
**PEG = P/E ÷ EPS growth %**. PEG ≤ 1 means you're paying less than the growth you get.
PEG ≤ 0.5 = cheap growth.

## 1. Core rules
- **Invest in what you know** — consumer products you see, industries you understand.
- **PEG ≤ 1** is the buy filter (Lynch often liked ≤ 0.5 even better).
- Classify stocks: slow growers, stalwarts, fast growers (his favourite — small cos growing 20–25%), cyclicals, turnarounds, asset plays.
- **Fast growers** at a reasonable PEG = his edge. Avoid hot stocks with PEG ≫ 1.
- Hold as long as the story holds; sell when PEG gets silly or earnings stumble.

## 2. Quant screen (`references/peg.py`)
- PEG = trailingPE ÷ (EPS growth % × 100). Pass if PEG ≤ 1 (and EPS growth positive).
- Also shows P/E, growth, to eyeball the quality.

## 3. Do / Don't
**DO:** buy what you understand; use PEG; let winners run; study the company.
**DON'T:** buy on tips/hype; ignore the P/E vs growth; hold a falling-earnings story; over-diversify into 50 names you can't track.

## 4. Script
```bash
cd <skill>/references
python3 peg.py AAPL NVDA APH
python3 peg.py --universe ../../scripts/universe.txt
```

## 5. Reality notes
- EPS growth source: yfinance `earningsGrowth` (often TTM YoY); can be None for losers → fail.
- PEG uses trailing P/E; for very high-growth names forward PEG is better but noisier.
- Lynch's real edge was *business understanding* the screen can't capture — use it as a filter.

## 6. Pitfalls
- ❌ PEG ≤ 1 on a company with decelerating growth (the "G" is backward-looking).
- ❌ Buying a high-PEG story stock because "it's the future."
- ❌ Ignoring debt/cyclicality in the PEG.

---
*Compiled 2026-08-17 from Lynch "One Up on Wall Street" / "Beating the Street". Not financial advice.*
