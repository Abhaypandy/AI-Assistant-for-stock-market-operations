"""Swing trading scanner (Daily timeframe)"""

from typing import Dict, List
import config.settings as settings

class SwingScanner:
    """Identifies swing trading opportunities"""
    
    def __init__(self):
        self.qualified_stocks = []
    
    def scan(self, stock_data: Dict) -> List[Dict]:
        """
        Scan stocks for swing trading setups
        
        Args:
            stock_data: Dict of {ticker: indicator_values}
        
        Returns:
            List of qualified stocks with scores
        """
        self.qualified_stocks = []
        
        for ticker, indicators in stock_data.items():
            if indicators is None:
                continue
            
            if self._qualifies_for_swing(indicators):
                score = self._calculate_swing_score(indicators)
                
                self.qualified_stocks.append({
                    'ticker': ticker,
                    'score': score,
                    'indicators': indicators,
                    'status': self._get_status(indicators)
                })
        
        # Sort by score
        self.qualified_stocks.sort(key=lambda x: x['score'], reverse=True)
        
        return self.qualified_stocks[:settings.TOP_N_STOCKS]
    
    def _qualifies_for_swing(self, ind: Dict) -> bool:
        """Check if stock meets swing criteria"""
        
        # Price > EMA20 > EMA50 (uptrend)
        if not (ind['close'] > ind['ema20'] > ind['ema50']):
            return False
        
        # RSI in healthy range
        if not (settings.SWING_RSI_MIN <= ind['rsi'] <= settings.SWING_RSI_MAX):
            return False
        
        # Volume not too weak
        if ind['volume_ratio'] < settings.SWING_MIN_VOLUME_RATIO:
            return False
        
        return True
    
    def _calculate_swing_score(self, ind: Dict) -> float:
        """Calculate swing trading score (0-100)"""
        
        score = 0
        
        # Trend strength (40 points)
        ema_gap = ((ind['ema20'] - ind['ema50']) / ind['ema50']) * 100
        score += min(ema_gap * 10, 40)
        
        # RSI positioning (30 points)
        # Best around 50-60
        rsi_score = 30 - abs(ind['rsi'] - 55) * 0.5
        score += max(rsi_score, 0)
        
        # Volume (30 points)
        volume_score = min(ind['volume_ratio'] * 15, 30)
        score += volume_score
        
        return round(score, 2)
    
    def _get_status(self, ind: Dict) -> str:
        """Determine entry status"""
        
        # Price pulled back to EMA20
        if abs(ind['close'] - ind['ema20']) / ind['ema20'] < 0.01:
            return "READY"
        
        # RSI overextended
        if ind['rsi'] > 68:
            return "WAIT (RSI high)"
        
        return "READY"