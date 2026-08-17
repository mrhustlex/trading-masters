# trading-masters

Scanner skills + scripts for the **greatest swing / momentum trading masters**, each
distilled into a layman-replicable method and a runnable yfinance screen.

> ⚠️ **Education only. Not financial advice.** Past performance ≠ future results.

## The masters included

| Master | Method | Skill | Script | The "job" |
|---|---|---|---|---|
| **Mark Minervini** | SEPA / VCP | `minervini-vcp-scanner` (separate repo) | `minervini_scanner.py` | The *timing* — buy VCP breakouts |
| **William O'Neil** | CAN SLIM | `oneil-canslim/` | `canslim.py` | The *which* — strongest fundamentals + pivot breakout |
| **Stan Weinstein** | Stage Analysis | `weinstein-stage/` | `stage.py` | The *when* — only trade Stage 2 |
| **Nicolas Darvas** | Box Theory (+ Livermore) | `darvas-box/` | `darvas.py` | The *box* — break above box, stop below floor |
| **Richard Wyckoff** | Accumulation/Distribution | `wyckoff/` | `wyckoff.py` | The *smart-money* read — spring = buy |

**How they stack:** CAN SLIM finds the name → Weinstein confirms the stage → Minervini
times the VCP breakout → Darvas manages the box/stop → Wyckoff reads the institution.
All agree on the core: **trend + volume + tight risk, never average down.**

## Install

```bash
pip install yfinance pandas numpy mplfinance
```

## Quick start (per method)

```bash
# O'Neil
python3 oneil-canslim/references/canslim.py NVDA APH
python3 oneil-canslim/references/canslim.py --universe scripts/universe.txt

# Weinstein
python3 weinstein-stage/references/stage.py NVDA APH SMCI SNDK

# Darvas
python3 darvas-box/references/darvas.py NVDA APH

# Wyckoff (weekly accumulation/spring)
python3 wyckoff/references/wyckoff.py NVDA APH

# Minervini (parabola-safe VCP)
python3 scripts/minervini_scanner.py          # or import + analyze()
python3 -c "import scanner,yfinance as yf; h=yf.Ticker('SNDK').history('1y'); c=h['Close']; m=c.rolling(200).mean().iloc[-1]; print(scanner.detect_parabola(c,m))"
```

## Common principles across all masters
- **Cut losses fast** (7–8% hard stop). Never average down.
- **Buy strength, not weakness** — breakouts, not falling knives.
- **Volume confirms** the move or it's noise.
- **Trend is your friend** until it isn't (check the stage / market).
- **Parabolas are exits, not entries** — `detect_parabola()` flags them.

## Files
```
skills/oneil-canslim/      SKILL.md + references/canslim.py
skills/weinstein-stage/    SKILL.md + references/stage.py
skills/darvas-box/         SKILL.md + references/darvas.py
skills/wyckoff/            SKILL.md + references/wyckoff.py
scripts/                   universe.txt, minervini_scanner.py (with detect_parabola)
README.md
```

## License
MIT
