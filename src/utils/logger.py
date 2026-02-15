"""Logging utility with colored output"""

from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

class Logger:
    """Simple colored logger"""
    
    @staticmethod
    def info(message):
        print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")
    
    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def warning(message):
        print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")
    
    @staticmethod
    def error(message):
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def header(message):
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}{message}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")
    
    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")