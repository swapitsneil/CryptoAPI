import streamlit as st
import requests
import pandas as pd
import mysql.connector
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="LiveAPICrypto", layout="wide")
st.title("LiveAPICrypto - Live Crypto Tracker")
st.caption("Real-time data from CoinGecko API → Saved to MySQL → Live Dashboard")

# Your coin list
coins = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano",
    "solana", "dogecoin", "polkadot", "matic-network", "litecoin"
]


# MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",  # change to your password
        database="crypto_db"
    )


# Fetch live data from API (your exact style)
def fetch_live_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    records = []
    for coin in coins:
        if coin in data:
            info = data[coin]
            records.append({
                "coin": coin.replace("-", " ").title(),
                "symbol": coin.split("-")[0].upper()[:6],
                "price": info.get("usd", 0),
                "change_24h": round(info.get("usd_24h_change", 0), 2),
                "market_cap": info.get("usd_market_cap", 0),
                "volume_24h": info.get("usd_24h_vol", 0),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    return pd.DataFrame(records)


# Save to MySQL
def save_to_mysql(df):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    query = """
    insert into crypto_prices 
    (coin, symbol, price, change_24h, market_cap, volume_24h, timestamp)
    values (%s, %s, %s, %s, %s, %s, %s)
    """

    for i in range(len(df)):
        row = df.iloc[i]
        values = (
            row["coin"], row["symbol"], row["price"],
            row["change_24h"], row["market_cap"], row["volume_24h"], row["timestamp"]
        )
        cursor.execute(query, values)

    conn.commit()
    conn.close()


# Load from MySQL
def load_from_mysql():
    conn = get_mysql_connection()
    df = pd.read_sql("select * from crypto_prices order by timestamp desc", conn)
    conn.close()
    return df


# Main Dashboard
if st.button("Fetch Latest Data & Update Dashboard", type="primary"):
    with st.spinner("Fetching live data from CoinGecko..."):
        new_data = fetch_live_data()
        save_to_mysql(new_data)
        st.success(f"Data updated! {len(new_data)} coins saved at {datetime.now().strftime('%H:%M:%S')}")

# Always show current data
df = load_from_mysql()
latest = df.drop_duplicates('coin', keep='first')

# Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    btc = latest[latest['coin'].str.contains('Bitcoin', case=False)].iloc[0]
    st.metric("Bitcoin", f"${btc['price']:,.0f}", f"{btc['change_24h']:+.2f}%")
with col2:
    eth = latest[latest['coin'].str.contains('Ethereum', case=False)].iloc[0]
    st.metric("Ethereum", f"${eth['price']:,.0f}", f"{eth['change_24h']:+.2f}%")
with col3:
    sol = latest[latest['coin'].str.contains('Solana', case=False)].iloc[0]
    st.metric("Solana", f"${sol['price']:,.0f}", f"{sol['change_24h']:+.2f}%")
with col4:
    st.metric("Last Update", datetime.now().strftime("%H:%M:%S"))

# Chart
st.subheader("Live Price Trend")
fig = px.line(df.tail(200), x="timestamp", y="price", color="coin", height=500)
st.plotly_chart(fig, use_container_width=True)

# Table
st.subheader("All Coins - 24h Performance")
show = latest[['coin', 'price', 'change_24h', 'market_cap']].copy()
show['price'] = show['price'].apply(lambda x: f"${x:,.0f}")
show['market_cap'] = show['market_cap'].apply(lambda x: f"${x / 1e9:.2f}B")
show = show.sort_values('change_24h', ascending=False)
st.dataframe(show, use_container_width=True, hide_index=True)

# Sidebar
st.sidebar.success("Connected to MySQL")
st.sidebar.caption("Live API | MySQL | Streamlit")