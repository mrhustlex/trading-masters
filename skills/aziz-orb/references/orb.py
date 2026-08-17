"""Andrew Aziz Opening Range Breakout + VWAP scanner (yfinance 1-min).
Run:  python3 orb.py NVDA --date 2026-08-17 --orb 15
      python3 orb.py AAPL TSLA --orb 5
Fetches last 5d of 1-min bars, slices the requested date, computes the opening
range (first N min), VWAP, and flags the FIRST long/short ORB signal + outcome.
"""
import sys, os, argparse, warnings
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")

def get_1m(t, days=5):
    df = yf.download(t, period=f"{days}d", interval="1m", progress=False, auto_adjust=True)
    if df is None or len(df)==0: return None
    # flatten multi-index columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    df = df[["Open","High","Low","Close","Volume"]].copy()
    df.index = pd.to_datetime(df.index)
    return df

def vwap(df):
    pv = (df["Close"]*df["Volume"]).cumsum()
    vol = df["Volume"].cumsum()
    return pv/vol

def analyze(t, date=None, orb_min=15):
    df = get_1m(t)
    if df is None: return None
    if date:
        day = pd.Timestamp(date).date()
        df = df[df.index.date==day]
    if len(df)==0: return None
    # only regular session 09:30-16:00
    d = df.between_time("09:30","15:59")
    if len(d)==0: d = df
    d["vwap"] = vwap(d)
    orb = d.iloc[:orb_min]
    orh, orl = orb["High"].max(), orb["Low"].min()
    # find first breakout
    sig = None
    for i in range(orb_min, len(d)):
        row = d.iloc[i]; prev = d.iloc[i-1]
        if prev["Close"] <= orh and row["Close"] > orh and row["Close"] > row["vwap"]:
            sig = ("LONG", i, row["Close"], orh, orl); break
        if prev["Close"] >= orl and row["Close"] < orl and row["Close"] < row["vwap"]:
            sig = ("SHORT", i, row["Close"], orl, orh); break
    out = dict(tkr=t, date=str(d.index[0].date()), orb_min=orb_min,
               or_high=round(orh,2), or_low=round(orl,2),
               vwap_eod=round(d["vwap"].iloc[-1],2), close_eod=round(d["Close"].iloc[-1],2),
               signal=None)
    if sig:
        kind, i, px, lvl, sl = sig
        # outcome: trail to end of day after signal
        after = d.iloc[i:]
        if kind=="LONG":
            tgt = lvl + (orh-orl)*2
            low_after = after["Low"].min()
            hit = low_after <= sl
            pnl = (after["Close"].iloc[-1]-px) if not hit else (sl-px)
        else:
            tgt = lvl - (orh-orl)*2
            high_after = after["High"].max()
            hit = high_after >= sl
            pnl = (px-after["Close"].iloc[-1]) if not hit else (px-sl)
        out.update(signal=kind, entry=round(px,2), stop=round(sl,2), target=round(tgt,2),
                   stop_hit=bool(hit), pnl_per_share=round(pnl,2))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="+")
    ap.add_argument("--date", default=None)
    ap.add_argument("--orb", type=int, default=15)
    a = ap.parse_args()
    for t in a.tickers:
        r = analyze(t, a.date, a.orb)
        if not r: print(f"{t}: no 1-min data"); continue
        if r["signal"]:
            print(f"{r['tkr']} {r['date']} ORB{r['orb_min']}: {r['signal']} @ {r['entry']} "
                  f"stop {r['stop']} tgt {r['target']} | stop_hit={r['stop_hit']} "
                  f"PnL/sh {r['pnl_per_share']}")
        else:
            print(f"{r['tkr']} {r['date']} ORB{r['orb_min']}: NO signal | "
                  f"OR {r['or_low']}-{r['or_high']} VWAP {r['vwap_eod']} close {r['close_eod']}")

if __name__ == "__main__":
    main()
