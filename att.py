import streamlit as st
import pdfplumber
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env에서 API 키 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# PDF에서 전체 학생 이름 목록 추출
def extract_all_students(pdf_path: str):
    names = set()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table or len(table) < 2:
                continue
            df = pd.DataFrame(table[1:], columns=table[0])
            df.columns = [str(c).replace("\n", "").strip() for c in df.columns]
            if '성명' in df.columns:
                df = df[df['성명'].notna()]
                names.update(df['성명'].unique())
    return sorted(names)

# 학생 개별 출석 정보 추출
def extract_attendance_summary(pdf_path: str, student_name: str):
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

                symbols = [v for k, v in row.items() if k not in ['성명', '훈련일수', '출석일수', '결석일수']]
                late = symbols.count('◎')
                early = symbols.count('▲')

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

# GPT 요약 생성
def get_gpt_summary(att_info: dict):
    prompt = f"""
다음은 직업훈련 출석부에서 추출된 {att_info['name']} 학생의 출결 정보입니다:

- 총 훈련일수: {att_info['total']}일
- 출석일수: {att_info['attended']}일
- 결석일수: {att_info['absent']}일
- 지각일수: {att_info['late']}일
- 조퇴일수: {att_info['early']}일
- 현재까지 수업일수: {att_info['completed']}일
- 앞으로 남은 수업일수: {att_info['remaining']}일

이 정보를 바탕으로 아래 형식으로 자연스럽게 요약해 주세요:

1. 출석 상태를 항목별로 보기 좋게 정리
2. 지각·조퇴·결석 횟수가 많을 경우 주의 멘트를 포함
3. 자연스러운 문장으로 요약
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content

# Streamlit 앱 UI
st.set_page_config(page_title="출석 요약 생성기", layout="centered")
st.title("📋 직업훈련 출석 요약 (GPT-4o)")

pdf_file = st.file_uploader("출석부 PDF 파일을 업로드하세요", type=["pdf"])

if pdf_file:
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.read())

    # 드롭다운용 이름 목록 추출
    student_list = extract_all_students("temp.pdf")

    if not student_list:
        st.warning("학생 목록을 추출할 수 없습니다.")
    else:
        student_name = st.selectbox("학생을 선택하세요", student_list)

        if student_name:
            st.info("📑 출석 정보 분석 중...")
            info = extract_attendance_summary("temp.pdf", student_name)

            if info:
                st.success(f"✅ {student_name} 학생의 출결 정보를 분석했습니다.")
                st.markdown("### 🤖 GPT 요약 결과")
                summary = get_gpt_summary(info)
                st.write(summary)
            else:
                st.error("해당 학생 정보를 찾을 수 없습니다.")
