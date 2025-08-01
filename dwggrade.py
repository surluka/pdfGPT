import streamlit as st
import pandas as pd 

# st.markdown("#### 교수자용")

# # st.markdown("#### (제품디자인) 오토캐드(CAD 2D)+ 3D 인벤터(Inventor)& 3D프린팅(제품모델링+디자인 & 퓨전360) B")
# st.markdown("\n")
# st.title("오토캐드 도면작성 평가 데이터 업로드")
# st.markdown("\n")

# st.markdown("📁 파일 업로드")

# answer_file = st.file_uploader("정답지 파일을 업로드하세요", type=["pdf", "jpg", "png"], key="answer")
# test_file = st.file_uploader("시험지 파일을 업로드하세요", type=["pdf", "jpg", "png"], key="test")

# if answer_file:
#     st.success("✅ 정답지 파일이 업로드되었습니다.")

# if test_file:
#     st.success("✅ 시험지 파일이 업로드되었습니다.")

st.markdown("#### (제품디자인) 오토캐드(CAD 2D)+ 3D 인벤터(Inventor)& 3D프린팅(제품모델링+디자인 & 퓨전360) B")
st.markdown("\n")
st.title("오토캐드 도면작성 수시 평가")
st.markdown("\n")
evaluator_name = st.text_input("이름", placeholder="평가자 이름을 입력 하세요")

#st.markdown("📁 파일 업로드")
#test_file = st.file_uploader("시험지 파일을 업로드하세요", type=["pdf", "jpg", "png"], key="test")
st.markdown("\n")
st.download_button(
    label="📥 시험지 다운로드",
    data="이건 예시 텍스트입니다.",
    file_name="result.txt",
    mime="text/plain")

uploaded_file = st.file_uploader("훈련생이 작성한 도면 (평가지 PDF)을 업로드하세요", type=["pdf"], key="eval_pdf")

if uploaded_file:
    st.success(f"✅ 업로드 완료: {uploaded_file.name}")

    # 이미지 미리보기 표시
    st.subheader("📄 정답지 보기")
    st.image("./images/정답지.jpg", caption="", use_container_width=True)

    st.subheader("📝 훈련생 평가지 보기")
    st.image("./images/평가지.jpg", caption="", use_container_width=True)


st.markdown("### 📝 도면 상세 평가 (전산응용기계제도기능사 기준)")
st.markdown("---")

st.markdown("""
#### 📌 1. 도면 구성 및 배치
- **문제 지점**: 중심선(Center Line)이 전체 도형에 대해 **표시되지 않음**.
- **해설**: 중심선은 대칭 요소나 축 기준이 필요한 도형에서 반드시 포함되어야 합니다. 현재 도면에서는 축 방향이 명확하지 않아 해독이 어려우며, **치수선 간격도 도형과 너무 가까워 시인성이 떨어집니다**.
- **개선 방향**: 모든 중심 도형에 대해 중심선 삽입, 치수선은 도형에서 **2~3mm 이상 간격**을 두고 배치.

---

#### 📌 2. 치수 기입
- **문제 지점**: Ø60, Ø80 등의 **직경 기호가 누락**되어 있고, 일부 **공차 기입이 생략**됨.
- **해설**: 전산응용기계제도기능사 기준에서는 **단위 생략은 가능하나 기호는 생략 불가**합니다. 특히 축 및 구멍 등은 직경 표시가 없으면 **형상 해석에 큰 오류**를 유발합니다.
- **개선 방향**: 모든 원형 요소에 Ø 기호를 명확하게 기입하고, 필요한 치수에는 **±0.01 또는 H7 등 공차 기입** 필수.

---

#### 📌 3. 단면도 및 해칭 표현
- **문제 지점**: 단면 표현은 되어 있으나, **해칭 간격이 일정하지 않고** 일부 구간은 누락됨.
- **해설**: 단면 해칭은 가공된 내부 형상을 표현하는 중요한 수단입니다. 간격이 좁거나 넓거나 누락되면, **내부 구조 해석에 오류**가 발생할 수 있습니다.
- **개선 방향**: 해칭 간격은 **일반적으로 2mm 간격**, 방향은 통일. 절단선은 **굵기와 유형으로 명확히 구분**.

---

#### 📌 4. 공차 및 형상 기입
- **문제 지점**: 일부 도형에서 **위치공차(예: ⌖, ∅0.015) 및 평행도 기호 누락**.
- **해설**: 위치공차는 부품 간 결합에서 매우 중요한 요소입니다. 기능사 실기 도면에서는 요구된 **형상공차와 위치공차를 명확히 표현해야 하며**, 누락되면 **도면 불합격 사유**가 됩니다.
- **개선 방향**: 해당 요소에 대해 형상 기호 박스를 활용해 **정확한 기입** 필요. 표준에 따라 작성(예: ⌖ 0.02 | A).

---

#### 📌 5. 문자 및 기타 사항
- **문제 지점**: 일부 문자 크기가 작고, 정렬이 **불규칙**함. 단위 일부는 **mm 혼용**, 영어 약어 사용.
- **해설**: 도면에서 문자는 치수와 함께 가장 기본적인 정보 전달 수단입니다. KS 규격에서는 **문자 크기, 간격, 정렬**을 통일하도록 명시하고 있으며, 오탈자 및 단위 혼용은 **실제 제조 공정 오류**로 이어질 수 있습니다.
- **개선 방향**: 문자 크기는 2.5~3.5mm로 통일, 단위는 mm 생략 가능하지만 혼용 금지. **정렬 기준선에 맞춰 배치**할 것.
""")

st.markdown("#### ✅ 종합 평가 요약표")

# 간결하게 요약한 평가 항목
evaluation_data = pd.DataFrame({
    "항목": ["도면 구성", "치수 기입", "단면 표현", "공차 기입", "기타 요소"],
    "평가": ["양호", "미흡", "미흡", "보통", "보통"],
    "비고": [
        "중심선 누락, 간격 조정 필요",
        "Ø 기호 및 단위 일부 누락",
        "해칭 간격 불균형",
        "공차 기호 누락",
        "문자 크기와 정렬 불균형"
    ]
})

st.table(evaluation_data)