#!/usr/bin/env python3
"""
Test script for yfinance tools
"""

import json
from yfinance_tool import (
    get_ticker_info,
    get_historical_data,
    get_financial_statements,
    get_analyst_recommendations,
    get_calendar_events,
    get_options_data,
    get_fund_data,
    get_multiple_tickers
)

def test_yfinance_tools():
    """Test all yfinance tools with sample data"""
    
    print("Testing YFinance Tools...")
    print("=" * 50)
    
    # Test 1: Get ticker info
    print("\n1. Testing get_ticker_info for MSFT:")
    result = get_ticker_info("MSFT")
    data = json.loads(result)
    if data.get("success"):
        info = data.get("info", {})
        print(f"   Company: {info.get('longName', 'N/A')}")
        print(f"   Current Price: ${info.get('currentPrice', 'N/A')}")
        print(f"   Market Cap: ${info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else "   Market Cap: N/A")
    else:
        print(f"   Error: {data.get('error', 'Unknown error')}")
    
    # Test 2: Get historical data
    print("\n2. Testing get_historical_data for AAPL (1 month):")
    result = get_historical_data("AAPL", "1mo", "1d")
    data = json.loads(result)
    if data.get("success"):
        history = data.get("data", [])
        if history:
            latest = history[-1]
            print(f"   Latest Close: ${latest.get('Close', 'N/A')}")
            print(f"   Date: {latest.get('Date', 'N/A')}")
        print(f"   Total data points: {len(history)}")
    else:
        print(f"   Error: {data.get('error', 'Unknown error')}")
    
    # Test 3: Get financial statements
    print("\n3. Testing get_financial_statements for GOOGL (income):")
    result = get_financial_statements("GOOGL", "income")
    data = json.loads(result)
    if data.get("success"):
        statements = data.get("data", [])
        print(f"   Found {len(statements)} income statement records")
    else:
        print(f"   Error: {data.get('error', 'Unknown error')}")
    
    # Test 4: Get analyst recommendations
    print("\n4. Testing get_analyst_recommendations for TSLA:")
    result = get_analyst_recommendations("TSLA")
    data = json.loads(result)
    if data.get("success"):
        recommendations = data.get("recommendations", [])
        price_targets = data.get("price_targets", [])
        print(f"   Found {len(recommendations)} recommendations")
        print(f"   Found {len(price_targets)} price targets")
    else:
        print(f"   Error: {data.get('error', 'Unknown error')}")
    
    # Test 5: Get calendar events
    print("\n5. Testing get_calendar_events for NVDA:")
    result = get_calendar_events("NVDA")
    data = json.loads(result)
    if data.get("success"):
        calendar = data.get("calendar", [])
        print(f"   Found {len(calendar)} calendar events")
    else:
        print(f"   Error: {data.get('error', 'Unknown error')}")
    
    
    

if __name__ == "__main__":
    test_yfinance_tools() 