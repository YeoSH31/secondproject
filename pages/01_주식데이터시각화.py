# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Top-10 Global Market-Cap Stocks: 3-Year Trend",
                   layout="wide")

st.title("📈 3-Year Price History of the World’s 10 Largest Companies")

# 최신(2025-06-10) 시가총액 Top-10 기업 -- Investing.com 기준
TICKERS = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "NVIDIA (NVDA)": "NVDA",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Saudi Aramco (2222.SR)": "2222.SR",      # 사우디거래소
    "Meta Platforms (META)": "META",
    "Berkshire Hathaway (BRK-B)": "BRK-B",     # B주식 사용
    "Broadcom (AVGO)": "AVGO",
    "Tesla (TSLA)": "TSLA",
}

TODAY  = date.today()
START  = TODAY - timedelta(days=365*3)

@st.cache_data(show_spinner="Downloading price data …")
def get_price_series(ticker: str) -> pd.Series:
    df = yf.download(ticker, start=START, end=TODAY, progress=False)
    # 예: 해외거래소(2222.SR)는 일부 휴장일로 인해 NaN 이 생길 수 있으므로 forward-fill
    return df["Adj Close"].ffill()

# 데이터 프레임 구성
prices = pd.concat({name: get_price_series(tic) for name, tic in TICKERS.items()},
                   axis=1)

# === 인터랙티브 옵션 ===
col1, col2 = st.columns([1, 3], gap="large")

with col1:
    view_mode = st.radio(
        "그래프 값 표시 방식 선택",
        ("실제 주가(USD·SAR)", "정규화(시작값=100)"),
        index=1,
    )
    selected = st.multiselect(
        "표시할 기업 선택 (기본 = 모두)",
        list(TICKERS.keys()),
        default=list(TICKERS.keys()),
    )

# 선택·정규화 처리
plot_df = prices[selected]
if view_mode.startswith("정규화"):
    plot_df = plot_df / plot_df.iloc[0] * 100

# === 시각화 ===
with col2:
    st.line_chart(plot_df, height=600)

# 원본 데이터 보조 탭
with st.expander("원본 데이터 보기"):
    st.dataframe(prices.tail(10))
