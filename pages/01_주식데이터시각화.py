import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("글로벌 시가총액 상위 10개 기업 주가 변동 (최근 3년)")

@st.cache_data(ttl=3600) # 데이터 캐싱: 1시간마다 업데이트
def get_top_companies_info():
    # 실제 시가총액 상위 10개 기업의 티커는 주기적으로 변동됩니다.
    # 여기서는 예시를 위해 널리 알려진 초대형 기업들을 선정했습니다.
    # 2025년 6월 현재 기준으로 시가총액 상위권에 있는 기업들을 반영하고자 노력했습니다.
    # 정확한 최신 정보는 투자 관련 사이트에서 확인하시고 필요시 업데이트하세요.
    company_tickers = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Alphabet (GOOGL)": "GOOGL",
        "Amazon": "AMZN",
        "Saudi Aramco": "2222.SR", # 사우디 아람코 (사우디 증시)
        "Meta Platforms": "META",
        "TSMC": "TSM",
        "Berkshire Hathaway": "BRK-A",
        "Eli Lilly": "LLY",
    }
    return company_tickers

company_tickers = get_top_companies_info()
selected_companies = st.multiselect(
    "주가를 확인하고 싶은 기업을 선택하세요:",
    options=list(company_tickers.keys()),
    default=list(company_tickers.keys()) # 기본값으로 모든 기업 선택
)

end_date = datetime.now()
start_date = end_date - timedelta(days=3*365) # 최근 3년

if selected_companies:
    data = pd.DataFrame()
    for company_name in selected_companies:
        ticker = company_tickers[company_name]
        try:
            # yfinance에서 주식 데이터를 가져옵니다.
            ticker_data = yf.download(ticker, start=start_date, end=end_date)
            if not ticker_data.empty:
                # 'Adj Close' 가격을 사용하고, 기업 이름으로 컬럼명 변경
                data[company_name] = ticker_data['Adj Close']
            else:
                st.warning(f"'{company_name}' ({ticker})의 데이터를 가져올 수 없습니다. 티커를 확인해주세요.")
        except Exception as e:
            st.error(f"'{company_name}' ({ticker}) 데이터를 가져오는 중 오류 발생: {e}")

    if not data.empty:
        # 모든 데이터가 NaN인 컬럼 제거
        data = data.dropna(axis=1, how='all')

        if not data.empty:
            st.subheader("최근 3년 주가 변동 추이")

            # Plotly Line Chart 생성
            fig = go.Figure()
            for col in data.columns:
                fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col))

            fig.update_layout(
                title="선택된 기업들의 주가 변동",
                xaxis_title="날짜",
                yaxis_title="주가 (USD)",
                hovermode="x unified",
                legend_title="기업",
                height=600 # 차트 높이 조정
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("주가 데이터 (상위 5개 행)")
            st.dataframe(data.head())

            st.subheader("주가 데이터 (하위 5개 행)")
            st.dataframe(data.tail())

            st.subheader("기술 통계")
            st.dataframe(data.describe())
        else:
            st.warning("선택된 기업들의 유효한 주가 데이터를 찾을 수 없습니다.")
    else:
        st.warning("선택된 기업들의 주가 데이터를 가져오지 못했습니다.")
else:
    st.info("주가를 확인하고 싶은 기업을 하나 이상 선택해주세요.")

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
