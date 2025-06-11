import streamlit as st
import fitz  # PyMuPDF
import re
import os
from dotenv import load_dotenv

# 환경변수에서 OpenAI 키 불러오기
load_dotenv()

# 색상 및 정답 추출
def int_to_rgb(color_int):
    r = (color_int >> 16) & 255
    g = (color_int >> 8) & 255
    b = color_int & 255
    return (r, g, b)

def is_red(rgb):
    r, g, b = rgb
    return r > 180 and g < 100 and b < 100

def extract_answer_index(answer_text):
    for mark in ['①', '②', '③', '④']:
        if mark in answer_text:
            return {'①': 0, '②': 1, '③': 2, '④': 3}[mark]
    return None

# 박스(연관 능력단위 등) 내용 제거
def remove_box_text(text):
    return re.sub(r"연관 ?능력단위.*?(?:상\s+중\s+하)?", "", text, flags=re.DOTALL)

# 문제 및 정답 파싱 (anns.pdf 전용)
def parse_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    red_answers = []
    lines = []

    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                line_text = ""
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    rgb = int_to_rgb(span.get("color", 0))
                    if text:
                        line_text += text + " "
                    if text and is_red(rgb):
                        red_answers.append(text)
                if line_text.strip():
                    lines.append(line_text.strip())

    # 박스 제거
    full_text = "\n".join(lines)
    cleaned_text = remove_box_text(full_text)
    cleaned_lines = [line.strip() for line in cleaned_text.splitlines() if line.strip()]

    # 문제 블록 분할
    blocks = []
    current_block = []
    for line in cleaned_lines:
        if re.match(r"^\d{1,2}\.", line):
            if current_block:
                blocks.append(current_block)
            current_block = [line]
        else:
            current_block.append(line)
    if current_block:
        blocks.append(current_block)

    # 문제와 보기 추출 (anns.pdf 기준)
    questions = []
    for block in blocks:
        number_match = re.match(r"^(\d{1,2})\.(.*)", block[0])
        if not number_match:
            continue
        qnum = int(number_match.group(1))
        qtext = number_match.group(2).strip()

        option_text = ' '.join([l for l in block[1:] if any(m in l for m in ['①', '②', '③', '④'])])
        parts = re.split(r'[①②③④]', option_text)
        options = [p.strip() for p in parts if p.strip()]

        if len(options) == 4:
            questions.append({
                "number": qnum,
                "question": qtext,
                "options": options
            })

    # 정답 적용
    answers = [extract_answer_index(ans) for ans in red_answers]
    for i in range(len(questions)):
        questions[i]["answer"] = answers[i] if i < len(answers) else None

    return questions

# Streamlit 앱 실행
st.title("AI 기반 CBT 자동 생성 시스템 (pdf 기반)")

# 성명 입력란 추가 
name = st.text_area("성명을 입력하세요:", height=68)  # 텍스트 박스를 넓게 설정

# PDF 파일 업로드
uploaded_file = st.file_uploader("정답지 PDF 파일을 업로드하세요", type="pdf")

if uploaded_file:
    questions = parse_pdf(uploaded_file)
    st.success(f"총 {len(questions)}문항을 불러왔습니다.")

    st.subheader("📝 시험 응시")
    user_answers = {}

    for q in questions:
        st.markdown(f"**{q['number']}. {q['question']}**")
        if len(q['options']) == 4:
            selected = st.radio("문항 보기 선택", q['options'], key=q['number'], index=None, label_visibility="collapsed")
            if selected is not None:
                user_answers[q['number']] = q['options'].index(selected)
        else:
            st.warning("보기 4개를 찾을 수 없습니다.")
        st.divider()

    # 이미지 공간 확보
    # st.markdown("### PDF에서 추출된 이미지가 여기에 표시됩니다:")
    # st.empty()  # 나중에 이미지를 추가할 수 있도록 공간만 확보

    if st.button("제출하기"):
        correct = 0
        incorrect = []
        for q in questions:
            if user_answers.get(q['number']) == q['answer']:
                correct += 1
            else:
                incorrect.append((q['number'], q['options'][q['answer']] if q['answer'] is not None else "(정답 없음)", q))

        st.subheader("✅ 결과 요약")
        st.write(f"총 {len(questions)}문항 중 {correct}개 정답")
        st.write(f"점수: {correct * 5}점 / {len(questions) * 5}점")

        if incorrect:
            st.markdown("#### ❌ 틀린 문항")
            for num, ans, q in incorrect:
                st.write(f"- {num}번 정답: {ans}")

    # GPT 채팅창
    st.markdown("### 🤖 AI와의 채팅")
    user_message = st.text_input("질문을 입력하세요:")

    if user_message:
        st.write(f"AI: '3번 문제에 대해서 설명을 해 줘' 에 대한 답변을 하겠습니다. 3번 문제의 경우 컴퓨터를 이용한 설계로 제품,건축,토목,플랜트 설계등 에서 사용되는 프로그램을 선택하는 문제 입니다. 선택하신 Photoshop 의 경우 이미지 편집을 할 수 있는 비트맵 전용 편집 프로그램 입니다.")