"""Jesse Livermore position sizer / risk calculator (pure math, no yfinance).
Encodes: risk R% of account, fixed stop, pyramid adds as price rises.
Run:  python3 livermore.py --account 100000 --risk 1 --entry 178 --stop 165
      python3 livermore.py --account 100000 --risk 2 --entry 100 --stop 93 --adds 3
"""
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--account", type=float, default=100000)
    ap.add_argument("--risk", type=float, default=1, help="max % of account at risk per trade")
    ap.add_argument("--entry", type=float, required=True)
    ap.add_argument("--stop", type=float, required=True)
    ap.add_argument("--adds", type=int, default=2, help="number of pyramid add levels above entry")
    a = ap.parse_args()
    risk_usd = a.account * a.risk/100.0
    per_share = a.entry - a.stop
    if per_share <= 0:
        print("ERROR: stop must be below entry"); return
    shares = int(risk_usd / per_share)
    notional = shares * a.entry
    print(f"Account ${a.account:,.0f} | risk {a.risk}% = ${risk_usd:.0f} per trade")
    print(f"Entry ${a.entry:.2f} | Stop ${a.stop:.2f} | risk/share ${per_share:.2f}")
    print(f"Initial position: {shares} shares  (~${notional:,.0f} notional, {notional/a.account*100:.1f}% of account)")
    print("Pyramid adds (Livermore: add only as it goes your way):")
    step = (a.entry - a.stop)  # each add one risk-unit above
    for i in range(1, a.adds+1):
        lvl = a.entry + step*i
        add_shares = int((risk_usd/2) / (lvl - a.stop))  # half-risk adds
        print(f"  add {i}: @ ${lvl:.2f}  +{add_shares} sh  (stop still ${a.stop:.2f})")
    print(f"If stop hit on full size: loss capped at ~${risk_usd*(1+a.adds/2):.0f} (incl. adds)")

if __name__ == "__main__":
    main()
