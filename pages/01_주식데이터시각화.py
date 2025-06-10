# app.py
# ────────────────────────────────────────────────────────────────────
# 3년간 글로벌 시가총액 Top-10 기업 주가 시각화 (Streamlit Cloud용)
# ────────────────────────────────────────────────────────────────────
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# ───── 기본 설정 ─────
st.set_page_config(
    page_title="Top-10 Global Market-Cap Stocks: 3-Year Trend",
    layout="wide"
)
st.title("📈 최근 3년 세계 시가총액 상위 10개 기업 주가 추세")

# 2025-06-10 기준 시가총액 Top-10 (Investing.com 등 참고)
TICKERS = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "NVIDIA (NVDA)": "NVDA",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Saudi Aramco (2222.SR)": "2222.SR",   # 사우디 거래소
    "Meta Platforms (META)": "META",
    "Berkshire Hathaway (BRK-B)": "BRK-B",  # B주 사용
    "Broadcom (AVGO)": "AVGO",
    "Tesla (TSLA)": "TSLA",
}

TODAY = date.today()
START = TODAY - timedelta(days=365 * 3)

# ───── 데이터 수집 함수 ─────
@st.cache_data(show_spinner="📥 주가 데이터 다운로드 중…")
def get_price_series(ticker: str) -> pd.Series:
    """3년치 조정주가(종가) 시리즈 반환 ― 결측치·예외 처리 포함"""
    df = yf.download(
        ticker,
        start=START,
        end=TODAY,
        progress=False,
        auto_adjust=True    # 'Close' 한 개 열만, 이미 분할‧배당 조정
    )

    # 1) 빈 DF 방어
    if df.empty:
        st.warning(f"📭 {ticker}: 데이터가 비어 있습니다.")
        return pd.Series(dtype="float64", name=ticker)

    # 2) 멀티인덱스 방어 (해외 일부 티커)
    if isinstance(df.columns, pd.MultiIndex):
        close = df.xs("Close", axis=1, level=0).iloc[:, 0]
    else:
        close = df["Close"]

    return close.rename(ticker).ffill()  # 결측치 전방 보간

# ───── 데이터프레임 구성 ─────
prices = pd.concat(
    {name: get_price_series(tic) for name, tic in TICKERS.items()},
    axis=1
)

# ───── 사이드바/옵션 UI ─────
st.sidebar.header("⚙️ 설정")
view_mode = st.sidebar.radio(
    "그래프 값 표시 방식",
    ("실제 주가 (USD·SAR)", "정규화 (시작값 = 100)"),
    index=1
)
selected = st.sidebar.multiselect(
    "표시할 기업 선택",
    list(TICKERS.keys()),
    default=list(TICKERS.keys())
)

# ───── 데이터 가공 ─────
plot_df = prices[selected]
if view_mode.startswith("정규화"):
    plot_df = plot_df / plot_df.iloc[0] * 100

# ───── 메인 차트 출력 ─────
st.line_chart(plot_df, height=600)

# ───── 원본 데이터 확인 ─────
with st.expander("📄 Raw Data (최근 10행)"):
    st.dataframe(prices.tail(10))

# ────────────────────────────────────────────────────────────────────
# 끝. 필요한 경우 여기 아래에 향후 예측 모델/성능 지표 등을 추가 가능
# ────────────────────────────────────────────────────────────────────
