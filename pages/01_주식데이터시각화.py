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
    "Amazon (AMZN)"          : "AMZN",
    "Saudi Aramco (2222.SR)" : "2222.SR",
    "Meta Platforms (META)"  : "META",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "Broadcom (AVGO)"        : "AVGO",
    "Tesla (TSLA)"           : "TSLA",
}

TODAY  = date.today()
START  = TODAY - timedelta(days=365*3)

# ───── 가격 시리즈 함수 ─────
@st.cache_data(show_spinner="📥 데이터 다운로드 중…")
def get_series(ticker: str) -> pd.Series:
    df = yf.download(ticker, start=START, end=TODAY,
                     progress=False, auto_adjust=True)
    if df.empty:
        return pd.Series(dtype="float64", name=ticker)
    if isinstance(df.columns, pd.MultiIndex):
        close = df.xs("Close", axis=1, level=0).iloc[:, 0]
    else:
        close = df["Close"]
    return close.rename(ticker).ffill().bfill()

prices = pd.concat(
    {name: get_series(tic) for name, tic in TICKERS.items()},
    axis=1
)

# ───── 사이드바 옵션 ─────
st.sidebar.header("⚙️  옵션")
view_mode = st.sidebar.radio("그래프 표시",
                             ("실제 주가", "정규화(시작값=100)"), index=1)
sel_stocks = st.sidebar.multiselect("표시할 기업",
                                    list(TICKERS.keys()),
                                    default=list(TICKERS.keys()))

# ───── 추세 그래프 ─────
plot_df = prices[sel_stocks]
if view_mode.startswith("정규화"):
    plot_df = plot_df / plot_df.iloc[0] * 100
st.line_chart(plot_df, height=550)

with st.expander("📄 Raw Data (tail)"):
    st.dataframe(prices.tail(10))

# ───── 예측 섹션 ─────
st.subheader("🔮 미래 주가 예측 (거시 변수 제외)")

if not PROPHET_OK:
    st.error("`prophet` 라이브러리가 설치되지 않았습니다. "
             "requirements.txt에 `prophet` 추가 후 재배포하세요.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    tgt_name = st.selectbox("예측할 종목", list(TICKERS.keys()))
with col2:
    horizon = st.slider("예측 기간 (일)", 7, 180, 30, step=7)

@st.cache_data(show_spinner="🔮 모델 학습 중…")
def train_prophet(target: str):
    s = prices[target].dropna().reset_index()
    s.columns = ["ds", "y"]
    model = Prophet(daily_seasonality=False,
                    yearly_seasonality=True,
                    changepoint_prior_scale=0.2)
    model.fit(s)
    return model, s

model, train_df = train_prophet(tgt_name)

future    = model.make_future_dataframe(periods=horizon)
forecast  = model.predict(future)

# ───── Plotly 시각화 ─────
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=train_df["ds"], y=train_df["y"],
                         mode="lines", name="Actual"))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"],
                         mode="lines", name="Forecast"))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"],
                         mode="lines", name="Upper CI",
                         line=dict(dash="dash"), opacity=0.3))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"],
                         mode="lines", name="Lower CI",
                         line=dict(dash="dash"), opacity=0.3))
fig.update_layout(height=550,
                  title=f"{tgt_name} — Prophet Forecast ({horizon} days)")
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔎 예측 테이블 (tail)"):
    st.dataframe(
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10)
    )

st.caption("ⓘ 본 예측은 교육용 예시이며, 실제 투자 판단에 사용할 수 없습니다.")
# ─────────────────────────────────────────────────────────────────
