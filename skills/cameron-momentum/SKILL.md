---
name: cameron-momentum
description: "Ross Cameron (Warrior Trading) momentum day trading. Trade the morning high-of-day (HOD) breakout on a stock with a fresh catalyst, huge relative volume, and a clean chart. Fast in/out, 1-2% risk, trail with VWAP/EMA. Intraday 1-min."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, day-trading, ross-cameron, warrior-trading, momentum, hod-breakout, relative-volume, intraday]
---

# Ross Cameron — Momentum Day Trading (v1.0)

> **Goal (day trade):** ride the explosive first-hour move. Find a stock gapping up on
> news with **relative volume ≥ 3-5×**, wait for it to break the **high of day (HOD)**,
> enter with the momentum, and trail a tight stop (VWAP or prior breakout bar low).

## 0. Plain English
You want a stock that's *already moving hard* on a catalyst. Don't predict — react to the
breakout of the day's high with massive volume behind it, then get out fast before the
afternoon fade.

## 1. Core rules
- **Catalyst:** earnings / news / sector spike (no catalyst = no trade).
- **Relative volume ≥ 3-5×** average → real participation, not noise.
- **Breakout:** price takes out the HOD (or opening range high) on a big-volume bar.
- **Entry:** the breakout bar; **stop** = just below that bar's low (or VWAP).
- **Target / exit:** 1st = prior resistance / round number; **trail** once in profit;
  Cameron often exits same-day (never marry a momentum trade).
- **Float matters:** low-float names move fastest (highest risk).

## 2. Quant screen (`references/momentum.py`)
Uses 1-min bars: computes relative volume vs 20-day avg, flags HOD breakouts with volume
spike, and reports the runner (how far it extended post-breakout).

## 3. Do / Don't
**DO:** trade only with a catalyst + huge rel-vol; cut losers at the bar low; trail winners.
**DON'T:** buy the top after a 100% rip (chase); hold into the close; trade no-catalyst names.

## 4. Script
```bash
cd <skill>/references
python3 momentum.py NVDA --date 2026-08-17
python3 momentum.py TSLA AAPL --relvol 3
```

## 5. Reality notes
- Relative volume = today's 1-min vol sum vs 20-day avg daily vol (yfinance daily).
- "Catalyst" is NOT detectable by code — script flags the *mechanical* breakout + rel-vol;
  YOU confirm the news.
- Cameron trades low-float small-caps; here we demo on liquid names — adjust mentally.

## 6. Pitfalls
- ❌ Late-entry after the move already ran (the script reports extension % to warn).
- ❌ No catalyst = random spike that reverts.
- ❌ Widening the stop "just this once" — discipline is the whole edge.

---
*Compiled 2026-08-17 from Ross Cameron / Warrior Trading. Not financial advice.*
