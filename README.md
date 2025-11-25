# 🚀 CryptoAPI – Live Cryptocurrency Dashboard

A real-time crypto tracking dashboard built with Streamlit, CoinGecko API, and MYSQL.
This project fetches live cryptocurrency prices, 24h changes, market caps, and visualizes them using interactive charts and auto-refreshing metrics.

Stay updated with the crypto market in a clean and beautifully designed dashboard.

## ⚡ Key Features

✔ Live Price Fetching (CoinGecko API)
✔ Auto-Refreshing Dashboard (every 60 seconds)
✔ Adding rows in MYSQL in every 120 seconds
✔ Interactive Charts with Plotly
✔ Real-time Metrics Cards for top coins
✔ 24h Performance Leaderboard
✔ One-Click Data Refresh & Reset
✔ Clean, modern UI using Streamlit

## 🖼️ Dashboard Preview

![Image](https://github.com/user-attachments/assets/de81eb46-b398-4123-bb23-94a5a7509b54)

<img width="1676" height="934" alt="Image" src="https://github.com/user-attachments/assets/3df42e2b-b5aa-46cd-84e6-5ef61e1263c7" />

<img width="1470" height="1324" alt="Image" src="https://github.com/user-attachments/assets/e34bdc64-73a9-4c74-a97a-580c7558629e" />

<img width="1988" height="1000" alt="Image" src="https://github.com/user-attachments/assets/9f5b3c56-a1cc-4750-9498-3fb5e7594bba" />

<img width="2328" height="994" alt="Image" src="https://github.com/user-attachments/assets/b2348dd3-e3f8-4bfa-8112-be74ff12da2e" />

## 🛠️ Tech Stack

| Component     | Technology     |
| ------------- | -------------- |
| Data API      | CoinGecko      |
| Frontend      | Streamlit      |
| Backend       | Python         |
| Database      | MySQL          |
| Visualization | Plotly         |
| Data Handling | Pandas         |

## 📦 Installation & Setup

### 1️⃣ Clone the Repository
    git clone https://github.com/your-username/cryptoapi.git
    cd cryptoapi

### 2️⃣ Install Dependencies
    pip install -r requirements.txt

### 3️⃣ Run the Streamlit App
    streamlit run app.py


streamlit link - https://appdeploypy-wvt9bjqbrn2j9war4zu2ea.streamlit.app/    


## 📡 How It Works

🔄 Live Data Fetching

Dashboard pulls fresh crypto data directly from CoinGecko:

- Price (USD)
- 24h Change %
- Market Cap
- 24h Volume
- Timestamped entries
- 10 major cryptocurrencies

💾 Historical Storage

MYSQL
crypto_db
└── crypto_prices
📊 Visual Insights
- Real-time line charts
- Sorted performance table
- Coin-wise filtering
- Auto refresh + manual refresh

## 📁 Project Structure

cryptoapi\
│
├── app.py                     # main streamlit application (mysql version)
├── appdeploy.py               # sqlite deployment version
├── liveapicrypto.ipynb        # jupyter notebook for crypto analysis
├── liveapidash.pbix           # power bi dashboard
├── requirements.txt           # dependencies for streamlit cloud
└── README.md                  # project documentation


## ⭐ Why This Project Stands Out

- Uses live API, not static CSV
- Lightweight, fast, and deployable anywhere
- Beautiful analytics dashboard
- Beginner-friendly + production-ready
- Perfect for portfolio or data engineering showcase

## 🚀 Future Improvements

- Add more coins dynamically
- Add alerts for price spikes/drops
- Build separate admin panel
- Integrate prediction models (ARIMA/LSTM)
- Add email notifications

## 🤝 Contributions

Pull requests are welcome!
If you want to improve charts, add APIs, or optimize code—jump in.

## 💬 Author

Swapnui Nicolson
For collaboration or suggestions: feel free to reach out!
