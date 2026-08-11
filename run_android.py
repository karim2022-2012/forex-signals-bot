#!/usr/bin/env python3
"""Lanceur Android (Pydroid 3 / Termux) avec chargement de .env."""
import os
from pathlib import Path


def load_env():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        print("⚠️  Pas de .env trouvé, valeurs du code utilisées")
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()


if __name__ == "__main__":
    load_env()
    import forex_signals
    forex_signals.TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY", forex_signals.TWELVE_DATA_API_KEY)
    forex_signals.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", forex_signals.TELEGRAM_BOT_TOKEN)
    forex_signals.TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", forex_signals.TELEGRAM_CHAT_ID)
    forex_signals.main()
