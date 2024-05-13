import yfinance as yf
import pandas as pd

def download_data(ticker, start_date, end_date):
    """
    Download stock data from Yahoo Finance.

    Args:
    - ticker (str): Ticker symbol of the stock.
    - start_date (str): Start date for the data in "YYYY-MM-DD" format.
    - end_date (str): End date for the data in "YYYY-MM-DD" format.

    Returns:
    - DataFrame: Stock data including Open, High, Low, Close, Adj Close, and Volume.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def calculate_technical_indicators(data):
    """
    Calculate technical indicators including SMA, RSI, and MACD.

    Args:
    - data (DataFrame): Stock data including Close prices.

    Returns:
    - DataFrame: Stock data with additional columns for technical indicators.
    """
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['RSI'] = calculate_RSI(data)
    data['MACD'], data['MACD_signal'], data['MACD_hist'] = calculate_MACD(data)
    return data

def calculate_RSI(data, window=14):
    """
    Calculate Relative Strength Index (RSI) for the given data.

    Args:
    - data (DataFrame): Stock data including Close prices.
    - window (int): Window size for RSI calculation (default is 14).

    Returns:
    - Series: RSI values.
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))
    return RSI

def calculate_MACD(data, short_window=12, long_window=26, signal_window=9):
    """
    Calculate Moving Average Convergence Divergence (MACD) for the given data.

    Args:
    - data (DataFrame): Stock data including Close prices.
    - short_window (int): Window size for short-term EMA (default is 12).
    - long_window (int): Window size for long-term EMA (default is 26).
    - signal_window (int): Window size for signal line (default is 9).

    Returns:
    - Tuple: MACD line, signal line, and histogram.
    """
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def trading_strategy(data):
    """
    Define trading strategy based on technical indicators.

    Args:
    - data (DataFrame): Stock data including technical indicators.

    Returns:
    - DataFrame: Signals indicating buy/sell positions.
    """
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0
    signals.loc[data['SMA_20'] > data['SMA_50'], 'signal'] = 1.0
    signals.loc[data['RSI'] > 70, 'signal'] = -1.0
    signals.loc[data['MACD'] > data['MACD_signal'], 'signal'] = 1.0
    signals.loc[data['MACD'] < data['MACD_signal'], 'signal'] = -1.0
    signals['positions'] = signals['signal'].diff()
    return signals

def generate_signals(data):
    """
    Generate trading signals based on the defined strategy.

    Args:
    - data (DataFrame): Stock data including technical indicators.

    Returns:
    - DataFrame: Signals indicating buy/sell positions.
    """
    signals = trading_strategy(data)
    return signals

def execute_orders(data, signals, initial_capital=100000):
    """
    Execute buy/sell orders based on generated signals.

    Args:
    - data (DataFrame): Stock data.
    - signals (DataFrame): Signals indicating buy/sell positions.
    - initial_capital (float): Initial capital for trading (default is $100,000).

    Returns:
    - DataFrame: Portfolio including cash, holdings, and total value over time.
    """
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    portfolio = pd.DataFrame(index=signals.index)
    portfolio['cash'] = initial_capital
    portfolio['holdings'] = 0.0
    portfolio['total'] = initial_capital

    for i in range(len(signals) - 1):
        if signals['positions'].iloc[i] == 1.0:
            shares = portfolio['cash'].iloc[i] / data['Close'].iloc[i]
            portfolio.loc[data.index[i+1], 'cash'] = 0.0
            portfolio.loc[data.index[i+1], 'holdings'] = shares
        elif signals['positions'].iloc[i] == -1.0:
            portfolio.loc[data.index[i+1], 'cash'] = portfolio['holdings'].iloc[i] * data['Close'].iloc[i]
            portfolio.loc[data.index[i+1], 'holdings'] = 0.0
        portfolio.loc[data.index[i+1], 'total'] = portfolio['cash'].iloc[i+1] + portfolio['holdings'].iloc[i+1] * data['Close'].iloc[i]

    return portfolio

if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2023-04-01"
    end_date = "2024-04-30"

    data = download_data(ticker, start_date, end_date)
    data = calculate_technical_indicators(data)
    signals = generate_signals(data)
    portfolio = execute_orders(data, signals)

    print(f"Final portfolio value: ${portfolio['total'].iloc[-1]:.2f}")
