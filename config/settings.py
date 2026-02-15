"""Global configuration settings"""

# Data fetching settings
DATA_PERIOD_SWING = "60d"      # 60 days for swing analysis
DATA_PERIOD_INTRADAY = "5d"    # 5 days for intraday
INTRADAY_INTERVAL = "15m"      # 15-minute candles

# Indicator parameters
EMA_SHORT = 20
EMA_LONG = 50
RSI_PERIOD = 14
VOLUME_PERIOD = 20

# Swing scanner thresholds (RELAXED)
SWING_RSI_MIN = 35              # Lowered from 40
SWING_RSI_MAX = 75              # Raised from 70
SWING_MIN_VOLUME_RATIO = 0.8    # Lowered from 1.0

# Intraday scanner thresholds (RELAXED)
INTRADAY_RSI_MIN = 40           # Lowered from 45
INTRADAY_RSI_MAX = 70           # Raised from 65
INTRADAY_VOLUME_SPIKE = 0.8     # Lowered from 1.5

# Output settings
TOP_N_STOCKS = 3
OUTPUT_DIR = "outputs"