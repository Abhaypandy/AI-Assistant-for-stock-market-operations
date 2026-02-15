"""
NIFTY 50 AI-Powered Stock Scanner
Main execution file
"""

import os
from datetime import datetime
from config.nifty50 import get_nifty50_tickers
import config.settings as settings
from src.data_fetcher import DataFetcher
from src.indicators import IndicatorCalculator
from src.scanners.swing_scanner import SwingScanner
from src.scanners.intraday_scanner import IntradayScanner
from src.ai_analyzer import AIAnalyzer
from src.utils.logger import Logger

def main():
    """Main execution flow"""
    
    logger = Logger()
    logger.header(f"🚀 NIFTY 50 AI SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize components
    fetcher = DataFetcher()
    calculator = IndicatorCalculator()
    swing_scanner = SwingScanner()
    intraday_scanner = IntradayScanner()
    ai_analyzer = AIAnalyzer()
    
    # Get NIFTY 50 tickers
    tickers = get_nifty50_tickers()
    logger.info(f"Scanning {len(tickers)} NIFTY 50 stocks...")
    
    # ========== SWING ANALYSIS (Daily) ==========
    logger.header("📊 SWING SCANNER (Daily Timeframe)")
    
    swing_data_raw = fetcher.fetch_multiple_stocks(
        tickers, 
        period=settings.DATA_PERIOD_SWING,
        interval="1d"
    )
    
    swing_data_processed = {}
    for ticker, df in swing_data_raw.items():
        df_with_indicators = calculator.calculate_all(df)
        swing_data_processed[ticker] = calculator.get_latest_values(df_with_indicators)
    
    swing_picks = swing_scanner.scan(swing_data_processed)
    
    # Display swing results
    print(f"\n{Fore.BLUE}{'='*60}")
    print(f"{Fore.BLUE}🟦 TOP {settings.TOP_N_STOCKS} SWING PICKS")
    print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}\n")
    
    for i, pick in enumerate(swing_picks, 1):
        ind = pick['indicators']
        ticker_clean = pick['ticker'].replace('.NS', '')
        
        print(f"{Fore.CYAN}{i}. {ticker_clean} - {pick['status']}")
        print(f"   Score: {pick['score']}/100")
        print(f"   Close: ₹{ind['close']:.2f} | EMA20: ₹{ind['ema20']:.2f} | EMA50: ₹{ind['ema50']:.2f}")
        print(f"   RSI: {ind['rsi']:.1f} | Vol Ratio: {ind['volume_ratio']:.2f}x{Style.RESET_ALL}\n")
    
    # ========== INTRADAY ANALYSIS (15-min) ==========
    logger.header("⚡ INTRADAY SCANNER (15-min Timeframe)")
    
    intraday_data_raw = fetcher.fetch_multiple_stocks(
        tickers,
        period=settings.DATA_PERIOD_INTRADAY,
        interval=settings.INTRADAY_INTERVAL
    )
    
    intraday_data_processed = {}
    for ticker, df in intraday_data_raw.items():
        df_with_indicators = calculator.calculate_all(df)
        intraday_data_processed[ticker] = calculator.get_latest_values(df_with_indicators)
    
    intraday_picks = intraday_scanner.scan(intraday_data_processed)
    
    # Display intraday results
    print(f"\n{Fore.RED}{'='*60}")
    print(f"{Fore.RED}🟥 TOP {settings.TOP_N_STOCKS} INTRADAY PICKS")
    print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}\n")
    
    for i, pick in enumerate(intraday_picks, 1):
        ind = pick['indicators']
        ticker_clean = pick['ticker'].replace('.NS', '')
        
        print(f"{Fore.YELLOW}{i}. {ticker_clean} - {pick['status']}")
        print(f"   Score: {pick['score']}/100")
        print(f"   Close: ₹{ind['close']:.2f} | VWAP: ₹{ind['vwap']:.2f}")
        print(f"   RSI: {ind['rsi']:.1f} | Vol Ratio: {ind['volume_ratio']:.2f}x{Style.RESET_ALL}\n")
    
    # ========== AI ANALYSIS ==========
    logger.header("🤖 AI ANALYSIS")
    
    ai_summary = ai_analyzer.analyze_results(swing_picks, intraday_picks)
    print(f"\n{ai_summary}\n")
    
    # ========== SAVE REPORT ==========
    save_report(swing_picks, intraday_picks, ai_summary, logger)
    
    logger.success("✅ Scan complete!")

def save_report(swing_picks, intraday_picks, ai_summary, logger):
    """Save results to file"""
    
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    
    filename = f"{settings.OUTPUT_DIR}/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"NIFTY 50 SCANNER REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n\n")
        
        f.write(f"🟦 SWING PICKS (Daily)\n")
        f.write(f"{'-'*60}\n")
        for i, pick in enumerate(swing_picks, 1):
            ind = pick['indicators']
            f.write(f"{i}. {pick['ticker'].replace('.NS', '')} - {pick['status']}\n")
            f.write(f"   Score: {pick['score']}/100\n")
            f.write(f"   Close: ₹{ind['close']:.2f} | EMA20: ₹{ind['ema20']:.2f} | EMA50: ₹{ind['ema50']:.2f}\n")
            f.write(f"   RSI: {ind['rsi']:.1f} | Vol Ratio: {ind['volume_ratio']:.2f}x\n\n")
        
        f.write(f"\n🟥 INTRADAY PICKS (15-min)\n")
        f.write(f"{'-'*60}\n")
        for i, pick in enumerate(intraday_picks, 1):
            ind = pick['indicators']
            f.write(f"{i}. {pick['ticker'].replace('.NS', '')} - {pick['status']}\n")
            f.write(f"   Score: {pick['score']}/100\n")
            f.write(f"   Close: ₹{ind['close']:.2f} | VWAP: ₹{ind['vwap']:.2f}\n")
            f.write(f"   RSI: {ind['rsi']:.1f} | Vol Ratio: {ind['volume_ratio']:.2f}x\n\n")
        
        f.write(f"\n🤖 AI ANALYSIS\n")
        f.write(f"{'-'*60}\n")
        f.write(ai_summary)
    
    logger.success(f"Report saved: {filename}")

if __name__ == "__main__":
    # Add missing import
    from colorama import Fore, Style
    main()