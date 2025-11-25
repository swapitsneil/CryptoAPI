import streamlit as st
import requests
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# streamlit config
st.set_page_config(page_title="LiveAPICrypto", layout="wide")
st.title("LiveAPICrypto - Live Crypto Tracker (sqlite)")
st.caption("real-time cryptocurrency data with sqlite storage and charts")

# database setup
DB_NAME = "crypto_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        create table if not exists crypto_prices (
            id integer primary key autoincrement,
            coin text,
            symbol text,
            price real,
            change_24h real,
            market_cap real,
            volume_24h real,
            timestamp text
        )
    """)
    conn.close()

init_db()

# coin list
coins = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano",
    "solana", "dogecoin", "polkadot", "matic-network", "litecoin"
]

# fetch data from api
def fetch_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params).json()

    rows = []
    for coin in coins:
        if coin in response:
            info = response[coin]
            rows.append({
                "coin": coin.replace("-", " ").title(),
                "symbol": coin.split("-")[0].upper(),
                "price": info.get("usd", 0),
                "change_24h": round(info.get("usd_24h_change", 0), 2),
                "market_cap": info.get("usd_market_cap", 0),
                "volume_24h": info.get("usd_24h_vol", 0),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    return pd.DataFrame(rows)

# save to sqlite
def save_to_db(df):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("crypto_prices", conn, if_exists="append", index=False)
    conn.close()

# load from sqlite
def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("select * from crypto_prices order by timestamp", conn)
    conn.close()
    return df

# fetch button
if st.button("fetch live data"):
    data = fetch_data()
    save_to_db(data)
    st.success("data updated")

# load existing data
df = load_data()
latest = df.drop_duplicates("coin", keep="last")

# metric cards
st.subheader("live market snapshot")
c1, c2, c3, c4 = st.columns(4)

for col, name in zip([c1, c2, c3, c4], ["Bitcoin", "Ethereum", "Solana", "Cardano"]):
    row = latest[latest["coin"] == name]
    if not row.empty:
        row = row.iloc[0]
        col.metric(name, f"${row['price']:,.0f}", f"{row['change_24h']:+.2f}%")

# matplotlib / seaborn chart
st.subheader("multi-coin price trend (matplotlib / seaborn)")
if len(df) > 0:
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=df, x="timestamp", y="price", hue="coin", linewidth=1.3)
    plt.xticks(rotation=45)
    plt.xlabel("time")
    plt.ylabel("price (usd)")
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.info("no data found, fetch data to see charts")

# plotly chart
st.subheader("interactive real-time chart")
fig = px.line(df.tail(200), x="timestamp", y="price", color="coin", height=500)
st.plotly_chart(fig, use_container_width=True)

# performance table
st.subheader("24h performance")
table = latest[["coin", "price", "change_24h", "market_cap"]].copy()
table["price"] = table["price"].apply(lambda x: f"${x:,.0f}")
table["market_cap"] = table["market_cap"].apply(lambda x: f"${x/1e9:.2f}B")
st.dataframe(table.sort_values("change_24h", ascending=False), use_container_width=True, hide_index=True)
