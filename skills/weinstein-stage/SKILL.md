---
name: weinstein-stage
description: "Stan Weinstein's Stage Analysis (4-stage lifecycle). The 'when' of trading: only buy in Stage 2 (advancing) above a rising 30-week/200-day MA; never hold Stage 4. yfinance-based scanner that classifies each stock's stage and flags Stage-2 breakouts."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, stocks, weinstein, stage-analysis, trend, swing-trading]
---

# Stan Weinstein — Stage Analysis (v1.0)

> **Goal:** know *where in its lifecycle* a stock sits, and only trade Stage 2. The
> perfect "when" companion to O'Neil's "which" (CAN SLIM) and Minervini's "timing" (VCP).

## 0. Plain English
Every stock cycles: **decline → base → advance → top → decline**. Weinstein gives you
one moving average (30-week ≈ 150-day) and tells you exactly which stage you're in.
**Buy only in Stage 2, sell in Stage 3, be gone in Stage 4.**

## 1. The 4 stages

| Stage | Price vs 30-wk/200-day MA | MA slope | Volume | What to do |
|---|---|---|---|---|
| **1 Base** | Sideways, near MA | Flattening | Early low, then rising on up-days | Wait (recovering) |
| **2 Advancing** | **Above rising MA**, higher highs/lows | Rising | Breakout 2–3× avg | ✅ **BUY** |
| **3 Top** | Churns at highs, MA flattens | Flat | Heavy two-sided churn | Sell / trim |
| **4 Declining** | **Below falling MA**, lower highs/lows | Falling | Can fall on its own | ❌ Exit, never hold |

## 2. Exact classification rules (as coded)
Using 50/150/200-day MAs (150d ≈ 30-week):
- **Stage 2** if: price > 150MA AND 150MA > 200MA AND 150MA slope up (price now > price ~3mo ago) AND price above 50MA.
- **Stage 4** if: price < 150MA AND 150MA < 200MA AND 150MA slope down.
- **Stage 1 / 3** otherwise (base vs top — check volume + MA flattening).

## 3. Buy / sell rules
- **Buy:** breakout from Stage 1 into Stage 2, price clears the base on **2–3× volume**, holds above rising MAs.
- **Stop:** close below 50-day MA (especially on a closing basis) = trend weakening → exit.
- **Weinstein's oath:** "never hold a stock in Stage 4." Sell the moment Stage 3 support breaks, even if MAs still flat.
- Stage 2 can run months/years — trail with the MA, don't top-pick.

## 4. Script (`references/stage.py`)
Classifies a ticker into Stage 1–4, prints MA slopes + volume trend, flags Stage-2 breakouts
(price just crossed above a flat/ rising 150MA on strong volume). Also prints SPY stage as the
market filter (Weinstein: only buy individual Stage-2 stocks when the market itself is Stage 2).

```bash
cd <skill>/references
python3 stage.py NVDA APH SMCI
python3 stage.py --universe ../universe.txt
```

## 5. Reality notes
- MA slope = compare price now vs ~63 trading days ago (a 30-week ≈ 150-day proxy via 150MA slope).
- Spin-offs / fresh IPOs (e.g. SNDK) have fake MAs → Stage can mislabel; chart-verify.
- Weinstein is the *macrotiming* layer: if the S&P is Stage 4, stand aside regardless of
  a single stock's Stage 2.

## 6. Pitfalls
- ❌ Buying a Stage 1 "it looks cheap" base before the breakout confirms.
- ❌ Holding a Stage 4 stock hoping for a bottom (can fall years).
- ❌ Ignoring the market's stage (M in CAN SLIM = same idea).

---
*Compiled 2026-08-17 from Weinstein's "Secrets for Profiting in Bull and Bear Markets". Not financial advice.*
