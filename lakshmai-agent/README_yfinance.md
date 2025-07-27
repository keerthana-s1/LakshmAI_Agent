# YFinance Tools for LakshmAI Agent

This document describes the yfinance tools implementation for the LakshmAI agent, providing comprehensive financial data access capabilities.

## Overview

The yfinance tools provide access to real-time and historical financial data for stocks, ETFs, and other securities. The implementation includes 8 main functions that cover all major aspects of financial data analysis.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The yfinance library will be automatically installed along with other dependencies.

## Available Tools

### 1. `get_ticker_info(symbol: str)`
Get comprehensive information about a ticker symbol.

**Parameters:**
- `symbol`: Stock symbol (e.g., 'MSFT', 'AAPL', 'GOOGL')

**Returns:**
- Company information including current price, market cap, P/E ratio, sector, etc.

**Example:**
```python
result = get_ticker_info("MSFT")
```

### 2. `get_historical_data(symbol: str, period: str = "1mo", interval: str = "1d")`
Get historical price data for a ticker.

**Parameters:**
- `symbol`: Stock symbol
- `period`: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
- `interval`: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')

**Returns:**
- Historical price data with OHLCV (Open, High, Low, Close, Volume) information

**Example:**
```python
result = get_historical_data("AAPL", "1mo", "1d")
```

### 3. `get_financial_statements(symbol: str, statement_type: str = "income")`
Get financial statements for a ticker.

**Parameters:**
- `symbol`: Stock symbol
- `statement_type`: Type of statement ('income', 'balance', 'cashflow')

**Returns:**
- Financial statement data (income statement, balance sheet, or cash flow statement)

**Example:**
```python
result = get_financial_statements("GOOGL", "income")
```

### 4. `get_analyst_recommendations(symbol: str)`
Get analyst recommendations and price targets for a ticker.

**Parameters:**
- `symbol`: Stock symbol

**Returns:**
- Analyst recommendations and price targets

**Example:**
```python
result = get_analyst_recommendations("TSLA")
```

### 5. `get_calendar_events(symbol: str)`
Get calendar events for a ticker (earnings, dividends, etc.).

**Parameters:**
- `symbol`: Stock symbol

**Returns:**
- Calendar events including earnings dates, dividend dates, etc.

**Example:**
```python
result = get_calendar_events("NVDA")
```

### 6. `get_options_data(symbol: str, expiration_date: Optional[str] = None)`
Get options data for a ticker.

**Parameters:**
- `symbol`: Stock symbol
- `expiration_date`: Specific expiration date (optional)

**Returns:**
- Options chain data including calls and puts

**Example:**
```python
result = get_options_data("AAPL")
```

### 7. `get_fund_data(symbol: str)`
Get fund data for ETFs and mutual funds.

**Parameters:**
- `symbol`: Fund symbol (e.g., 'SPY', 'QQQ')

**Returns:**
- Fund information including description, top holdings, etc.

**Example:**
```python
result = get_fund_data("SPY")
```

### 8. `get_multiple_tickers(symbols: List[str])`
Get data for multiple tickers at once.

**Parameters:**
- `symbols`: List of stock symbols

**Returns:**
- Information for all requested tickers

**Example:**
```python
result = get_multiple_tickers(["MSFT", "AAPL", "GOOGL"])
```

## Integration with Agent

The yfinance tools are integrated into the main agent through the `agent.py` file. Each tool is wrapped as an `Agent` with appropriate descriptions for the LLM to understand when and how to use them.

## Testing

Run the test script to verify that all tools work correctly:

```bash
python test_yfinance.py
```

This will test all 8 yfinance tools with sample data and display the results.

## Error Handling

All tools include comprehensive error handling:
- Network errors are caught and reported
- Invalid symbols are handled gracefully
- Missing data is handled appropriately
- All responses include a `success` field indicating whether the operation succeeded

## Response Format

All tools return JSON-formatted strings with the following structure:

```json
{
  "success": true/false,
  "symbol": "TICKER",
  "data": {...},
  "error": "error message" (if success is false)
}
```

## Usage Examples

### Basic Stock Information
```python
# Get current stock information
info = get_ticker_info("MSFT")
print(f"Microsoft current price: ${json.loads(info)['info']['currentPrice']}")
```

### Historical Data Analysis
```python
# Get 6 months of daily data
history = get_historical_data("AAPL", "6mo", "1d")
data = json.loads(history)
if data['success']:
    print(f"Retrieved {len(data['data'])} data points")
```

### Financial Analysis
```python
# Get income statement
income = get_financial_statements("GOOGL", "income")
balance = get_financial_statements("GOOGL", "balance")
cashflow = get_financial_statements("GOOGL", "cashflow")
```

### Options Trading
```python
# Get options data
options = get_options_data("TSLA")
data = json.loads(options)
if data['success']:
    calls = data['calls']
    puts = data['puts']
    print(f"Found {len(calls)} call options and {len(puts)} put options")
```

## Limitations

1. **Rate Limiting**: yfinance may have rate limits for API calls
2. **Data Availability**: Some data may not be available for all tickers
3. **Market Hours**: Real-time data is only available during market hours
4. **International Markets**: Some international markets may have limited data

## Troubleshooting

1. **Import Errors**: Ensure yfinance is installed: `pip install yfinance`
2. **Network Issues**: Check internet connection and try again
3. **Invalid Symbols**: Verify the ticker symbol is correct
4. **Data Not Available**: Some tickers may not have all types of data available

## Future Enhancements

Potential improvements for the yfinance tools:
1. Add caching for frequently requested data
2. Implement batch processing for multiple requests
3. Add more sophisticated error handling
4. Include data validation and cleaning
5. Add support for more financial instruments 