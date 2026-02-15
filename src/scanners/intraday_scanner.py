"""Intraday trading scanner (15-minute timeframe)"""

from typing import Dict, List
import config.settings as settings

class IntradayScanner:
    """Identifies intraday trading opportunities"""
    
    def __init__(self):
        self.qualified_stocks = []
    
    def scan(self, stock_data: Dict) -> List[Dict]:
        """
        Scan stocks for intraday setups
        
        Args:
            stock_data: Dict of {ticker: indicator_values}
        
        Returns:
            List of qualified stocks with scores
        """
        self.qualified_stocks = []
        
        for ticker, indicators in stock_data.items():
            if indicators is None:
                continue
            
            if self._qualifies_for_intraday(indicators):
                score = self._calculate_intraday_score(indicators)
                
                self.qualified_stocks.append({
                    'ticker': ticker,
                    'score': score,
                    'indicators': indicators,
                    'status': self._get_status(indicators)
                })
        
        # Sort by score
        self.qualified_stocks.sort(key=lambda x: x['score'], reverse=True)
        
        return self.qualified_stocks[:settings.TOP_N_STOCKS]
    
    def _qualifies_for_intraday(self, ind: Dict) -> bool:
        """Check if stock meets intraday criteria"""
        
        # Must have VWAP
        if ind['vwap'] is None:
            return False
        
        # Price above VWAP (bullish bias)
        if ind['close'] <= ind['vwap']:
            return False
        
        # EMA20 > EMA50 (momentum)
        if ind['ema20'] <= ind['ema50']:
            return False
        
        # RSI not extreme
        if not (settings.INTRADAY_RSI_MIN <= ind['rsi'] <= settings.INTRADAY_RSI_MAX):
            return False
        
        return True
    
    def _calculate_intraday_score(self, ind: Dict) -> float:
        """Calculate intraday score (0-100)"""
        
        score = 0
        
        # Distance from VWAP (30 points)
        vwap_distance = ((ind['close'] - ind['vwap']) / ind['vwap']) * 100
        score += min(vwap_distance * 30, 30)
        
        # Volume spike (40 points)
        volume_score = min((ind['volume_ratio'] - 1) * 20, 40)
        score += volume_score
        
        # RSI momentum (30 points)
        rsi_score = (ind['rsi'] - 50) * 0.6
        score += max(rsi_score, 0)
        
        return round(score, 2)
    
    def _get_status(self, ind: Dict) -> str:
        """Determine entry status"""
        
        # Volume dried up
        if ind['volume_ratio'] < 0.8:
            return "WAIT (Low volume)"
        
        # Too far from VWAP
        vwap_dist = abs(ind['close'] - ind['vwap']) / ind['vwap']
        if vwap_dist > 0.02:
            return "WAIT (Far from VWAP)"
        
        return "READY"