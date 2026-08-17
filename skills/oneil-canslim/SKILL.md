---
name: oneil-canslim
description: "William O'Neil's CAN SLIM momentum/growth strategy. Screen for stocks with strong fundamentals (C-A-N-S-L-I-M), buy pivot breakouts from sound chart bases (cup-with-handle, flat base, double-bottom) on 40%+ volume, cut losses at 7-8%. yfinance-based scanner script included."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, stocks, oneil, canslim, momentum, growth, swing-trading, breakout]
---

# William O'Neil — CAN SLIM (v1.0)

> **Goal:** find the market's leading growth stocks at the exact breakout point, the way
> O'Neil ( founder of Investor's Business Daily, 1960s–present) did. Companion to the
> Minervini VCP skill — O'Neil is the *origin* of the pivot-breakout idea Minervini
> refined into VCP.

## 0. Plain English
Buy the **strongest earnings-growth stocks** when they **break out of a sound base** on
heavy volume. Sell fast if wrong (−7/8%). The method won O'Neil a reputation for catching
100%+ movers (Coca-Cola, Apple, Netflix-type setups).

## 1. CAN SLIM = 7 filters

| Letter | Filter | Concrete rule |
|---|---|---|
| **C** | Current quarterly earnings | EPS growth **≥ 25% YoY** (latest quarter) |
| **A** | Annual earnings | 3-yr EPS growth **≥ 25%**, ROE ≥ 17% |
| **N** | New thing | New product/high/manager, OR **new high in price** |
| **S** | Supply/Demand | Shares float not huge; rising institutional ownership; volume confirms |
| **L** | Leader not laggard | RS Rating **≥ 80** (prefer 90+); never buy laggards |
| **I** | Institutional sponsorship | At least a few top funds owning it |
| **M** | Market direction | Only buy in a **bull (uptrending general market)**; step aside in correction |

## 2. The chart buy point (PIVOT)
O'Neil's bases (all need 7+ weeks to form, except flat base 5+ weeks):
- **Cup-with-handle**: U-shape decline 20–35%, handle dips 10–20% on light volume; pivot = handle high.
- **Flat base**: 3–4% tight sideways; pivot = base high.
- **Double-bottom**: W-shape; pivot = middle peak.
- **High-tight-flag**: rare, explosive — after a 100%+ run, a brief tight flag.

**Buy rule:** close above pivot on volume **≥ 40% above the 50-day average** (O'Neil often wants 2–3× on the best). Add 0.1–0.2% to the pivot as the actual trigger.

## 3. Sell / risk rules
- **Stop:** −7% to −8% from entry, no exceptions.
- **Cut** if it falls back below the pivot within days (failed breakout).
- **Take profits** when up 20–25% (then a normal 8-week hold rule); or on a climax/top signal (weekly close weak, huge volume churn).
- **Never average down.**

## 4. How the script works (`references/canslim.py`)
- Pulls fundamentals from `yf.Ticker(t).info` (C/A/L/I/S-ish; EPS growth, ROE, RS via 52w return).
- Detects a base pivot = highest close in last 60 trading days; entry = pivot×1.01.
- Volume check approximated at scan time (or use chart). Prints `pass` (C+A+L+RS gates) + entry/stop/target.
- Note: M (market) must be checked by you (is the S&P in an uptrend?). Script prints SPY trend hint.

```bash
cd <skill>/references
python3 canslim.py AAPL NVDA ...        # single or many
python3 canslim.py --universe ../universe.txt
```

## 5. Reality notes (from running it)
- Yahoo `info` EPS growth can be `None` for losers / spin-offs → treated as fail.
- RS here = 52w return ranked vs SPY (same approximation as Minervini skill). RS≥80 gate.
- CAN SLIM is stricter on *fundamentals* than Minervini and looser on *base tightness*;
  the two skills complement: use CAN SLIM to find the name, Minervini VCP for timing.
- O'Neil's #1 lesson: **the M (market) kills more good stocks than bad chart. In a bear
  market, even perfect CAN SLIM setups fail. Check the general market first.**

## 6. Pitfalls
- ❌ Buying a laggard with great earnings but weak RS.
- ❌ Buying a base that's "wide and loose" (O'Neil hates these — wants tight handles).
- ❌ Ignoring the M (buying into a correction).
- ❌ Holding a −7% loser hoping.
- ❌ Confusing a parabola blow-off with a base (see Minervini skill's parabola note).

---
*Compiled 2026-08-17 from O'Neil's "How to Make Money in Stocks" + IBD/CAN SLIM docs. Not financial advice.*
