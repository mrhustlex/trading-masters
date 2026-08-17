"""Peter Lynch PEG (GARP) scanner (yfinance-based).
Run:  python3 peg.py AAPL NVDA APH
      python3 peg.py --universe ../../scripts/universe.txt
PEG = trailingPE / (EPS growth %). Pass if PEG <= 1 and growth positive.
"""
import sys, os, time, random, warnings, argparse
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))

def get_info(t):
    for _ in range(3):
        try: return yf.Ticker(t).info
        except Exception: pass
        time.sleep(random.uniform(1.5,4))
    return {}

def analyze(t):
    info = get_info(t)
    if not info: return None
    pe = info.get('trailingPE')
    eg = info.get('earningsGrowth')
    eg = eg if isinstance(eg,(int,float)) else None
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    if not pe or pe <= 0 or not eg or eg <= 0:
        return dict(tkr=t, price=round(price,2) if price else None, pe=round(pe,1) if pe else None,
                    growth=round(eg*100,1) if eg else None, peg=None, passed=False)
    peg = pe / (eg*100)
    passed = peg <= 1.0
    return dict(tkr=t, price=round(price,2) if price else None, pe=round(pe,1),
                growth=round(eg*100,1), peg=round(peg,2), passed=bool(passed))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", default=os.path.join(HERE,"..","..","scripts","universe.txt"))
    a = ap.parse_args()
    if a.tickers: tkrs = a.tickers
    elif os.path.exists(a.universe): tkrs = open(a.universe).read().split()
    else: tkrs = ["AAPL","NVDA","APH"]
    print(f"{'TKR':<6}{'Price':>9}{'PE':>7}{'Grw%':>7}{'PEG':>6}  PASS")
    for t in tkrs[:80]:
        r = analyze(t)
        if not r: continue
        print(f"{r['tkr']:<6}{r['price'] if r['price'] else 0:>9}{r['pe'] if r['pe'] else 0:>7}"
              f"{r['growth'] if r['growth'] else 0:>7}{r['peg'] if r['peg'] else 0:>6}  "
              f"{'YES' if r['passed'] else ''}")

if __name__ == "__main__":
    main()
