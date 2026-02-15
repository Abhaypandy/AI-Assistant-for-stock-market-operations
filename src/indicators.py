"""Technical indicators calculation module"""

import pandas as pd
import ta
from typing import Dict

class IndicatorCalculator:
    """Calculates technical indicators for stock data"""
    
    @staticmethod
    def calculate_all(df: pd.DataFrame, ema_short: int = 20, ema_long: int = 50) -> pd.DataFrame:
        """
        Calculate all required technical indicators
        
        Args:
            df: DataFrame with OHLCV data
            ema_short: Short EMA period
            ema_long: Long EMA period
        
        Returns:
            DataFrame with added indicator columns
        """
        df = df.copy()
        
        # EMAs
        df['EMA20'] = ta.trend.ema_indicator(df['Close'], window=ema_short)
        df['EMA50'] = ta.trend.ema_indicator(df['Close'], window=ema_long)
        
        # RSI
        df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
        
        # Volume analysis
        df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA']
        
        # ATR (for risk assessment)
        df['ATR'] = ta.volatility.average_true_range(
            df['High'], df['Low'], df['Close'], window=14
        )
        
        # VWAP (for intraday)
        if len(df) > 0:
            df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
        
        return df
    
    @staticmethod
    def get_latest_values(df: pd.DataFrame) -> Dict:
        """
        Extract latest indicator values
        
        Returns:
            Dictionary with current values
        """
        if df.empty or len(df) < 50:
            return None
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        return {
            'close': latest['Close'],
            'ema20': latest['EMA20'],
            'ema50': latest['EMA50'],
            'rsi': latest['RSI'],
            'volume': latest['Volume'],
            'volume_ma': latest['Volume_MA'],
            'volume_ratio': latest['Volume_Ratio'],
            'atr': latest['ATR'],
            'vwap': latest.get('VWAP', None),
            'prev_close': prev['Close']
        }