import pandas as pd
import numpy as np

# 학생 수 및 시험 과목 정의
num_students = 150
subjects = ['국어', '영어', '수학', '역사', '사회', '과학']
num_exams = 10 # 각 과목별 시험 횟수

# 더미 데이터 생성
data = {}
for student_id in range(1, num_students + 1):
    student_name = f'학생_{student_id}'
    for subject in subjects:
        for exam_num in range(1, num_exams + 1):
            column_name = f'{subject}_시험_{exam_num}'
            # 각 시험 점수는 0점에서 100점 사이의 정수로 무작위 생성
            score = np.random.randint(0, 101)
            if student_name not in data:
                data[student_name] = {}
            data[student_name][column_name] = score

# 딕셔너리를 DataFrame으로 변환
df = pd.DataFrame.from_dict(data, orient='index')
df.index.name = '학생_이름'

# 결과 확인
print(df.head())
print(f"\n생성된 데이터프레임의 크기: {df.shape}")

# CSV 파일로 저장 (선택 사항)
df.to_csv('student_scores.csv')
print("\n'student_scores.csv' 파일로 데이터가 저장되었습니다.")

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# --- 데이터 로드 및 전처리 ---
# (이전에 생성한 student_scores.csv 파일을 사용하거나, 데이터를 직접 생성)
try:
    df = pd.read_csv('student_scores.csv', index_col='학생_이름')
except FileNotFoundError:
    st.error("student_scores.csv 파일을 찾을 수 없습니다. 데이터를 생성하거나 경로를 확인해주세요.")
    # 파일이 없을 경우 더미 데이터 직접 생성 (위의 데이터 생성 코드를 여기에 포함)
    num_students = 150
    subjects = ['국어', '영어', '수학', '역사', '사회', '과학']
    num_exams = 10
    data = {}
    for student_id in range(1, num_students + 1):
        student_name = f'학생_{student_id}'
        for subject in subjects:
            for exam_num in range(1, num_exams + 1):
                column_name = f'{subject}_시험_{exam_num}'
                score = np.random.randint(0, 101)
                if student_name not in data:
                    data[student_name] = {}
                data[student_name][column_name] = score
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index.name = '학생_이름'
    st.success("CSV 파일을 찾을 수 없어 더미 데이터를 생성했습니다.")


# --- Streamlit 앱 구성 ---
st.set_page_config(layout="wide") # 페이지 전체 너비 사용
st.title('📚 학생 성적 분석 및 예측 시스템')
st.write("학생들의 과목별 시험 성적을 분석하고, 다음 시험 성적을 예측합니다.")

# 사이드바 메뉴
st.sidebar.header('메뉴')
analysis_type = st.sidebar.radio(
    "원하는 분석을 선택하세요:",
    ('데이터 개요', '성적 분석', '성적 예측')
)

# --- 1. 데이터 개요 ---
if analysis_type == '데이터 개요':
    st.header('📊 데이터 개요')
    st.write("생성된 학생 성적 데이터의 일부를 보여줍니다.")
    st.dataframe(df.head())
    st.write(f"총 학생 수: {df.shape[0]}명")
    st.write(f"총 시험 항목: {df.shape[1]}개")

    st.subheader('기술 통계')
    st.write(df.describe())

    st.subheader('결측치 확인')
    st.write(df.isnull().sum().sum())
    if df.isnull().sum().sum() == 0:
        st.info("데이터에 결측치가 없습니다.")
    else:
        st.warning("데이터에 결측치가 있습니다. 전처리 필요!")


# --- 2. 성적 분석 ---
elif analysis_type == '성적 분석':
    st.header('📈 학생 성적 분석')

    # 학생 선택 드롭다운
    selected_student = st.selectbox(
        '성적을 분석할 학생을 선택하세요:',
        df.index.tolist()
    )

    if selected_student:
        st.subheader(f'**{selected_student}**의 과목별 평균 성적')
        student_scores = df.loc[selected_student]

        # 과목별 평균 성적 계산
        subject_avg_scores = {}
        for subject in subjects:
            subject_exam_cols = [col for col in student_scores.index if col.startswith(subject)]
            if subject_exam_cols:
                subject_scores = student_scores[subject_exam_cols].astype(float)
                subject_avg_scores[subject] = subject_scores.mean()

        avg_scores_df = pd.DataFrame(subject_avg_scores.items(), columns=['과목', '평균 성적'])
        st.dataframe(avg_scores_df.set_index('과목'))

        # 막대 그래프 시각화
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='과목', y='평균 성적', data=avg_scores_df, ax=ax, palette='viridis')
        ax.set_ylim(0, 100)
        ax.set_title(f'{selected_student}의 과목별 평균 성적')
        ax.set_ylabel('평균 성적 (점)')
        st.pyplot(fig)
        plt.close(fig) # 그래프 메모리 해제

        st.subheader(f'**{selected_student}**의 과목별 시험 점수 추이')
        # 각 과목별 시험 점수 추이 그래프
        for subject in subjects:
            exam_columns = [col for col in df.columns if col.startswith(f'{subject}_시험_')]
            if exam_columns:
                fig_line, ax_line = plt.subplots(figsize=(10, 4))
                subject_exam_scores = df.loc[selected_student, exam_columns].astype(float)
                ax_line.plot(range(1, num_exams + 1), subject_exam_scores, marker='o')
                ax_line.set_title(f'{selected_student}의 {subject} 과목 시험 점수 추이')
                ax_line.set_xlabel('시험 회차')
                ax_line.set_ylabel('점수')
                ax_line.set_xticks(range(1, num_exams + 1))
                ax_line.set_ylim(0, 100)
                st.pyplot(fig_line)
                plt.close(fig_line)


# --- 3. 성적 예측 ---
elif analysis_type == '성적 예측':
    st.header('🔮 다음 시험 성적 예측')
    st.write("이전 시험 성적을 바탕으로 다음 시험 성적을 예측합니다.")

    # 예측할 학생 선택
    student_for_prediction = st.selectbox(
        '다음 시험 성적을 예측할 학생을 선택하세요:',
        df.index.tolist(),
        key='prediction_student_select'
    )

    if student_for_prediction:
        st.subheader(f'**{student_for_prediction}**의 다음 시험 성적 예측 결과')

        predictions = {}
        for subject in subjects:
            exam_columns = [col for col in df.columns if col.startswith(f'{subject}_시험_')]
            if len(exam_columns) >= 2: # 최소 2개 이상의 시험 데이터가 있어야 예측 가능
                # 특징 (X): 이전 시험 회차
                # 타겟 (y): 해당 시험 점수
                # 예측 모델 학습을 위해 학생의 해당 과목 성적만 추출
                subject_scores = df.loc[student_for_prediction, exam_columns].astype(float)
                X = np.array(range(1, len(subject_scores) + 1)).reshape(-1, 1)
                y = subject_scores.values

                # 선형 회귀 모델 학습
                model = LinearRegression()
                model.fit(X, y)

                # 다음 시험 (num_exams + 1) 예측
                next_exam_num = num_exams + 1
                predicted_score = model.predict(np.array([[next_exam_num]]))

                # 점수 범위를 0-100으로 제한
                predicted_score = np.clip(predicted_score[0], 0, 100)
                predictions[subject] = f'{predicted_score:.2f}점'

                # 예측 모델 평가 (선택 사항)
                # train_test_split (데이터가 충분할 경우)
                # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                # model.fit(X_train, y_train)
                # y_pred = model.predict(X_test)
                # mae = mean_absolute_error(y_test, y_pred)
                # r2 = r2_score(y_test, y_pred)
                # st.write(f"{subject} 예측 모델 MAE: {mae:.2f}, R2: {r2:.2f}")

                # 예측 추이 그래프
                fig_pred, ax_pred = plt.subplots(figsize=(10, 5))
                ax_pred.plot(X.flatten(), y, marker='o', label='실제 점수')
                ax_pred.plot(next_exam_num, predicted_score, marker='X', color='red', markersize=10, label='예측 점수')
                ax_pred.set_title(f'{student_for_prediction}의 {subject} 과목 다음 시험 예측')
                ax_pred.set_xlabel('시험 회차')
                ax_pred.set_ylabel('점수')
                ax_pred.set_xticks(list(range(1, num_exams + 1)) + [next_exam_num])
                ax_pred.set_ylim(0, 100)
                ax_pred.legend()
                st.pyplot(fig_pred)
                plt.close(fig_pred)

            else:
                predictions[subject] = "데이터 부족 (최소 2회 이상 시험 필요)"

        # 예측 결과 요약
        st.write("---")
        st.subheader('예측 요약')
        for subject, pred_score in predictions.items():
            st.write(f"**{subject}**: {pred_score}")
