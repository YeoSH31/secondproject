# streamlit_app.py
# ──────────────────────────────────────────────────────────
# 글로벌 시가총액 상위 10개 기업(예시)- 최근 3년 주가 변동 시각화
# - Streamlit 1.28+에서 테스트 (1.18 이하라면 CACHE 데코레이터 부분만 주석 참고)
# - yfinance 0.2.37 기준
# ──────────────────────────────────────────────────────────

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ──────────────────── 기본 설정 ───────────────────────────
st.set_page_config(layout="wide")
st.title("📈 글로벌 시가총액 상위 10개 기업 주가 변동 (최근 3년)")

# ──────────────────── 캐싱 헬퍼 ────────────────────────────
# Streamlit 1.18 미만에서는 st.cache_data 가 없음 → st.cache 로 대체
if hasattr(st, "cache_data"):
    cache_decorator = st.cache_data(ttl=3600)
else:  # fallback
    cache_decorator = st.cache(ttl=3600)

@cache_decorator
def get_top_companies_info() -> dict:
    """
    2025-06 기준 시가총액 상위권(예시) 기업 티커 사전 반환.
    필요 시 실시간 순위에 맞춰 수정하세요.
    """
    return {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Alphabet (GOOGL)": "GOOGL",
        "Amazon": "AMZN",
        "Saudi Aramco": "2222.SR",   # 데이터가 비어 있을 수 있음
        "Meta Platforms": "META",
        "TSMC": "TSM",
        "Berkshire Hathaway": "BRK.B",  # A주 대신 B주 사용 (yfinance 안정)
        "Eli Lilly": "LLY",
    }

# ──────────────────── 사용자 입력 ──────────────────────────
company_tickers = get_top_companies_info()
selected_companies = st.multiselect(
    "주가를 확인하고 싶은 기업을 선택하세요",
    options=list(company_tickers.keys()),
    default=list(company_tickers.keys())
)

# 3년 구간(종가 데이터는 전날 기준으로 끊어줌)
end_date = datetime.today() - timedelta(days=1)
start_date = end_date - timedelta(days=3 * 365)

# ──────────────────── 데이터 수집 ──────────────────────────
@cache_decorator
def fetch_price(ticker: str, start: datetime, end: datetime) -> pd.Series:
    """단일 티커의 Adjusted Close 시리즈 반환(빈 DF면 빈 시리즈)."""
    df = yf.download(ticker, start=start, end=end, progress=False)
    return df["Adj Close"] if not df.empty else pd.Series(dtype=float)

data = pd.DataFrame()

if selected_companies:
    for name in selected_companies:
        raw_ticker = company_tickers[name]

        # yfinance 형식에 맞춰 '-' → '.' 치환 (예: BRK-A → BRK.A)  
        ticker = raw_ticker.replace("-", ".")

        series = fetch_price(ticker, start_date, end_date)
        if not series.empty:
            data[name] = series
        else:
            st.warning(f"⚠️ '{name}'({raw_ticker})의 데이터를 가져올 수 없습니다.")

# ──────────────────── 시각화 & 출력 ────────────────────────
if data.dropna(axis=1, how="all").empty:
    st.info("선택한 기업 중 표시할 유효 데이터가 없습니다. 티커를 확인해 주세요.")
    st.stop()

# ① 라인 차트
st.subheader("최근 3년 주가 변동 추이")
fig = go.Figure()
for col in data.columns:
    if data[col].notna().any():
        fig.add_trace(go.Scatter(x=data.index, y=data[col],
                                 mode="lines", name=col))

fig.update_layout(
    title="선택된 기업 주가 변동",
    xaxis_title="날짜",
    yaxis_title="주가 (USD)",
    hovermode="x unified",
    legend_title="기업",
    height=600
)
st.plotly_chart(fig, use_container_width=True)

# ② 데이터 미리보기 및 통계
st.subheader("📄 데이터 미리보기")
st.dataframe(data.head())

st.subheader("📄 데이터 (최근)")
st.dataframe(data.tail())

st.subheader("📊 기술 통계")
st.dataframe(data.describe())

# ──────────────────── 마진/패딩 조정 (선택) ────────────────
# 최신 Streamlit에서는 reportview-container 클래스가 사라졌으므로
# 최소한의 padding 조정만 적용
st.markdown(
    """
    <style>
    .block-container {
        padding: 2rem 2rem 2rem 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
