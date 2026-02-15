"""Module for fetching stock market data using yahooquery"""

from yahooquery import Ticker
import pandas as pd
from typing import Optional
from src.utils.logger import Logger
import time

class DataFetcher:
    """Handles all data fetching operations using yahooquery"""
    
    def __init__(self):
        self.logger = Logger()
    
    def fetch_stock_data(
        self, 
        ticker: str, 
        period: str = "60d", 
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data using yahooquery
        
        Args:
            ticker: Stock symbol (e.g., 'RELIANCE.NS')
            period: Data period (e.g., '5d', '1mo', '3mo', '1y', '2y')
            interval: Data interval (e.g., '1d', '1h', '15m', '5m')
        
        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            # Create ticker object
            stock = Ticker(ticker)
            
            # Fetch data
            data = stock.history(period=period, interval=interval)
            
            # Check if data is valid
            if isinstance(data, str):
                # Error message returned
                self.logger.warning(f"Error for {ticker}: {data}")
                return None
            
            if not isinstance(data, pd.DataFrame) or data.empty:
                self.logger.warning(f"No data for {ticker}")
                return None
            
            # Handle multi-index (symbol, date)
            if isinstance(data.index, pd.MultiIndex):
                # Remove the symbol level, keep only date
                data = data.reset_index(level=0, drop=True)
            
            # Standardize column names (yahooquery uses lowercase)
            data.columns = [col.capitalize() for col in data.columns]
            
            # Rename 'Adjclose' to match our indicators
            if 'Adjclose' in data.columns:
                data = data.rename(columns={'Adjclose': 'Adj Close'})
            
            return data
        
        except Exception as e:
            self.logger.error(f"Error fetching {ticker}: {str(e)}")
            return None
    
    def fetch_multiple_stocks(
        self, 
        tickers: list, 
        period: str = "60d",
        interval: str = "1d"
    ) -> dict:
        """
        Fetch data for multiple stocks
        
        Args:
            tickers: List of stock symbols
            period: Data period
            interval: Data interval
        
        Returns:
            Dictionary {ticker: dataframe}
        """
        results = {}
        total = len(tickers)
        
        self.logger.info(f"Fetching data for {total} stocks...")
        
        # Process in batches to avoid overwhelming the API
        batch_size = 10
        
        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i+batch_size]
            
            for ticker in batch:
                idx = tickers.index(ticker) + 1
                
                if idx % 10 == 0 or idx == 1:
                    self.logger.info(f"Progress: {idx}/{total} stocks...")
                
                data = self.fetch_stock_data(ticker, period, interval)
                
                if data is not None and not data.empty:
                    results[ticker] = data
            
            # Small delay between batches
            if i + batch_size < len(tickers):
                time.sleep(1)
        
        self.logger.success(f"Successfully fetched {len(results)}/{total} stocks")
        return results