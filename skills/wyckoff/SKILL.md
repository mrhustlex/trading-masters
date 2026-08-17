---
name: wyckoff
description: "Richard Wyckoff Method — Accumulation/Distribution schematic. Identify the Composite Operator's buying (accumulation: Phase A-E with spring/shakeout) vs selling (distribution) to trade in harmony with smart money. yfinance-based scanner detects accumulation-range + spring setups."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, stocks, wyckoff, accumulation, distribution, composite-operator, swing-trading, smart-money]
---

# Richard Wyckoff — Accumulation / Distribution (v1.0)

> **Goal:** trade *with* the Composite Operator (smart money), not against. Wyckoff maps
> the full cause-and-effect of institutional accumulation (before up-moves) and
> distribution (before down-moves) via a 5-phase schematic.

## 0. Plain English
Big players can't buy millions of shares at once without moving price. So they **accumulate**
in a range (Phase A–E), shake out weak holders with a fake breakdown (the **spring**), then
mark up. Wyckoff teaches you to spot that range + spring = buy; range + upthrust = sell.

## 1. Accumulation schematic (the buy side)
- **Phase A** — downtrend stops: Preliminary Support (PS), Selling Climax (SC), Automatic Rally (AR), Secondary Test (ST).
- **Phase B** — "building the cause": range bounds set; multiple STs; institution absorbs supply.
- **Phase C** — **Spring**: price breaks *below* the range low, then reverses back in (shakes out stops, buys cheap). A low-volume spring + successful test = high-probability entry.
- **Phase D** — Sign of Strength (SOS): demand dominates, price reaches range top; Last Point of Support (LPS) holds.
- **Phase E** — Markup: leaves the range, trend obvious.

## 2. Distribution schematic (the sell/short side)
- Phase A: buying climax (BC), AR, ST.
- Phase B: cause built for downtrend (institutions distribute).
- Phase C: **Upthrust (UT/UTAD)** — fake breakout above range, then fails.
- Phase D/E: supply dominates, markdown begins.

## 3. Script (`references/wyckoff.py`)
Detects a **potential accumulation range**: price in a horizontal range for N weeks, with a
recent **spring** (new low below range then recovery) on *lower* volume (supply exhausted).
Flags the entry zone (back above the spring low / range support).

```bash
cd <skill>/references
python3 wyckoff.py NVDA APH
python3 wyckoff.py --universe ../universe.txt
```

## 4. Reality notes
- Wyckoff is the *deepest* method — needs weekly charts + volume reading; the script is a
  first-pass scanner (range + spring detection), not a substitute for reading the schematic.
- Spring must be on **declining volume** to be valid (supply dried up). Script checks this.
- Always confirm with Weinstein stage (accumulation = late Stage 1 → early Stage 2).

## 5. Pitfalls
- ❌ Buying a spring that *fails* (price stays below range = distribution, not accumulation).
- ❌ Ignoring the market (M / Stage 4) — distribution dominates in bear markets.
- ❌ Treating every dip as a spring; needs the full range context.

---
*Compiled 2026-08-17 from Wyckoff Method (wyckoffanalytics.com schematics). Not financial advice.*
