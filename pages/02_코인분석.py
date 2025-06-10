import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("글로벌 시가총액 상위 10개 가상화폐 가격 변동 (최근 3년)")
st.markdown("---")

@st.cache_data(ttl=3600) # 데이터 캐싱: 1시간마다 업데이트
def get_top_crypto_info():
    # 2025년 6월 현재 (추정치) 글로벌 시가총액 상위 10개 코인 (업비트 거래 가능성 고려)
    # yfinance 티커는 보통 [코인티커]-USD 형태입니다.
    # 주의: 이 목록은 변동될 수 있으며, 업비트 상장 여부 및 yfinance 티커 정확성은
    # 실제 사용 시점에서 다시 확인이 필요합니다.
    crypto_tickers = {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
        "Tether (USDT)": "USDT-USD", # 스테이블 코인, 변동성 적음
        "BNB": "BNB-USD",
        "Solana": "SOL-USD",
        "XRP": "XRP-USD",
        "USD Coin (USDC)": "USDC-USD", # 스테이블 코인
        "Dogecoin": "DOGE-USD",
        "Cardano": "ADA-USD",
        "Shiba Inu": "SHIB-USD",
    }
    return crypto_tickers

crypto_tickers = get_top_crypto_info()
selected_cryptos = st.multiselect(
    "가격을 확인하고 싶은 가상화폐를 선택하세요:",
    options=list(crypto_tickers.keys()),
    default=list(crypto_tickers.keys()) # 기본값으로 모든 코인 선택
)

end_date = datetime.now() # 현재 시간 기준
start_date = end_date - timedelta(days=3 * 365) # 최근 3년

st.write(f"**데이터 조회 기간:** {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
st.markdown("---")

if selected_cryptos:
    all_crypto_data = {}
    
    st.subheader("데이터 로딩 현황")
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, crypto_name in enumerate(selected_cryptos):
        ticker = crypto_tickers[crypto_name]
        status_text.info(f"'{crypto_name}' ({ticker}) 데이터 가져오는 중... ({i+1}/{len(selected_cryptos)})")
        progress_bar.progress((i + 1) / len(selected_cryptos))
        
        try:
            # yfinance에서 주식 데이터를 가져옵니다. 가상화폐도 동일한 함수 사용.
            ticker_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if not ticker_data.empty:
                # 가상화폐는 'Adj Close' 대신 주로 'Close'를 사용합니다.
                if 'Close' in ticker_data.columns:
                    all_crypto_data[crypto_name] = ticker_data['Close']
                    status_text.success(f"'{crypto_name}' ({ticker}) 데이터 성공적으로 로드 완료.")
                else:
                    status_text.warning(f"'{crypto_name}' ({ticker})에서 'Close' 가격 데이터를 찾을 수 없습니다. (사용 가능한 컬럼: {ticker_data.columns.tolist()})")
            else:
                status_text.warning(f"'{crypto_name}' ({ticker})의 데이터를 가져왔지만 비어있습니다. 해당 기간에 데이터가 없거나 티커가 잘못되었을 수 있습니다.")
        except Exception as e:
            status_text.error(f"'{crypto_name}' ({ticker}) 데이터를 가져오는 중 심각한 오류 발생: {e}")
    
    progress_bar.empty() # 진행바 제거
    status_text.empty() # 최종 상태 메시지 제거 (아래 그래프 표시)

    data = pd.DataFrame(all_crypto_data)

    if not data.empty:
        # 모든 데이터가 NaN인 컬럼 제거 (데이터를 가져오지 못한 코인 제거)
        data = data.dropna(axis=1, how='all')

        if not data.empty:
            st.subheader("가상화폐 가격 변동 추이 (최근 3년)")

            fig = go.Figure()
            for col in data.columns:
                # 가격 스케일이 너무 다르면 그래프가 뭉개질 수 있으므로, 로그 스케일 옵션도 고려
                # fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col, yaxis='y1' if col == "Bitcoin" else 'y2'))
                fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col))

            fig.update_layout(
                title="선택된 가상화폐의 USD 기준 가격 변동",
                xaxis_title="날짜",
                yaxis_title="가격 (USD)",
                hovermode="x unified",
                legend_title="가상화폐",
                height=600,
                # yaxis_type="log" # 가격 차이가 클 경우 로그 스케일 고려
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("가격 데이터 (상위 5개 행)")
            st.dataframe(data.head())

            st.subheader("가격 데이터 (하위 5개 행)")
            st.dataframe(data.tail())

            st.subheader("기술 통계")
            st.dataframe(data.describe())
        else:
            st.warning("선택된 가상화폐들 중 유효한 가격 데이터를 가진 코인이 없습니다.")
    else:
        st.error("선택된 모든 가상화폐의 가격 데이터를 가져오는 데 실패했거나, 유효한 데이터가 없습니다. 네트워크 연결이나 티커를 다시 확인해주세요.")
else:
    st.info("가격을 확인하고 싶은 가상화폐를 하나 이상 선택해주세요.")

st.markdown(
    """
    <style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
