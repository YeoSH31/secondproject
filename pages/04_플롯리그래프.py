import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide") # 페이지 레이아웃을 넓게 설정

st.title("📊 스트림릿과 플롯리를 이용한 인터랙티브 그래프")
st.write("간단한 데이터셋으로 다양한 플롯리 그래프를 그려보세요!")

# 1. 데이터 생성 (예시)
st.header("1. 데이터 선택 및 미리보기")
data_option = st.selectbox(
    "데이터셋을 선택하세요:",
    ("랜덤 데이터", "아이리스 데이터")
)

if data_option == "랜덤 데이터":
    st.subheader("랜덤 데이터 생성")
    num_rows = st.slider("데이터 행 개수:", 10, 1000, 100)
    df = pd.DataFrame({
        "x": [i * 0.1 for i in range(num_rows)],
        "y": [i**2 + 5 * i + 10 + (pd.np.random.randn() * 20) for i in range(num_rows)],
        "category": [f"Category {(i % 3) + 1}" for i in range(num_rows)]
    })
    st.dataframe(df.head())
else:
    st.subheader("아이리스(붓꽃) 데이터셋")
    df = px.data.iris() # 플롯리에 내장된 아이리스 데이터셋 사용
    st.dataframe(df.head())

st.write("---")

# 2. 그래프 유형 선택 및 그리기
st.header("2. 그래프 유형 선택 및 그리기")
chart_type = st.selectbox(
    "그릴 그래프 유형을 선택하세요:",
    ("산점도 (Scatter Plot)", "라인 차트 (Line Chart)", "막대 그래프 (Bar Chart)", "히스토그램 (Histogram)")
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("차트 설정")
    if chart_type == "산점도 (Scatter Plot)":
        x_col = st.selectbox("X축 선택:", df.columns)
        y_col = st.selectbox("Y축 선택:", df.columns)
        color_col = st.selectbox("색상으로 그룹화 (선택 사항):", ["선택 안함"] + list(df.columns))
        size_col = st.selectbox("크기로 표현 (선택 사항):", ["선택 안함"] + list(df.select_dtypes(include=['number']).columns))

        if color_col != "선택 안함" and size_col != "선택 안함":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col, title=f"{x_col} vs {y_col} 산점도")
        elif color_col != "선택 안함":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{x_col} vs {y_col} 산점도")
        elif size_col != "선택 안함":
            fig = px.scatter(df, x=x_col, y=y_col, size=size_col, title=f"{x_col} vs {y_col} 산점도")
        else:
            fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col} 산점도")

    elif chart_type == "라인 차트 (Line Chart)":
        x_col = st.selectbox("X축 선택:", df.columns)
        y_col = st.selectbox("Y축 선택:", df.columns)
        fig = px.line(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col} 라인 차트")

    elif chart_type == "막대 그래프 (Bar Chart)":
        x_col = st.selectbox("X축 (범주) 선택:", df.columns)
        y_col = st.selectbox("Y축 (값) 선택:", df.columns)
        fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col}별 {y_col} 막대 그래프")

    elif chart_type == "히스토그램 (Histogram)":
        x_col = st.selectbox("데이터 분포를 볼 컬럼 선택:", df.columns)
        fig = px.histogram(df, x=x_col, title=f"{x_col} 분포 히스토그램")

with col2:
    st.subheader("생성된 그래프")
    if 'fig' in locals(): # fig가 정의된 경우에만 그래프를 그림
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("그래프 유형을 선택하고 설정을 완료하면 여기에 그래프가 표시됩니다.")

st.write("---")
st.markdown("Made with ❤️ by Streamlit and Plotly")
