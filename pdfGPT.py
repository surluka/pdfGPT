import streamlit as st
import pdfplumber
import pandas as pd
import openai
import os
from dotenv import load_dotenv

# .env 에서 API 키 불러오기
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 출석 정보 추출 함수
def extract_attendance_summary(pdf_path: str, student_name: str):
    records = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table or len(table) < 2:
                continue

            df = pd.DataFrame(table[1:], columns=table[0])
            df.columns = [str(c).replace("\n", "").strip() for c in df.columns]
            df = df[df['성명'].notna()]
            if '성명' not in df.columns:
                continue

            if student_name in df['성명'].values:
                row = df[df['성명'] == student_name].iloc[0]

                try:
                    total = int(row['훈련일수'])
                    attended = int(row['출석일수'])
                    absent = int(row['결석일수'])
                except ValueError:
                    continue

                daily = [v for k, v in row.items() if k not in ['성명', '훈련일수', '출석일수', '결석일수']]
                late = daily.count('◎')
                early = daily.count('▲')

                return {
                    "name": student_name,
                    "total": total,
                    "attended": attended,
                    "absent": absent,
                    "late": late,
                    "early": early,
                    "completed": attended + absent,
                    "remaining": total - (attended + absent)
                }

    return None

# GPT 요약 생성 함수
def get_gpt_summary(attendance_info: dict):
    prompt = f"""
다음은 직업훈련 출석부에서 추출된 {attendance_info['name']} 학생의 출결 정보입니다:

- 총 훈련일수: {attendance_info['total']}일
- 출석일수: {attendance_info['attended']}일
- 결석일수: {attendance_info['absent']}일
- 지각일수: {attendance_info['late']}일
- 조퇴일수: {attendance_info['early']}일
- 현재까지 수업일수: {attendance_info['completed']}일
- 앞으로 남은 수업일수: {attendance_info['remaining']}일

이 정보를 바탕으로 아래와 같이 출력 요약을 해주세요:

1. 위의 항목을 한눈에 보기 쉽게 정리
2. 지각, 조퇴, 결석 횟수에 따른 주의 멘트 포함 (예: 출결 문제 주의 필요)
3. 가능한 한 자연스러운 말투로 요약
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message['content']

# Streamlit UI
st.set_page_config(page_title="출석 분석 앱", layout="centered")
st.title("📋 직업훈련 출석 요약 생성기 (GPT-4o)")

pdf_file = st.file_uploader("출석부 PDF 파일을 업로드하세요", type=["pdf"])
student_name = st.text_input("학생 이름을 입력하세요")

if pdf_file and student_name:
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.read())

    st.info("📑 PDF 분석 중...")
    info = extract_attendance_summary("temp.pdf", student_name)

    if info:
        st.success(f"✅ {student_name} 학생의 출석 정보를 불러왔습니다.")
        st.markdown("### 🤖 AI 요약 결과")
        summary = get_gpt_summary(info)
        st.write(summary)
    else:
        st.error("❌ 해당 학생 정보를 PDF에서 찾을 수 없습니다.")
