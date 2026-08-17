---
name: darvas-box
description: "Nicolas Darvas Box Theory. Draw boxes around price consolidations; buy when price breaks above the box top on volume, stop just below the box bottom. Combined with Jesse Livermore's pyramiding + cut-loss discipline. yfinance-based box detector."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, stocks, darvas, box-theory, livermore, breakout, swing-trading, pyramiding]
---

# Nicolas Darvas — Box Theory (+ Livermore discipline) (v1.0)

> **Goal:** catch a stock as it *steps up* in a series of boxes. Darvas turned $10k→$2M
> in 18 months (1950s) with this. Jesse Livermore's rules (pyramid into winners, cut
> losers immediately) are folded in as the risk layer.

## 0. Plain English
A stock runs, pauses, ranges = one "box" (floor = recent low, ceiling = recent high).
When it breaks **above the ceiling on volume**, buy. Your stop is the **box floor**.
If it keeps running, a new higher box forms — trail your stop up to each new floor
(pyramiding / riding). If price drops below the floor → stop out.

## 1. Exact rules (as coded in `references/darvas.py`)
- Box = rolling window: floor = min low, ceiling = max high over last N days (default 20).
- **Buy signal:** close > ceiling AND volume > 1.4× 50d avg AND price > box-floor.
- **Stop:** just below box floor (tight, structural).
- **Trail:** as price makes new highs, raise stop to the most recent box floor (Livermore:
  never let a profit become a loss).
- **Pyramid:** only add on a *new* box breakout above the prior ceiling, never in the middle.

## 2. Livermore discipline layered on top
- **Cut losses at the box floor — no exceptions.** Never average down.
- **Let winners run**; move stop to breakeven after first box confirms.
- **Buy strength, not weakness** — boxes form after rallies, not in declines.
- **Don't trade chop** — a box needs a clear floor/ceiling, not noise.

## 3. Script
`references/darvas.py` scans a ticker/universe, detects the current box (floor/ceiling),
reports if price is breaking out, and the trailing stop.

```bash
cd <skill>/references
python3 darvas.py NVDA APH
python3 darvas.py --universe ../universe.txt
```

## 4. Reality notes
- Box length N matters: 10–20d for swing, 20–50d for position. Script default 20.
- A parabola (see Minervini skill) has no real box — it's a vertical line; Darvas would
  NOT buy (no defined floor to stop under). Avoid.
- Spin-offs (SNDK) = fake boxes early; chart-verify.

## 5. Pitfalls
- ❌ Buying a breakdown through the floor (that's the stop, not entry).
- ❌ Widening the stop below the floor.
- ❌ Pyramiding into a parabola.
- ❌ Trading a box in a Stage-4 stock (Weinstein) — check stage first.

---
*Compiled 2026-08-17 from Darvas "How I Made $2,000,000 in the Stock Market" + Livermore "Reminiscences". Not financial advice.*
