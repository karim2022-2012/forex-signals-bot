# 📈 Forex Signals Bot

Bot Python qui envoie des **signaux Forex BUY/SELL** sur Telegram en se basant sur :

- **EMA** 9 / 21 (tendance court terme)
- **RSI** 14 (survendu / suracheté)
- **Bollinger Bands** 20, 2 (volatilité & extrêmes)

Chaque signal est accompagné d'un **score de confluence** (1 à 3), du prix d'entrée, du **Take Profit** et du **Stop Loss** (calculés sur la largeur des bandes de Bollinger).

## ✨ Fonctionnalités

- 📊 13 paires majeures (EUR/USD, GBP/USD, USD/JPY, etc.)
- ⏱ 3 timeframes : `1min`, `5min`, `15min`
- 🎯 TP / SL dynamiques (1.5× la demi-largeur BB)
- 🚫 Anti-doublon : 1 alerte max par paire / TF toutes les 15 min
- 📲 Alertes Telegram formatées en HTML
- 🆓 Compatible plan gratuit Twelve Data (8 req/min, 800/jour)

## 🚀 Installation

```bash
git clone https://github.com/karim2022-2012/forex-signals-bot.git
cd forex-signals-bot
pip install -r requirements.txt
```

### 🔑 Configuration

Copie `.env.example` en `.env` et remplis tes clés :

- **Twelve Data** : crée un compte sur [twelvedata.com](https://twelvedata.com) → API Key
- **Telegram Bot** : parle à [@BotFather](https://t.me/BotFather) → `/newbot` → récupère le token
- **chat_id** : envoie un message à ton bot puis va sur `https://api.telegram.org/bot<TOKEN>/getUpdates`

### ▶️ Lancer

```bash
python forex_signals.py
```

## 📱 Exemple d'alerte Telegram

```
🟢 BUY EUR/USD (5min)
💰 Prix: 1.08542
🎯 TP: 1.08712 (~17 pips)
🛡 SL: 1.08477 (~6 pips)
📊 Confluence: 2/3
📈 RSI: 28.4
📋 EMA9 croise EMA21 à la hausse, RSI survendu (28.4)
🕐 14:32:15
```

## 📂 Structure

```
forex-signals-bot/
├── forex_signals.py      # Bot principal
├── run_android.py        # Lanceur Android (charge .env)
├── requirements.txt      # Dépendances Python
├── .env.example          # Template de config
├── .gitignore            # Fichiers ignorés
└── README.md             # Ce fichier
```

## 📱 Sur Android (Pydroid 3)

```bash
pip install -r requirements.txt
python run_android.py
```

## ⚙️ Personnalisation

Édite le début de `forex_signals.py` :

| Variable | Défaut | Description |
|----------|--------|-------------|
| `FOREX_PAIRS` | 13 majeures | Liste des paires à scanner |
| `TIMEFRAMES` | 1min/5min/15min | Timeframes analysés |
| `SCAN_INTERVAL` | 60s | Pause entre deux cycles complets |
| Anti-doublon | 900s | Délai min entre 2 alertes sur la même paire/TF |

## ⚠️ Avertissement

Ce bot est fourni à des fins **éducatives uniquement**. Le trading comporte des risques importants de perte en capital. Trade responsable — teste toujours sur un compte démo avant.

## 📜 Licence
MIT
