"""Ross Cameron momentum / HOD-breakout scanner (yfinance 1-min + daily for rel-vol).
Run:  python3 momentum.py NVDA --date 2026-08-17
      python3 momentum.py TSLA AAPL --relvol 3
Flags HOD breakouts with relative-volume spike; reports post-breakout extension %.
"""
import sys, os, argparse, warnings
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")

def get_1m(t, days=5):
    df = yf.download(t, period=f"{days}d", interval="1m", progress=False, auto_adjust=True)
    if df is None or len(df)==0: return None
    if isinstance(df.columns, pd.MultiIndex): df.columns=[c[0] for c in df.columns]
    df = df[["Open","High","Low","Close","Volume"]].copy()
    df.index = pd.to_datetime(df.index)
    return df

def get_avg_daily_vol(t):
    try:
        d = yf.download(t, period="30d", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d)==0: return None
        v = d["Volume"]
        if isinstance(v, pd.DataFrame): v = v.iloc[:,0]
        return float(v.tail(20).mean())
    except Exception:
        return None

def analyze(t, date=None, relvol_min=3.0):
    df = get_1m(t)
    if df is None: return None
    if date:
        df = df[df.index.date==pd.Timestamp(date).date()]
    if len(df)==0: return None
    d = df.between_time("09:30","15:59") if len(df)>30 else df
    adv = get_avg_daily_vol(t)
    today_vol = d["Volume"].sum()
    relvol = (today_vol/adv) if adv else None
    # HOD breakout: first time today's high exceeds the prior intraday high, on volume spike
    d["hod"] = d["High"].cummax()
    hod_break_i = None
    for i in range(1,len(d)):
        if d["High"].iloc[i] > d["High"].iloc[:i].max()*1.0 and d["Volume"].iloc[i] > 1.5*d["Volume"].iloc[max(0,i-20):i].mean():
            hod_break_i = i; break
    out = dict(tkr=t, date=str(d.index[0].date()),
               rel_vol=(round(relvol,1) if relvol else None),
               day_high=round(d["High"].max(),2), day_low=round(d["Low"].min(),2),
               close=round(d["Close"].iloc[-1],2),
               hod_breakout=False)
    if hod_break_i is not None and (relvol is None or relvol>=relvol_min):
        px = d["Close"].iloc[hod_break_i]
        after = d.iloc[hod_break_i:]
        ext = (after["High"].max()-px)/px*100
        out.update(hod_breakout=True, break_price=round(px,2),
                   break_time=str(d.index[hod_break_i].time()),
                   max_extension_pct=round(ext,1),
                   stop=round(d["Low"].iloc[hod_break_i],2))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="+")
    ap.add_argument("--date", default=None)
    ap.add_argument("--relvol", type=float, default=3.0)
    a = ap.parse_args()
    for t in a.tickers:
        r = analyze(t, a.date, a.relvol)
        if not r: print(f"{t}: no data"); continue
        if r["hod_breakout"]:
            print(f"{r['tkr']} {r['date']}: HOD BREAKOUT @ {r['break_price']} ({r['break_time']}) "
                  f"relVol={r['rel_vol']} max_ext={r['max_extension_pct']}% stop {r['stop']}")
        else:
            print(f"{r['tkr']} {r['date']}: no HOD breakout (relVol={r['rel_vol']}, "
                  f"range {r['day_low']}-{r['day_high']}, close {r['close']})")

if __name__ == "__main__":
    main()
