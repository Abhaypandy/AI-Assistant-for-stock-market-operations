from nsepy import get_history
from datetime import datetime, timedelta

print("Testing NSEpy with RELIANCE...")

end = datetime.now()
start = end - timedelta(days=5)

try:
    data = get_history(symbol="RELIANCE", start=start, end=end)
    
    if not data.empty:
        print("✅ NSEpy WORKS!")
        print(data.tail())
        print(f"\nColumns: {data.columns.tolist()}")
    else:
        print("❌ No data returned")
        
except Exception as e:
    print(f"❌ Error: {e}")