# """AI-powered analysis using Claude"""

# import os
# from anthropic import Anthropic
# from dotenv import load_dotenv
# from typing import List, Dict
# from src.utils.logger import Logger

# load_dotenv()

# class AIAnalyzer:
#     """Generates AI-powered explanations for scan results"""
    
#     def __init__(self):
#         self.logger = Logger()
#         api_key = os.getenv("ANTHROPIC_API_KEY")
        
#         if not api_key:
#             self.logger.warning("ANTHROPIC_API_KEY not found. AI analysis will be skipped.")
#             self.client = None
#         else:
#             self.client = Anthropic(api_key=api_key)
    
#     def analyze_results(
#         self, 
#         swing_picks: List[Dict], 
#         intraday_picks: List[Dict],
#         scan_type: str = "daily"
#     ) -> str:
#         """
#         Generate AI explanation for scan results
        
#         Args:
#             swing_picks: Top swing stocks
#             intraday_picks: Top intraday stocks
#             scan_type: Type of scan performed
        
#         Returns:
#             AI-generated analysis as string
#         """
#         if not self.client:
#             return "⚠️  AI analysis unavailable (API key not configured)"
        
#         prompt = self._build_prompt(swing_picks, intraday_picks, scan_type)
        
#         try:
#             self.logger.info("Generating AI analysis...")
            
#             response = self.client.messages.create(
#                 model="claude-sonnet-4-20250514",
#                 max_tokens=1000,
#                 messages=[{
#                     "role": "user",
#                     "content": prompt
#                 }]
#             )
            
#             return response.content[0].text
        
#         except Exception as e:
#             self.logger.error(f"AI analysis failed: {str(e)}")
#             return f"⚠️  AI analysis unavailable: {str(e)}"
    
"""AI-powered analysis using Groq"""

import os
from groq import Groq  # Changed from anthropic
from dotenv import load_dotenv
from typing import List, Dict
from src.utils.logger import Logger

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.logger = Logger()
        # Change the variable name in your .env file to GROQ_API_KEY
        api_key = os.getenv("GROQ_API_KEY") 
        
        if not api_key:
            self.logger.warning("GROQ_API_KEY not found. AI analysis will be skipped.")
            self.client = None
        else:
            self.client = Groq(api_key=api_key) # Changed to Groq client
    
    def analyze_results(self, swing_picks: List[Dict], intraday_picks: List[Dict], scan_type: str = "daily") -> str:
        if not self.client:
            return "⚠️ AI analysis unavailable (API key not configured)"
        
        prompt = self._build_prompt(swing_picks, intraday_picks, scan_type)
        
        try:
            self.logger.info("Generating AI analysis via Groq...")
            
            # Updated for Groq's syntax and model
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile", # <--- THIS is your new model
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            self.logger.error(f"AI analysis failed: {str(e)}")
            return f"⚠️ AI analysis unavailable: {str(e)}"

  
    
    
    
    
    
    
    def _build_prompt(self, swing: List, intraday: List, scan_type: str) -> str:
        """Build prompt for Claude"""
        
        prompt = f"""You are a professional stock market analyst. Analyze these NIFTY 50 scan results and provide a brief, actionable summary.

📊 SCAN TYPE: {scan_type.upper()}

🟦 SWING PICKS (Daily Timeframe):
"""
        
        for i, stock in enumerate(swing, 1):
            ind = stock['indicators']
            prompt += f"""
{i}. {stock['ticker'].replace('.NS', '')} - Score: {stock['score']}/100
   • Close: ₹{ind['close']:.2f}
   • EMA20: ₹{ind['ema20']:.2f} | EMA50: ₹{ind['ema50']:.2f}
   • RSI: {ind['rsi']:.1f}
   • Volume Ratio: {ind['volume_ratio']:.2f}x
   • Status: {stock['status']}
"""
        
        prompt += "\n🟥 INTRADAY PICKS (15-min Timeframe):\n"
        
        for i, stock in enumerate(intraday, 1):
            ind = stock['indicators']
            prompt += f"""
{i}. {stock['ticker'].replace('.NS', '')} - Score: {stock['score']}/100
   • Close: ₹{ind['close']:.2f} | VWAP: ₹{ind['vwap']:.2f}
   • RSI: {ind['rsi']:.1f}
   • Volume Ratio: {ind['volume_ratio']:.2f}x
   • Status: {stock['status']}
"""
        
        prompt += """

Provide a concise analysis covering:
1. Market sentiment (2 sentences)
2. Why these swing picks are strong (1-2 sentences)
3. Why these intraday picks show momentum (1-2 sentences)
4. Any risk warnings (1 sentence)

Keep it professional, actionable, and under 150 words total."""
        
        return prompt