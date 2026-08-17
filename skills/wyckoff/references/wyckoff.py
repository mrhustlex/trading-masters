"""Richard Wyckoff accumulation-range + spring detector (yfinance-based, weekly).
Run:  python3 wyckoff.py NVDA APH
      python3 wyckoff.py --universe universe.txt
Detects: horizontal range (Phase B), recent spring (new low below range then recovery) on
LOW volume (supply exhausted) -> high-probability accumulation entry zone.
"""
import sys, os, time, random, warnings, argparse
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))

def get_weekly(t, period="2y"):
    for _ in range(3):
        try:
            h = yf.Ticker(t).history(period=period, interval="1wk")
            h = h[['High','Low','Close','Volume']].dropna()
            if len(h) > 40: return h
        except Exception: pass
        time.sleep(random.uniform(1.5,4))
    return None

def analyze(t):
    h = get_weekly(t)
    if h is None: return None
    close, high, low, vol = h['Close'], h['High'], h['Low'], h['Volume']
    price = close.iloc[-1]
    # range detection over last ~30 weeks: tightness
    win = close.iloc[-30:]
    rng_pct = (win.max()-win.min())/win.mean()
    is_range = rng_pct < 0.25
    support = win.min(); resistance = win.max()
    # spring: a recent weekly low below support, then close back inside range, on lower vol
    recent_low = low.iloc[-8:].min()
    spring = (recent_low < support*0.98) and (price > support)
    spring_vol = vol.iloc[-8:].mean() < vol.iloc[-30:-8].mean()
    valid = is_range and spring and spring_vol
    return dict(tkr=t, price=round(price,2), range_tight=is_range,
                support=round(support,2), resistance=round(resistance,2),
                spring=spring, spring_low_vol=spring_vol, accumulation=valid)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", default=os.path.join(HERE,"..","universe.txt"))
    a = ap.parse_args()
    if a.tickers: tkrs = a.tickers
    elif os.path.exists(a.universe): tkrs = open(a.universe).read().split()
    else: tkrs = ["NVDA","APH"]
    print(f"{'TKR':<6}{'Price':>9}  tight?  support  resist  spring  lowVol  ACCUM?")
    for t in tkrs[:60]:
        r = analyze(t)
        if not r: continue
        print(f"{r['tkr']:<6}{r['price']:>9}  {'Y' if r['range_tight'] else '-':<6}  "
              f"{r['support']:>7}{r['resistance']:>7}  {'Y' if r['spring'] else '-':<6}  "
              f"{'Y' if r['spring_low_vol'] else '-':<6}  {'YES' if r['accumulation'] else ''}")

if __name__ == "__main__":
    main()
