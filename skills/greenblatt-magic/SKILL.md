---
name: greenblatt-magic
description: "Joel Greenblatt Magic Formula — rank stocks by Return on Capital (quality) + Earnings Yield (cheapness), buy the top, hold ~1yr, rebalance. Mechanical, evidence-based value+quality. yfinance-based ranker."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, stocks, greenblatt, magic-formula, roic, earnings-yield, quantitative, value]
---

# Joel Greenblatt — Magic Formula (v1.0)

> **Goal:** a *mechanical* system that buys good businesses at cheap prices, with no
> emotion. Greenblatt (Returns of 30%/yr backtested in "The Little Book That Beats the
> Market"). The perfect "set-and-forget quantitative" companion to the discretionary masters.

## 0. Plain English
Rank all stocks on two things: **how good a business** (high ROC) and **how cheap** (high
earnings yield). Add the two ranks; buy the names with the lowest combined rank. Hold ~1
year, rebalance. That's the whole formula.

## 1. The two formulas (exact)
- **Return on Capital (ROC)** = EBIT ÷ (Net Fixed Assets + Net Working Capital)
- **Earnings Yield** = EBIT ÷ Enterprise Value
- Rank each stock 1..N on ROC (1 = best) and on Earnings Yield (1 = best). Add ranks.
- Buy the ~20–30 with the **lowest combined rank**. Hold 1 year, sell, repeat.

## 2. Rules
- Only invest in companies with market cap above a threshold (avoid micro-caps / utilities / financials per Greenblatt).
- Equal-weight the 20–30 names.
- Rebalance annually. Ignore news, charts, macro.
- Expect to underperform in some years (behavioral sticking-power is the edge).

## 3. Do / Don't
**DO:** mechanize it; hold a year; rebalance; ignore the noise.
**DON'T:** tweak the formula emotionally; sell early on a bad month; skip the annual rebalance; add "your favourite" stocks.

## 4. Script (`references/magic.py`)
Computes ROC + earnings yield from yfinance (EBIT via `ebit`, EV via marketCap+debt−cash),
ranks a universe, prints the top names by combined rank.

```bash
cd <skill>/references
python3 magic.py --universe ../../scripts/universe.txt --top 20
python3 magic.py AAPL KO JPM XOM
```

## 5. Reality notes
- yfinance `ebit` lives in `financials`/`incomeStmt`; may be None for some → skipped.
- Excludes financials/utilities (Greenblatt) — script filters those sectors if available.
- Past 30%/yr is backtested; live results vary. The discipline (annual hold + rebalance) is the real edge.

## 6. Pitfalls
- ❌ Abandoning it after one bad year (most do — that's why it works).
- ❌ Mixing with momentum timing.
- ❌ Using it on tiny/illiquid names.

---
*Compiled 2026-08-17 from Greenblatt "The Little Book That Beats the Market". Not financial advice.*
