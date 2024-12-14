import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from ta.momentum import RSIIndicator  # Import RSIIndicator
from ta.trend import MACD  # Import MACD
from ta.volatility import BollingerBands  # Import BollingerBands

# Dictionary of companies with their tickers
company_tickers = {
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "itc": "ITC.NS",
    "sbi": "SBIN.NS",
    "hdfc": "HDFCBANK.NS",
    "icici": "ICICIBANK.NS",
    "larsen": "LT.NS",
    "hindustan": "HINDUNILVR.NS",
    "bharti": "BHARTIARTL.NS",
    "kotak": "KOTAKBANK.NS",
    "asian": "ASIANPAINT.NS",
    "maruti": "MARUTI.NS",
    "tatasteel": "TATASTEEL.NS",
    "adanigreen": "ADANIGREEN.NS",
    "bajajfinance": "BAJFINANCE.NS",
    "wipro": "WIPRO.NS",
    "hcl": "HCLTECH.NS",
    "ntpc": "NTPC.NS",
    "powergrid": "POWERGRID.NS",
    "tatamotors": "TATAMOTORS.NS",
    "bajaj": "BAJAJ-AUTO.NS",
    "hero": "HEROMOTOCO.NS",
    "sun": "SUNPHARMA.NS",
    "reddy": "DRREDDY.NS",
    "cipla": "CIPLA.NS",
    "axis": "AXISBANK.NS",
    "adaniports": "ADANIPORTS.NS",
    "ultratech": "ULTRACEMCO.NS",
    "grasim": "GRASIM.NS",
    "bharat": "BPCL.NS",
    "ongc": "ONGC.NS",
    "ioc": "IOC.NS",
    "tatapower": "TATAPOWER.NS",
    "wilmar": "AWL.NS",
    "zee": "ZEEL.NS",
    "godrej": "GODREJCP.NS",
    "dabur": "DABUR.NS",
    "britannia": "BRITANNIA.NS",
    "havells": "HAVELLS.NS",
    "apollo": "APOLLOHOSP.NS",
    "gail": "GAIL.NS",
    "prudential": "ICICIPRULI.NS",
    "tataconsum": "TATACONSUM.NS",
    "lupin": "LUPIN.NS",
    "biocon": "BIOCON.NS",
    "mphasis": "MPHASIS.NS",
    "persistent": "PERSISTENT.NS",
    "coforge": "COFORGE.NS",
    "aurobindo": "AUROPHARMA.NS",
    "amara": "AMARAJABAT.NS",
    "berger": "BERGEPAINT.NS",
    "whirlpool": "WHIRLPOOL.NS",
    "hal": "HAL.NS",
    "bel": "BEL.NS",
    "pidilite": "PIDILITIND.NS",
    "rec": "RECLTD.NS",
    "nhpc": "NHPC.NS",
    "chambal": "CHAMBLFERT.NS",
    "escorts": "ESCORTS.NS",
    "gujarat": "GUJGASLTD.NS",
    "voltas": "VOLTAS.NS",
    "tvs": "TVSMOTOR.NS",
    "indiabulls": "IBULHSGFIN.NS",
    "shriram": "SHRIRAMFIN.NS",
    "lichf": "LICHSGFIN.NS",
    "idfc": "IDFCFIRSTB.NS",
    "bob": "BANKBARODA.NS",
    "canara": "CANBK.NS",
    "pnb": "PNB.NS",
    "indianbank": "INDIANB.NS",
    "unionbank": "UNIONBANK.NS",
    "federal": "FEDERALBNK.NS",
    "bandhan": "BANDHANBNK.NS",
    "aubank": "AUBANK.NS",
    "manappuram": "MANAPPURAM.NS",
    "muthoot": "MUTHOOTFIN.NS",
    "lic": "LICI.NS",
    "nmdc": "NMDC.NS",
    "sail": "SAIL.NS",
    "glenmark": "GLENMARK.NS",
    "torrent": "TORNTPHARM.NS",
    "zydus": "CADILAHC.NS",
    "mcdowell": "MCDOWELL-N.NS",
    "ubl": "UBL.NS",
    "radico": "RADICO.NS",
    "jubilant": "JUBLFOOD.NS",
    "westlife": "WESTLIFE.NS",
    "burgerking": "BURGERKING.NS",
    "zomato": "ZOMATO.NS",
    "nykaa": "NYKAA.NS",
    "paytm": "PAYTM.NS",
    "delhivery": "DELHIVERY.NS",
    "policybazaar": "POLICYBZR.NS",
    "irctc": "IRCTC.NS",
    "concor": "CONCOR.NS",
    "abfrl": "ABFRL.NS",
    "trent": "TRENT.NS",
    "dmart": "DMART.NS",
    "future": "FRETAIL.NS"
}

# Function to fetch data and calculate support/resistance levels
def fetch_and_calculate_levels(ticker):
    stock_data = yf.download(ticker, period="1d", interval="1m", progress=False)

    if stock_data.empty:
        raise ValueError(f"No data found for ticker {ticker}.")

    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in stock_data.columns]

    stock_data.columns = [col.split('_')[0] for col in stock_data.columns]

    required_columns = ['High', 'Low', 'Close']
    missing_columns = [col for col in required_columns if col not in stock_data.columns]
    
    if missing_columns:
        raise KeyError(f"Missing columns: {', '.join(missing_columns)}")

    stock_data = stock_data[['High', 'Low', 'Close']].dropna()

    stock_data['Pivot'] = (stock_data['High'] + stock_data['Low'] + stock_data['Close']) / 3
    stock_data['Support1'] = (2 * stock_data['Pivot']) - stock_data['High']
    stock_data['Resistance1'] = (2 * stock_data['Pivot']) - stock_data['Low']
    stock_data['Support2'] = stock_data['Pivot'] - (stock_data['Resistance1'] - stock_data['Support1'])
    stock_data['Resistance2'] = stock_data['Pivot'] + (stock_data['Resistance1'] - stock_data['Support1'])

    return stock_data

# Function to add technical indicators and generate buy/sell signal
def add_technical_indicators(stock_data):
    close_prices = stock_data['Close'].squeeze()

    rsi = RSIIndicator(close_prices)
    stock_data['RSI'] = rsi.rsi()

    macd = MACD(close_prices)
    stock_data['MACD'] = macd.macd()
    stock_data['Signal_Line'] = macd.macd_signal()

    bollinger = BollingerBands(close_prices)
    stock_data['BB_Middle'] = bollinger.bollinger_mavg()
    stock_data['BB_Upper'] = bollinger.bollinger_hband()
    stock_data['BB_Lower'] = bollinger.bollinger_lband()

    stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()

    return stock_data

# Generate Buy/Sell signals based on the indicators
def generate_signals(stock_data):
    latest_data = stock_data.iloc[-1]

    rsi_value = latest_data['RSI'].item()
    close_price = latest_data['Close'].item()
    bb_lower = latest_data['BB_Lower'].item()
    macd_value = latest_data['MACD'].item()
    signal_line = latest_data['Signal_Line'].item()

    print(f"RSI: {rsi_value}, Close: {close_price}, BB Lower: {bb_lower}, MACD: {macd_value}, Signal Line: {signal_line}")

    # Relaxed threshold conditions
    rsi_condition_buy = rsi_value < 60  # Relaxed condition for "Buy"
    rsi_condition_sell = rsi_value > 40  # Relaxed condition for "Sell"
    bb_condition_buy = close_price < bb_lower * 1.02  # More lenient BB condition
    bb_condition_sell = close_price > bb_lower * 1.02
    macd_condition_buy = macd_value > signal_line
    macd_condition_sell = macd_value < signal_line

    if rsi_condition_buy and bb_condition_buy and macd_condition_buy:
        signal = "Buy"
        confidence = "High"
    elif rsi_condition_sell and bb_condition_sell and macd_condition_sell:
        signal = "Sell"
        confidence = "High"
    else:
        signal = "No Signal"
        confidence = "Neutral"

    return signal, confidence

# Dash app initialization
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Real-Time Stock Price with Support and Resistance Levels", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': company.capitalize(), 'value': ticker} for company, ticker in company_tickers.items()],
        value='RELIANCE.NS',
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    html.Div(id='signal-display', style={'textAlign': 'center', 'fontSize': 24, 'marginTop': 20}),
    
    html.Div(id='indicator-display', style={'textAlign': 'center', 'fontSize': 18, 'marginTop': 10}),
    
    dcc.Graph(id='stock-graph'),
    
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # Update every minute (60000ms)
        n_intervals=0
    )
])

# Update the graph and buy/sell signal
@app.callback(
    [Output('stock-graph', 'figure'),
     Output('signal-display', 'children'),
     Output('indicator-display', 'children')],
    [Input('ticker-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(ticker, n_intervals):
    stock_data = fetch_and_calculate_levels(ticker)
    stock_data = add_technical_indicators(stock_data)

    signal, confidence = generate_signals(stock_data)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=stock_data.index,
        open=stock_data['Close'] - np.random.normal(0, 1, size=len(stock_data)),
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name="Stock Price"
    ))

    fig.add_trace(go.Scatter(
        x=stock_data.index, y=stock_data['Support1'],
        mode='lines', name='Support 1', line=dict(color='red', dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=stock_data.index, y=stock_data['Resistance1'],
        mode='lines', name='Resistance 1', line=dict(color='green', dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=stock_data.index, y=stock_data['Support2'],
        mode='lines', name='Support 2', line=dict(color='blue', dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=stock_data.index, y=stock_data['Resistance2'],
        mode='lines', name='Resistance 2', line=dict(color='purple', dash='dash')
    ))

    fig.update_layout(
        title=f"{ticker} Stock Price with Support and Resistance Levels",
        xaxis_title="Time",
        yaxis_title="Price",
        template="plotly_dark"
    )

    signal_text = f"Signal: {signal} | Confidence: {confidence}"
    indicator_text = f"RSI: {stock_data['RSI'].iloc[-1]:.2f} | MACD: {stock_data['MACD'].iloc[-1]:.2f} | Signal Line: {stock_data['Signal_Line'].iloc[-1]:.2f} | BB Lower: {stock_data['BB_Lower'].iloc[-1]:.2f}"

    return fig, signal_text, indicator_text

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
