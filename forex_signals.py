#!/usr/bin/env python3
"""
Forex Signals Bot — Twelve Data + Telegram
Stratégie : EMA 9/21 + RSI 14 + Bollinger Bands (20, 2)
Alertes Telegram BUY/SELL avec score de confluence.
"""

import time
import requests
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# =================== CONFIG ===================
TWELVE_DATA_API_KEY = "54704bd0a64545d494321ac2353bb997"
TELEGRAM_BOT_TOKEN = "COLLE_TON_TOKEN_ICI"
TELEGRAM_CHAT_ID = "COLLE_TON_CHAT_ID_ICI"

FOREX_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF",
    "AUD/USD", "USD/CAD", "NZD/USD",
    "EUR/GBP", "EUR/JPY", "GBP/JPY",
    "AUD/JPY", "EUR/AUD", "GBP/CHF",
]

TIMEFRAMES = ["1min", "5min", "15min"]
SCAN_INTERVAL = 60


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 200:
            print(f"[TG] Erreur {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[TG] Exception: {e}")


def fetch_candles(symbol: str, interval: str, outputsize: int = 100) -> pd.DataFrame:
    url = "https://api.twelvedata.com/time_series"
    params = {"symbol": symbol, "interval": interval, "outputsize": outputsize, "apikey": TWELVE_DATA_API_KEY, "format": "JSON"}
    try:
        r = requests.get(url, params=params, timeout=15)
        data = r.json()
        if "values" not in data:
            return pd.DataFrame()
        df = pd.DataFrame(data["values"]).iloc[::-1].reset_index(drop=True)
        df["datetime"] = pd.to_datetime(df["datetime"])
        for col in ["open", "high", "low", "close"]:
            df[col] = df[col].astype(float)
        return df
    except Exception:
        return pd.DataFrame()


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) < 30:
        return df
    df["ema9"] = ta.ema(df["close"], length=9)
    df["ema21"] = ta.ema(df["close"], length=21)
    df["rsi"] = ta.rsi(df["close"], length=14)
    bb = ta.bbands(df["close"], length=20, std=2)
    if bb is not None:
        df["bb_lower"] = bb.iloc[:, 0]
        df["bb_mid"] = bb.iloc[:, 1]
        df["bb_upper"] = bb.iloc[:, 2]
    return df


def evaluate_signal(row, prev):
    if row is None or prev is None:
        return None, 0, []
    signals, direction = [], None
    if prev["ema9"] <= prev["ema21"] and row["ema9"] > row["ema21"]:
        direction, signals = "BUY", ["EMA9 croise EMA21 à la hausse"]
    elif prev["ema9"] >= prev["ema21"] and row["ema9"] < row["ema21"]:
        direction, signals = "SELL", ["EMA9 croise EMA21 à la baisse"]
    if row["rsi"] < 30:
        if direction is None: direction = "BUY"
        signals.append(f"RSI survendu ({row['rsi']:.1f})")
    elif row["rsi"] > 70:
        if direction is None: direction = "SELL"
        signals.append(f"RSI suracheté ({row['rsi']:.1f})")
    if row["close"] <= row["bb_lower"]:
        if direction is None: direction = "BUY"
        signals.append("Prix touche bande inf Bollinger")
    elif row["close"] >= row["bb_upper"]:
        if direction is None: direction = "SELL"
        signals.append("Prix touche bande sup Bollinger")
    if direction is None: return None, 0, []
    return direction, len(signals), signals


def compute_targets(direction: str, row):
    close, width = row["close"], (row["bb_upper"] - row["bb_lower"]) / 2
    if direction == "BUY": return close - width, close + width * 1.5
    return close + width, close - width * 1.5


def scan_pair(symbol: str, interval: str, last_alert: dict):
    df = fetch_candles(symbol, interval)
    if df.empty or len(df) < 30: return
    df = compute_indicators(df)
    row, prev = df.iloc[-1], df.iloc[-2]
    direction, score, reasons = evaluate_signal(row, prev)
    if direction is None or score < 1: return
    key = f"{symbol}-{interval}"
    now = time.time()
    if key in last_alert and now - last_alert[key] < 900: return
    sl, tp = compute_targets(direction, row)
    mult = 100 if "JPY" in symbol else 10000
    sl_pips, tp_pips = abs(row["close"] - sl) * mult, abs(tp - row["close"]) * mult
    emoji = "🟢" if direction == "BUY" else "🔴"
    msg = (f"{emoji} <b>{direction} {symbol}</b> ({interval})\n"
           f"💰 Prix: <code>{row['close']:.5f}</code>\n"
           f"🎯 TP: <code>{tp:.5f}</code> (~{tp_pips:.0f} pips)\n"
           f"🛡 SL: <code>{sl:.5f}</code> (~{sl_pips:.0f} pips)\n"
           f"📊 Confluence: {score}/3\n"
           f"📈 RSI: {row['rsi']:.1f}\n"
           f"📋 {', '.join(reasons)}\n"
           f"🕐 {datetime.now().strftime('%H:%M:%S')}")
    send_telegram(msg)
    last_alert[key] = now
    print(f"[SIGNAL] {direction} {symbol} {interval} score={score}")


def main():
    print("🚀 Forex Signals Bot démarré")
    send_telegram(f"🤖 <b>Bot Forex démarré</b>\n📊 {len(FOREX_PAIRS)} paires × {len(TIMEFRAMES)} TF\n⏱ Scan toutes les {SCAN_INTERVAL}s")
    last_alert = {}
    while True:
        print(f"\n--- Scan {datetime.now().strftime('%H:%M:%S')} ---")
        for symbol in FOREX_PAIRS:
            for tf in TIMEFRAMES:
                try:
                    scan_pair(symbol, tf, last_alert)
                    time.sleep(2)
                except Exception as e:
                    print(f"[ERR] {symbol} {tf}: {e}")
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
