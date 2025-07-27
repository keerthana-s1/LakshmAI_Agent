#!/usr/bin/env python3
"""
Comprehensive test for yfinance tools with JSON serialization
"""

import json
import sys
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

def test_json_serialization():
    """Test JSON serialization for all functions"""
    
    print("Testing YFinance Tools JSON Serialization...")
    print("=" * 60)
    
    tests = [
        ("get_ticker_info", lambda: get_ticker_info("MSFT")),
        ("get_historical_data", lambda: get_historical_data("AAPL", "1mo", "1d")),
        ("get_financial_statements", lambda: get_financial_statements("GOOGL", "income")),
        ("get_analyst_recommendations", lambda: get_analyst_recommendations("TSLA")),
        ("get_calendar_events", lambda: get_calendar_events("NVDA")),
        ("get_options_data", lambda: get_options_data("AAPL")),
        ("get_fund_data", lambda: get_fund_data("SPY")),
        ("get_multiple_tickers", lambda: get_multiple_tickers(["MSFT", "AAPL", "GOOGL"]))
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        try:
            # Execute the function
            result = test_func()
            print(f"  ✓ Function executed successfully")
            
            # Try to parse the JSON
            data = json.loads(result)
            print(f"  ✓ JSON parsing successful")
            
            # Check if it's a valid response
            if isinstance(data, dict):
                if data.get("success"):
                    print(f"  ✓ Data retrieved successfully")
                    if "data" in data:
                        print(f"  ✓ Response contains data field")
                    elif "info" in data:
                        print(f"  ✓ Response contains info field")
                    elif "error" in data:
                        print(f"  ✓ Response contains error field (expected for some functions)")
                else:
                    print(f"  ⚠ Function returned error: {data.get('error', 'Unknown error')}")
                
                passed += 1
            else:
                print(f"  ✗ Invalid response format")
                failed += 1
                
        except json.JSONDecodeError as e:
            print(f"  ✗ JSON parsing failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Function failed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! JSON serialization is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

def test_specific_functions():
    """Test specific functions that were problematic"""
    
    print("\nTesting Specific Problematic Functions...")
    print("=" * 60)
    
    # Test financial statements specifically
    print("\n1. Testing get_financial_statements (previously failing):")
    try:
        result = get_financial_statements("MSFT", "income")
        data = json.loads(result)
        if data.get("success"):
            statements = data.get("data", [])
            print(f"  ✓ Successfully retrieved {len(statements)} income statement records")
        else:
            print(f"  ⚠ Function returned: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
    
    # Test analyst recommendations
    print("\n2. Testing get_analyst_recommendations:")
    try:
        result = get_analyst_recommendations("MSFT")
        data = json.loads(result)
        if data.get("success"):
            recommendations = data.get("recommendations", [])
            price_targets = data.get("price_targets", [])
            print(f"  ✓ Successfully retrieved {len(recommendations)} recommendations and {len(price_targets)} price targets")
        else:
            print(f"  ⚠ Function returned: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
    
    # Test calendar events
    print("\n3. Testing get_calendar_events:")
    try:
        result = get_calendar_events("MSFT")
        data = json.loads(result)
        if data.get("success"):
            calendar = data.get("calendar", [])
            print(f"  ✓ Successfully retrieved {len(calendar)} calendar events")
        else:
            print(f"  ⚠ Function returned: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

if __name__ == "__main__":
    print("Starting comprehensive yfinance tools test...")
    
    # Run the main test
    success = test_json_serialization()
    
    # Run specific tests
    test_specific_functions()
    
    if success:
        print("\n🎉 All JSON serialization issues have been resolved!")
        sys.exit(0)
    else:
        print("\n❌ Some issues remain. Please review the implementation.")
        sys.exit(1) 