#!/usr/bin/env python3
"""
Simple test for the JSON serialization fix
"""

import json
from yfinance_tool import get_financial_statements

def test_financial_statements():
    """Test the financial statements function with JSON serialization"""
    
    print("Testing financial statements JSON serialization...")
    
    try:
        # Test with a simple case first
        result = get_financial_statements("MSFT", "income")
        print("✓ Financial statements function executed successfully")
        
        # Try to parse the JSON
        data = json.loads(result)
        print("✓ JSON parsing successful")
        
        if data.get("success"):
            print("✓ Data retrieved successfully")
            statements = data.get("data", [])
            print(f"✓ Found {len(statements)} income statement records")
        else:
            print(f"✗ Error: {data.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    test_financial_statements() 