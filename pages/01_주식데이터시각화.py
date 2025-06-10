import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 시가총액 상위 10대 기업 주가", layout="wide")
st.title("📈 글로벌 시가총액 상위 10대 기업의 주가 변화 (최근 3년)")

# 기업 목록
TOP_10_TICKERS = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Saudi Aramco (2222.SR)": "2222.SR",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "NVIDIA (NVDA)": "NVDA",
    "Meta Platforms (META)": "META",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "TSMC (TSM)": "TSM",
    "Tesla (TSLA)": "TSLA"
}

# 사용자 선택
selected_companies = st.multiselect(
    "시각화할 기업을 선택하세요:",
    options=list(TOP_10_TICKERS.keys()),
    default=["Apple (AAPL)", "Microsoft (MSFT)", "NVIDIA (NVDA)"]
)

# 날짜 범위 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)

# 데이터 가져오기 및 시각화
if selected_companies:
    fig = go.Figure()
    for name in selected_companies:
        ticker = TOP_10_TICKERS[name]
        df = yf.download(ticker, start=start_date, end=end_
