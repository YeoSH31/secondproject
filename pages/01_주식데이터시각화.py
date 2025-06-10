import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("글로벌 시가총액 상위 10개 기업 주가 변동 (2025년 6월 8일 기준 최근 3년)")

@st.cache_data(ttl=3600) # 데이터 캐싱: 1시간마다 업데이트
def get_top_companies_info():
    # 2025년 6월 현재 기준 (추정치) 글로벌 시가총액 상위 기업 티커
    # 실제 시가총액 순위와 티커는 실시간으로 변동되므로,
    # 이 목록은 예시이며, 정확한 최신 정보는 별도 확인이 필요합니다.
    company_tickers = {
        "Microsoft": "MSFT",
        "Apple": "AAPL",
        "NVIDIA": "NVDA",
        "Alphabet (GOOGL)": "GOOGL", # 클래스 A 주식
        "Amazon": "AMZN",
        "Saudi Aramco": "2222.SR", # 야후 파이낸스 기준 사우디 아람코 티커
        "Meta Platforms": "META",
        "Berkshire Hathaway": "BRK-A", # 클래스 A 주식
        "Eli Lilly": "LLY",
        "TSMC": "TSM", # Taiwan Semiconductor Manufacturing Company (미국 ADR)
    }
    return company_tickers

company_tickers = get_top_companies_info()
selected_companies = st.multiselect(
    "주가를 확인하고 싶은 기업을 선택하세요:",
    options=list(company_tickers.keys()),
    default=list(company_tickers.keys()) # 기본값으로 모든 기업 선택
)

# --- 변경된 부분 시작 ---
# 데이터를 가져올 기준 종료일 설정 (2025년 6월 8일)
fixed_end_date = datetime(2025, 6, 8)
# 기준 종료일로부터 3년 전 날짜 계산
start_date = fixed_end_date - timedelta(days=3*365)
end_date = fixed_end_date # end_date를 fixed_end_date로 설정
# --- 변경된 부분 끝 ---

st.write(f"**데이터 조회 기간:** {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

if selected_companies:
    data = pd.DataFrame()
    for company_name in selected_companies:
        ticker = company_tickers[company_name]
        st.info(f"'{company_name}' ({ticker}) 데이터 가져오는 중...")
        try:
            # yfinance에서 주식 데이터를 가져옵니다.
            ticker_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if not ticker_data.empty:
                if 'Adj Close' in ticker_data.columns:
                    data[company_name] = ticker_data['Adj Close']
                    st.success(f"'{company_name}' ({ticker}) 데이터 성공적으로 로드 완료.")
                elif 'Close' in ticker_data.columns:
                    data[company_name] = ticker_data['Close']
                    st.warning(f"'{company_name}' ({ticker})의 'Adj Close' 데이터를 찾을 수 없습니다. 'Close' 데이터를 사용합니다.")
                else:
                    st.warning(f"'{company_name}' ({ticker})에서 'Adj Close' 또는 'Close' 주가 데이터를 찾을 수 없습니다. (사용 가능한 컬럼: {ticker_data.columns.tolist()})")
            else:
                st.warning(f"'{company_name}' ({ticker})의 데이터를 가져왔지만 비어있습니다. 해당 기간에 데이터가 없거나 티커가 잘못되었을 수 있습니다.")
        except Exception as e:
            st.error(f"'{company_name}' ({ticker}) 데이터를 가져오는 중 심각한 오류 발생: {e}")

    if not data.empty:
        data = data.dropna(axis=1, how='all')

        if not data.empty:
            st.subheader("최근 3년 주가 변동 추이")

            fig = go.Figure()
            for col in data.columns:
                fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col))

            fig.update_layout(
                title="선택된 기업들의 주가 변동",
                xaxis_title="날짜",
                yaxis_title="주가 (USD)",
                hovermode="x unified",
                legend_title="기업",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("주가 데이터 (상위 5개 행)")
            st.dataframe(data.head())

            st.subheader("주가 데이터 (하위 5개 행)")
            st.dataframe(data.tail())

            st.subheader("기술 통계")
            st.dataframe(data.describe())
        else:
            st.warning("선택된 기업들 중 유효한 주가 데이터를 가진 기업이 없습니다. 모든 데이터가 누락되었을 수 있습니다.")
    else:
        st.error("선택된 모든 기업의 주가 데이터를 가져오는 데 실패했습니다. 네트워크 연결이나 티커를 다시 확인해주세요.")
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
