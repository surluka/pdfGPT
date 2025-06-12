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
    image_blocks = []
    question_bboxes = {}

    for page_index, page in enumerate(doc):
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
                    if re.match(r"^\d{1,2}\.", text):
                        question_bboxes[int(text.split('.')[0])] = {
                            "page": page_index,
                            "y": span.get("bbox", [0, 0])[1]
                        }
                if line_text.strip():
                    lines.append((line_text.strip(), page_index))

        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            rect = fitz.Rect(img[1], img[2], img[3], img[4]) if len(img) >= 5 else None
            image_blocks.append({"page": page_index, "bbox": rect, "image": image_bytes})

    full_text = "\n".join([t[0] for t in lines])
    cleaned_text = remove_box_text(full_text)
    cleaned_lines = [line.strip() for line in cleaned_text.splitlines() if line.strip()]

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
                "options": options,
                "answer": None,
                "images": []
            })

    answers = [extract_answer_index(ans) for ans in red_answers]
    for i in range(len(questions)):
        questions[i]["answer"] = answers[i] if i < len(answers) else None

    for question in questions:
        qnum = question["number"]
        if qnum not in question_bboxes:
            continue
        page = question_bboxes[qnum]["page"]
        y = question_bboxes[qnum]["y"]
        y_next = float("inf")
        for next_q in range(qnum + 1, qnum + 5):
            if next_q in question_bboxes and question_bboxes[next_q]["page"] == page:
                y_next = question_bboxes[next_q]["y"]
                break

        for img in image_blocks:
            if img["page"] == page:
                img_y = img["bbox"].y0 if img["bbox"] else 0
                if y <= img_y < y_next:
                    question["images"].append(img["image"])

    return questions

# Streamlit 앱 실행

# 상단 소제목 (작은 글씨)
st.markdown("#### 교수자용")
st.markdown("\n")
st.title("📘 AI 기반 필답형 CBT 자동생성 시스템(PDF 기반) ")
st.markdown("\n")
uploaded_file = st.file_uploader("정답지 PDF 파일을 업로드하세요", type="pdf")

if uploaded_file:
    questions = parse_pdf(uploaded_file)
    st.success(f"총 {len(questions)}문항을 불러왔습니다.")

    st.subheader("📝 시험 응시")
    user_answers = {}

    for q in questions:
        st.markdown(f"**{q['number']}. {q['question']}**")
        for img in q.get("images", []):
            st.image(img, use_column_width=True)
        if len(q['options']) == 4:
            selected = st.radio("문항 보기 선택", q['options'], key=q['number'], index=None, label_visibility="collapsed")
            if selected is not None:
                user_answers[q['number']] = q['options'].index(selected)
        else:
            st.warning("보기 4개를 찾을 수 없습니다.")
        st.divider()

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
