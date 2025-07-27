import yfinance as yf
import pandas as pd
from typing import Optional, List, Dict, Any
from google.adk.tools import agent_tool
import json
import numpy as np
from datetime import date, datetime

class PandasJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle pandas/numpy objects"""
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, (np.integer, int)):
            return int(obj)
        elif isinstance(obj, (np.floating, float)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        elif hasattr(obj, 'isoformat'):  # Handle other date-like objects
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):  # Handle custom objects like FundsData
            return str(obj)
        else:
            return str(obj)  # Convert any other non-serializable objects to string

def clean_for_json(obj):
    """Clean pandas/numpy objects for JSON serialization"""
    if isinstance(obj, pd.DataFrame):
        # Convert DataFrame to records and clean each record
        records = obj.to_dict('records')
        cleaned_records = []
        for record in records:
            cleaned_record = {}
            for key, value in record.items():
                # Convert key to string if it's a Timestamp or date
                if isinstance(key, (pd.Timestamp, date, datetime)):
                    key = key.isoformat()
                elif not isinstance(key, (str, int, float, bool, type(None))):
                    key = str(key)
                
                # Clean the value
                if isinstance(value, (pd.Timestamp, np.datetime64, date, datetime)):
                    cleaned_record[key] = value.isoformat()
                elif isinstance(value, (np.integer, np.floating)):
                    cleaned_record[key] = value.item()
                elif isinstance(value, np.ndarray):
                    cleaned_record[key] = value.tolist()
                elif pd.isna(value):
                    cleaned_record[key] = None
                else:
                    cleaned_record[key] = value
            cleaned_records.append(cleaned_record)
        return cleaned_records
    elif isinstance(obj, pd.Series):
        # Convert Series to dict and clean keys/values
        series_dict = obj.to_dict()
        cleaned_dict = {}
        for key, value in series_dict.items():
            # Convert key to string if it's a Timestamp or date
            if isinstance(key, (pd.Timestamp, date, datetime)):
                key = key.isoformat()
            elif not isinstance(key, (str, int, float, bool, type(None))):
                key = str(key)
            
            # Clean the value
            if isinstance(value, (pd.Timestamp, np.datetime64, date, datetime)):
                cleaned_dict[key] = value.isoformat()
            elif isinstance(value, (np.integer, np.floating)):
                cleaned_dict[key] = value.item()
            elif isinstance(value, np.ndarray):
                cleaned_dict[key] = value.tolist()
            elif pd.isna(value):
                cleaned_dict[key] = None
            else:
                cleaned_dict[key] = value
        return cleaned_dict
    elif isinstance(obj, (pd.Timestamp, np.datetime64, date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    elif hasattr(obj, '__dict__'):  # Handle custom objects like FundsData
        return str(obj)
    elif isinstance(obj, dict):
        cleaned_dict = {}
        for k, v in obj.items():
            # Convert key to string if it's a Timestamp or date
            if isinstance(k, (pd.Timestamp, date, datetime)):
                k = k.isoformat()
            elif not isinstance(k, (str, int, float, bool, type(None))):
                k = str(k)
            cleaned_dict[k] = clean_for_json(v)
        return cleaned_dict
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    else:
        return str(obj)  # Convert any other non-serializable objects to string

class YFinanceTool:
    """
    A comprehensive yfinance tool for accessing financial data.
    Provides access to stock information, historical data, financial statements, and more.
    """
    
    def __init__(self):
        self.name = "yfinance_tool"
        self.description = """
        A comprehensive financial data tool that provides access to:
        - Stock information and metadata
        - Historical price data
        - Financial statements (income, balance sheet, cash flow)
        - Analyst recommendations and price targets
        - Options data
        - Calendar events
        - Fund data (for ETFs and mutual funds)
        
        Use this tool to get real-time and historical financial data for stocks, ETFs, and other securities.
        """
    
    def get_ticker_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a ticker symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'MSFT', 'AAPL')
            
        Returns:
            Dictionary containing ticker information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Clean up the info dict to make it JSON serializable
            cleaned_info = {}
            for key, value in info.items():
                if isinstance(value, (int, float, str, bool, type(None))):
                    cleaned_info[key] = value
                else:
                    cleaned_info[key] = str(value)
            
            return {
                "success": True,
                "symbol": symbol,
                "info": cleaned_info
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def get_historical_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
        """
        Get historical price data for a ticker.
        
        Args:
            symbol: Stock symbol
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
            
        Returns:
            Dictionary containing historical data
        """
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period=period, interval=interval)
            
            # Convert to JSON serializable format
            history_dict = history.reset_index().to_dict('records')
            for record in history_dict:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif isinstance(value, pd.Timestamp):
                        record[key] = value.isoformat()
            
            return {
                "success": True,
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "data": history_dict
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def get_financial_statements(self, symbol: str, statement_type: str = "income") -> Dict[str, Any]:
        """
        Get financial statements for a ticker.
        
        Args:
            symbol: Stock symbol
            statement_type: Type of statement ('income', 'balance', 'cashflow')
            
        Returns:
            Dictionary containing financial statement data
        """
        try:
            ticker = yf.Ticker(symbol)
            
            if statement_type == "income":
                data = ticker.income_stmt
            elif statement_type == "balance":
                data = ticker.balance_sheet
            elif statement_type == "cashflow":
                data = ticker.cashflow
            else:
                return {
                    "success": False,
                    "error": f"Invalid statement_type: {statement_type}. Must be 'income', 'balance', or 'cashflow'"
                }
            
            # Convert to JSON serializable format
            if data is not None:
                data_dict = clean_for_json(data)
            else:
                data_dict = None
            
            return {
                "success": True,
                "symbol": symbol,
                "statement_type": statement_type,
                "data": data_dict
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def get_analyst_recommendations(self, symbol: str) -> Dict[str, Any]:
        """
        Get analyst recommendations and price targets for a ticker.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary containing analyst recommendations
        """
        try:
            ticker = yf.Ticker(symbol)
            
            # Get analyst recommendations
            recommendations = ticker.recommendations
            price_targets = ticker.analyst_price_targets
            
            # Convert to JSON serializable format
            rec_dict = clean_for_json(recommendations) if recommendations is not None else None
            pt_dict = clean_for_json(price_targets) if price_targets is not None else None
            
            return {
                "success": True,
                "symbol": symbol,
                "recommendations": rec_dict,
                "price_targets": pt_dict
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def get_calendar_events(self, symbol: str) -> Dict[str, Any]:
        """
        Get calendar events for a ticker (earnings, dividends, etc.).
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary containing calendar events
        """
        try:
            ticker = yf.Ticker(symbol)
            calendar = ticker.calendar
            
            # Convert to JSON serializable format
            calendar_dict = clean_for_json(calendar) if calendar is not None else None
            
            return {
                "success": True,
                "symbol": symbol,
                "calendar": calendar_dict
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def get_options_data(self, symbol: str, expiration_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get options data for a ticker.
        
        Args:
            symbol: Stock symbol
            expiration_date: Specific expiration date (optional)
            
        Returns:
            Dictionary containing options data
        """
        try:
            ticker = yf.Ticker(symbol)
            
            if expiration_date:
                chain = ticker.option_chain(expiration_date)
            else:
                # Get the first available expiration
                options = ticker.options
                if not options:
                    return {
                        "success": False,
                        "error": "No options available for this ticker",
                        "symbol": symbol
                    }
                chain = ticker.option_chain(options[0])
            
            # Convert to JSON serializable format
            calls_dict = clean_for_json(chain.calls) if chain.calls is not None else None
            puts_dict = clean_for_json(chain.puts) if chain.puts is not None else None
            
            return {
                "success": True,
                "symbol": symbol,
                "expiration_date": expiration_date or ticker.options[0] if ticker.options else None,
                "calls": calls_dict,
                "puts": puts_dict
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def get_fund_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get fund data for ETFs and mutual funds.
        
        Args:
            symbol: Fund symbol (e.g., 'SPY', 'QQQ')
            
        Returns:
            Dictionary containing fund data
        """
        try:
            ticker = yf.Ticker(symbol)
            
            # Get fund-specific data
            fund_data = {
                "description": getattr(ticker, 'description', None),
                "top_holdings": clean_for_json(ticker.top_holdings) if hasattr(ticker, 'top_holdings') and ticker.top_holdings is not None else [],
                "funds_data": clean_for_json(ticker.funds_data) if hasattr(ticker, 'funds_data') and ticker.funds_data is not None else {}
            }
            
            return {
                "success": True,
                "symbol": symbol,
                "fund_data": fund_data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbol": symbol
            }
    
    def get_multiple_tickers(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Get data for multiple tickers at once.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dictionary containing data for all tickers
        """
        try:
            tickers = yf.Tickers(' '.join(symbols))
            
            results = {}
            for symbol in symbols:
                ticker = tickers.tickers[symbol]
                info = ticker.info
                
                # Clean up the info dict
                cleaned_info = {}
                for key, value in info.items():
                    if isinstance(value, (int, float, str, bool, type(None))):
                        cleaned_info[key] = value
                    else:
                        cleaned_info[key] = str(value)
                
                results[symbol] = cleaned_info
            
            return {
                "success": True,
                "symbols": symbols,
                "data": results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "symbols": symbols
            }

# Create tool instances for the agent
yfinance_tool = YFinanceTool()

# Function wrappers for the agent
def get_ticker_info(symbol: str) -> str:
    """Get comprehensive information about a ticker symbol."""
    result = yfinance_tool.get_ticker_info(symbol)
    return json.dumps(result, indent=2, cls=PandasJSONEncoder)

def get_historical_data(symbol: str, period: str = "1mo", interval: str = "1d") -> str:
    """Get historical price data for a ticker."""
    result = yfinance_tool.get_historical_data(symbol, period, interval)
    return json.dumps(result, indent=2, cls=PandasJSONEncoder)

def get_financial_statements(symbol: str, statement_type: str = "income") -> str:
    """Get financial statements for a ticker."""
    result = yfinance_tool.get_financial_statements(symbol, statement_type)
    return json.dumps(result, indent=2, cls=PandasJSONEncoder)

def get_analyst_recommendations(symbol: str) -> str:
    """Get analyst recommendations and price targets for a ticker."""
    result = yfinance_tool.get_analyst_recommendations(symbol)
    return json.dumps(result, indent=2, cls=PandasJSONEncoder)

def get_calendar_events(symbol: str) -> str:
    """Get calendar events for a ticker (earnings, dividends, etc.)."""
    result = yfinance_tool.get_calendar_events(symbol)
    return json.dumps(result, indent=2, cls=PandasJSONEncoder)

def get_options_data(symbol: str, expiration_date: Optional[str] = None) -> str:
    """Get options data for a ticker."""
    result = yfinance_tool.get_options_data(symbol, expiration_date)
    return json.dumps(result, indent=2, cls=PandasJSONEncoder)

def get_fund_data(symbol: str) -> str:
    """Get fund data for ETFs and mutual funds."""
    result = yfinance_tool.get_fund_data(symbol)
    return json.dumps(result, indent=2, cls=PandasJSONEncoder)

def get_multiple_tickers(symbols: List[str]) -> str:
    """Get data for multiple tickers at once."""
    result = yfinance_tool.get_multiple_tickers(symbols)
    return json.dumps(result, indent=2, cls=PandasJSONEncoder) 