---
name: value-masters
description: "Qualitative master-investor wisdom distilled into checklists: Charlie Munger (mental models, invert, avoid stupidity), Howard Marks (risk cycles, psychology), John Templeton (max pessimism, global), Jesse Livermore (cut losses, pyramids, sit tight). No hard scanner — a discipline/checklist skill + a Livermore risk-sizer script."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, stocks, munger, marks, templeton, livermore, mental-models, discipline, checklists]
---

# Value Masters — Munger / Marks / Templeton / Livermore (v1.0)

> **Goal:** the *mindset* layer the quants can't code. These four sharpen judgment,
> risk psychology, and behavioral edge — the part that decides whether you actually
> follow the other 8 skills' rules.

## Charlie Munger (Buffett's partner)
- **Invert:** "Invert, always invert." To get rich, first list how to stay poor and avoid it.
- **Mental models:** build a lattice across disciplines (math, psych, accounting, econ); one model alone blinds you.
- **Avoid stupidity, not seek brilliance:** most success = not doing dumb things.
- **Circle of competence + "Too Hard" pile** (with Buffett). Skip what you can't model.
- **DO:** read widely; be patient; demand quality; say no to most ideas.
- **DON'T:** trade on tips; confuse activity with wisdom; use leverage.

## Howard Marks (Oaktree, "The Most Important Thing")
- **Risk is not volatility — it's the probability of permanent loss**; bought in at the wrong price.
- **Cycles & psychology:** markets swing between euphoria and despair; buy when others are fearful, sell when greedy.
- **Second-level thinking:** what's obvious is already priced in.
- **DO:** stress-test the downside; understand where we are in the cycle.
- **DON'T:** extrapolate the recent past; follow the crowd; ignore margin of safety.

## Sir John Templeton
- **"Buy at the point of maximum pessimism"** — global, contrarian, long horizon.
- **Diversify globally**; bargains appear when headlines are worst.
- **DO:** be brutally contrarian; look worldwide; be patient decades.
- **DON'T:** chase yesterday's winners; fear the unknown market.

## Jesse Livermore (speculator, "Reminiscences")
- **Cut losses immediately**; let winners run.
- **Pyramid:** add only as a trade goes your way, never average down.
- **Sit tight** through normal corrections once in a profit.
- **The tape doesn't lie**; don't argue with the market.
- **DO:** trade in the direction of the main trend; size by risk; take a loss fast.
- **DON'T:** average down; trade every day; let a loss become a disaster.

## Script (`references/livermore.py`)
A position-sizer / risk calculator encoding Livermore's rules: given account, risk %, and
stop distance, it computes shares + the pyramid add levels. No yfinance needed — pure math.

```bash
cd <skill>/references
python3 livermore.py --account 100000 --risk 1 --entry 178 --stop 165
```

## Reality notes
- These are *judgment* skills — the scripts only encode Livermore's sizing; Munger/Marks/
  Templeton are checklists to read before every decision.
- The single biggest edge across all 9 masters: **behavioral discipline** (not selling
  winners early, not holding losers, not chasing). The checklists exist to enforce it.

## Pitfalls
- ❌ Treating checklists as a screen (they're not — they're pre-trade filters).
- ❌ Reading Munger then still overtrading.
- ❌ Contrarian for its own sake (Templeton still demands a margin of safety).

---
*Compiled 2026-08-17 from Munger, Marks "The Most Important Thing", Templeton, Livermore "Reminiscences". Not financial advice.*
