# app.py  ──────────────────────────────────────────────────────────
# 글로벌 시가총액 Top-10 기업: 최근 3년 시각화 + 단기 예측(거시 변수 X)
# ─────────────────────────────────────────────────────────────────
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# Prophet ─────────────────────────────────────────────────────────
try:
    from prophet import Prophet
    PROPHET_OK = True
except ImportError:
    PROPHET_OK = False

# ───── 기본 설정 ─────
st.set_page_config(page_title="Top-10 Stocks: Trend & Forecast",
                   layout="wide")
st.title("🌍 글로벌 시가총액 Top-10 기업\n최근 3년 추세 ＋ 🔮 단기 예측")

TICKERS = {
    "Apple (AAPL)"           : "AAPL",
    "Microsoft (MSFT)"       : "MSFT",
    "NVIDIA (NVDA)"          : "NVDA",
    "Alphabet (GOOGL)"       : "GOOGL",
    "Amazon (AMZN)"          : "AMZN
