---
name: aziz-orb
description: "Andrew Aziz (Bear Bull Traders) day-trading method — Opening Range Breakout (ORB) + VWAP + ABCD. Trade the first N-minute range breakout with VWAP as support/resistance. Intraday 1-min data. Has peer-reviewed backtests (2018-2023 profitable)."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, day-trading, aziz, orb, opening-range-breakout, vwap, abcd, intraday]
---

# Andrew Aziz — Opening Range Breakout + VWAP (v1.0)

> **Goal (day trade):** catch the first directional move of the session. Define the
> opening range (first 5/15/30 min), then buy the breakout above it (long) or break below
> (short), using **VWAP** as the line in the sand. Aziz's book *"How to Day Trade for a
> Living"* + peer-reviewed papers (SSRN 4631351, 4729284) back this.

## 0. Plain English
The market "decides direction" in the first few minutes. Mark that high/low. When price
blasts through it on volume, follow it — but only if it stays on the right side of VWAP.

## 1. Core rules
- **Opening Range (OR):** first `N` mins (5/15/30) high & low.
- **Long signal:** price breaks above OR high, AND price > VWAP, AND volume spikes.
- **Short signal:** price breaks below OR low, AND price < VWAP, AND volume spikes.
- **Target:** 1st = prior day high / 2× range; trail with VWAP.
- **Stop:** back inside the OR (failed breakout) or just opposite side of VWAP.
- **ABCD pattern:** A→B leg, B→C retrace, C→D = same length as A→B → D is the exit/short.
- **Kill switch:** no trade in first 1-2 min (avoid noise); avoid low-volume / news traps.

## 2. Quant screen (`references/orb.py`)
Takes 1-min bars for a day, computes OR (default 15 min), VWAP, and flags the FIRST
long/short ORB signal + whether it held. Prints entries/stops/targets + a P&L if exited.

## 3. Do / Don't
**DO:** wait for the range; confirm with VWAP + volume; cut failed breakouts fast.
**DON'T:** chase 1-min wicks; trade against VWAP without a catalyst; hold through lunch
chop; size > 1-2% risk.

## 4. Script
```bash
cd <skill>/references
python3 orb.py NVDA --date 2026-08-17 --orb 15
python3 orb.py AAPL TSLA --orb 5
```

## 5. Reality notes
- yfinance 1-min = last ~7 sessions only; auto_adjust=True. Timezone is exchange-local.
- ORB needs the DAY'S 1-min bars; script fetches `period='5d'` and slices the requested date.
- Aziz's edge is *discipline + catalysts*, not the pattern alone — the script flags;
  YOU judge the catalyst (earnings, news, sector).

## 6. Pitfalls
- ❌ "Head-fake" breakouts (break then immediately fail) — the stop handles it.
- ❌ Trading ORB on a flat / low-range day (no edge).
- ❌ Ignoring VWAP — breakouts that fail to hold VWAP usually revert.

---
*Compiled 2026-08-17 from Aziz "How to Day Trade for a Living" + BearBullTraders research. Not financial advice.*
