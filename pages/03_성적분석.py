import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Streamlit 페이지 설정은 모든 import 문 바로 다음에 와야 합니다.
st.set_page_config(layout="wide", page_title="학생 성적 분석 및 예측 시스템")

# --- 설정 및 데이터 생성 ---
# ... (이전 코드와 동일)
subjects_korean = ['국어', '영어', '수학', '역사', '사회', '과학']
subjects_english = ['Korean', 'English', 'Math', 'History', 'Social', 'Science']
subject_map = dict(zip(subjects_korean, subjects_english))

num_students = 150
num_exams = 10

@st.cache_data
def generate_and_load_data():
    """더미 데이터를 생성하고 DataFrame으로 반환합니다."""
    data = {}
    for student_id in range(1, num_students + 1):
        student_name = f'Student_{student_id}'
        for subject_kor, subject_eng in subject_map.items():
            for exam_num in range(1, num_exams + 1):
                column_name = f'{subject_eng}_Exam_{exam_num}'
                score = np.random.randint(0, 101)
                if student_name not in data:
                    data[student_name] = {}
                data[student_name][column_name] = score
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index.name = 'Student_Name'
    return df

df = generate_and_load_data()

st.title('📚 학생 성적 분석 및 예측 시스템') # 이제부터 다른 Streamlit 명령어 사용
st.write("학생들의 과목별 시험 성적을 분석하고, 다음 시험 성적을 예측합니다.")

# 사이드바 메뉴
st.sidebar.header('메뉴')
analysis_type = st.sidebar.radio(
    "원하는 분석을 선택하세요:",
    ('Data Overview', 'Grade Analysis', 'Grade Prediction')
)

# --- 1. Data Overview (데이터 개요) ---
if analysis_type == 'Data Overview':
    st.header('📊 Data Overview')
    st.write("생성된 학생 성적 데이터의 일부를 보여줍니다.")
    st.dataframe(df.head())
    st.write(f"Total Students: {df.shape[0]} students")
    st.write(f"Total Exam Items: {df.shape[1]} items")

    st.subheader('Descriptive Statistics')
    st.write(df.describe())

    st.subheader('Missing Values Check')
    if df.isnull().sum().sum() == 0:
        st.info("No missing values found in the data.")
    else:
        st.warning(f"Missing values found: {df.isnull().sum().sum()}! Further preprocessing may be needed.")

# --- 2. Grade Analysis (성적 분석) ---
elif analysis_type == 'Grade Analysis':
    st.header('📈 Student Grade Analysis')

    # 학생 선택 드롭다운
    selected_student = st.selectbox(
        'Select a student for grade analysis:',
        df.index.tolist()
    )

    if selected_student:
        st.subheader(f'**{selected_student}**\'s Average Scores by Subject')
        student_scores = df.loc[selected_student]

        # 과목별 평균 성적 계산
        subject_avg_scores = {}
        for subject_eng in subjects_english:
            subject_exam_cols = [col for col in student_scores.index if col.startswith(subject_eng)]
            if subject_exam_cols:
                subject_scores_values = student_scores[subject_exam_cols].astype(float)
                subject_avg_scores[subject_eng] = subject_scores_values.mean()

        avg_scores_df = pd.DataFrame(subject_avg_scores.items(), columns=['Subject', 'Average Score'])
        st.dataframe(avg_scores_df.set_index('Subject'))

        # 막대 그래프 시각화
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Subject', y='Average Score', data=avg_scores_df, ax=ax, palette='viridis')
        ax.set_ylim(0, 100)
        ax.set_title(f'{selected_student}\'s Average Scores by Subject')
        ax.set_ylabel('Average Score (Points)')
        st.pyplot(fig)
        plt.close(fig) # 그래프 메모리 해제

        st.subheader(f'**{selected_student}**\'s Exam Score Trend by Subject')
        # 각 과목별 시험 점수 추이 그래프
        for subject_eng in subjects_english:
            exam_columns = [col for col in df.columns if col.startswith(f'{subject_eng}_Exam_')]
            if exam_columns:
                fig_line, ax_line = plt.subplots(figsize=(10, 4))
                subject_exam_scores = df.loc[selected_student, exam_columns].astype(float)
                ax_line.plot(range(1, num_exams + 1), subject_exam_scores, marker='o')
                ax_line.set_title(f'{selected_student}\'s {subject_eng} Exam Score Trend')
                ax_line.set_xlabel('Exam Number')
                ax_line.set_ylabel('Score')
                ax_line.set_xticks(range(1, num_exams + 1))
                ax_line.set_ylim(0, 100)
                st.pyplot(fig_line)
                plt.close(fig_line)


# --- 3. Grade Prediction (성적 예측) ---
elif analysis_type == 'Grade Prediction':
    st.header('🔮 Next Exam Grade Prediction')
    st.write("Predicts the next exam score based on previous exam scores.")

    # 예측할 학생 선택
    student_for_prediction = st.selectbox(
        'Select a student to predict next exam score:',
        df.index.tolist(),
        key='prediction_student_select'
    )

    # 시험 난이도 선택
    difficulty_mapping = {
        'Easy (쉬움)': 5,   # 점수 +5점 효과
        'Normal (보통)': 0, # 점수 변화 없음
        'Hard (어려움)': -5 # 점수 -5점 효과
    }
    selected_difficulty = st.radio(
        "Select the difficulty of the next exam:",
        list(difficulty_mapping.keys())
    )
    difficulty_adjustment = difficulty_mapping[selected_difficulty]


    if student_for_prediction:
        st.subheader(f'**{student_for_prediction}**\'s Next Exam Score Prediction Results (Difficulty: {selected_difficulty})')

        predictions = {}
        for subject_eng in subjects_english:
            exam_columns = [col for col in df.columns if col.startswith(f'{subject_eng}_Exam_')]
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

                # 난이도 조절 반영
                predicted_score_adjusted = predicted_score[0] + difficulty_adjustment

                # 점수 범위를 0-100으로 제한
                predicted_score_adjusted = np.clip(predicted_score_adjusted, 0, 100)
                predictions[subject_eng] = f'{predicted_score_adjusted:.2f} points'

                # 예측 추이 그래프
                fig_pred, ax_pred = plt.subplots(figsize=(10, 5))
                ax_pred.plot(X.flatten(), y, marker='o', label='Actual Scores')
                ax_pred.plot(next_exam_num, predicted_score_adjusted, marker='X', color='red', markersize=10, label=f'Predicted Score ({selected_difficulty})')
                ax_pred.set_title(f'{student_for_prediction}\'s {subject_eng} Next Exam Prediction')
                ax_pred.set_xlabel('Exam Number')
                ax_pred.set_ylabel('Score')
                ax_pred.set_xticks(list(range(1, num_exams + 1)) + [next_exam_num])
                ax_pred.set_ylim(0, 100)
                ax_pred.legend()
                st.pyplot(fig_pred)
                plt.close(fig_pred)

            else:
                predictions[subject_eng] = "Not enough data (requires at least 2 exams)"

        # 예측 결과 요약
        st.write("---")
        st.subheader('Prediction Summary')
        for subject, pred_score in predictions.items():
            st.write(f"**{subject}**: {pred_score}")
