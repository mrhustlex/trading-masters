"""Nicolas Darvas Box Theory detector (+ Livermore trailing stop). yfinance-based.
Run:  python3 darvas.py NVDA APH
      python3 darvas.py --universe universe.txt --box 20
Prints current box floor/ceiling, breakout flag, trailing stop (box floor).
"""
import sys, os, time, random, warnings, argparse
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))

def get_hist(t, period="1y"):
    for _ in range(3):
        try:
            h = yf.Ticker(t).history(period=period)
            h = h[['High','Low','Close','Volume']].dropna()
            if len(h) > 120: return h
        except Exception: pass
        time.sleep(random.uniform(1.5,4))
    return None

def analyze(t, box=20):
    h = get_hist(t, period="6mo")
    if h is None: return None
    close, high, low, vol = h['Close'], h['High'], h['Low'], h['Volume']
    price = close.iloc[-1]
    win_h = high.iloc[-box:]; win_l = low.iloc[-box:]
    floor = win_l.min(); ceiling = win_h.max()
    # also previous box for pyramidal check
    prev_h = high.iloc[-2*box:-box]; prev_l = low.iloc[-2*box:-box]
    prev_ceiling = prev_h.max() if len(prev_h) else ceiling
    vma = vol.iloc[-50:].mean()
    vol_ok = vol.iloc[-1] > 1.4*vma
    breakout = (price > ceiling) and vol_ok
    # trailing stop = most recent box floor (Livermore)
    stop = floor*0.99
    target = ceiling*1.20 if breakout else None
    return dict(tkr=t, price=round(price,2), floor=round(floor,2), ceiling=round(ceiling,2),
                prev_ceiling=round(prev_ceiling,2), breakout=breakout, vol_ok=vol_ok,
                stop=round(stop,2), target=(round(target,2) if target else None),
                new_high_box=(ceiling > prev_ceiling))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", default=os.path.join(HERE,"..","universe.txt"))
    ap.add_argument("--box", type=int, default=20)
    a = ap.parse_args()
    if a.tickers: tkrs = a.tickers
    elif os.path.exists(a.universe): tkrs = open(a.universe).read().split()
    else: tkrs = ["NVDA","APH"]
    print(f"{'TKR':<6}{'Price':>9}  Floor  Ceiling  break  vol   stop   newBox")
    for t in tkrs[:60]:
        r = analyze(t, a.box)
        if not r: continue
        print(f"{r['tkr']:<6}{r['price']:>9}  {r['floor']:>6}{r['ceiling']:>8}  "
              f"{'YES' if r['breakout'] else '':<5}  {'YES' if r['vol_ok'] else '':<4}  "
              f"{r['stop']:>7}  {'YES' if r['new_high_box'] else ''}")

if __name__ == "__main__":
    main()
