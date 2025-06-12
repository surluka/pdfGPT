import streamlit as st

st.markdown("#### (제품디자인) 오토캐드(CAD 2D)+ 3D 인벤터(Inventor)& 3D프린팅(제품모델링+디자인 & 퓨전360) B")
st.markdown("\n")
st.title("사전평가")
st.markdown("\n")

evaluator_name = st.text_input("이름", placeholder="평가자 이름을 입력 하세요")

st.write("1. 열을 가하면 녹아내려 다시 가소성을 띠는 수지로, 재활용하기가 비교적 쉬운 열가소성 수지는 무엇인가요?")

options = ["① 알루미늄", "② ABS", "③ 기계구조용 탄소강", "④ 회주철"]
selected_option = st.radio("정답을 선택하세요:", options, index=None)

st.markdown("\n")

st.write("2. 제품 전체의 부품들에 대한 구성 요소를 정리한 시트로 정확한 데이터를 통하여 원가 및 관련 구성물들을 관리 하는 것을 무엇이라 하나?")

options = ["① BOM", "② PP", "③ MP", "④ LP"]
st.radio("정답을 선택하세요:", options, index=None)

st.markdown("\n")

st.write("3. 컴퓨터를 이용한  설계로 제품,건축,토목,플랜트 설계등에 매우 다양한 분야에서 도면을 제작하기 위해 사용되는 소프트웨어는 무엇인가요?")

st.image("images/image01.png")

options = ["① Auto CAD", "② Photoshop", "③ illustrator", "④ Premiere"]
st.radio("정답을 선택하세요:", options, index=None)

st.markdown("\n")

st.write("19. 3D 프린터 출력후 제품에서 제거해야 되는 부분을 무엇이라고 하나?")

options = ["① 베드", "② 지지대", "③ 노즐", "④ G-CODE"]
st.radio("정답을 선택하세요:", options, index=None)

st.markdown("\n")

st.write("20. 사람이나 사물의 3차원 형상을 측정하여 3D 데이터를 얻는 장비를 무엇이라고 하나?")

st.image("images/image02.png")

options = ["① 3D스캐너", "② 3D압출기", "③ 필라멘트", "④ 3D구동부"]
st.radio("정답을 선택하세요:", options, index=None)

if st.button("📨 최종제출"):
    st.success("제출이 완료되었습니다. 수고하셨습니다!")


st.markdown("\n")

st.markdown("최종 점수 : 75점")


wrong_answers = [3, 7, 9, 13, 17]

# 틀린 문제별 설명 딕셔너리
explanations = {
    3: "정답은 '① Auto CAD'입니다. 'Photoshop', 'Illustrator', 'Premiere'는 그래픽, 영상, 디자인용 소프트웨어로 CAD 설계와는 관련이 없습니다.",
    7: "정답은 '② 2점투시'입니다. 그림 설명에 따르면 좌우 두 개의 소실점을 사용하는 투시도이므로 2점투시입니다. 1점 또는 3점, 4점은 다른 조건입니다.",
    9: "정답은 '③ 3D 모델링'입니다. 2D 도면은 평면이고, 렌더링은 시각화 기법, 솔리드는 표현 방식 중 하나로 정확한 개념 구분이 필요합니다.",
    13: "정답은 '③ 포지셔닝 맵'입니다. 상반된 키워드의 위치를 2차원 공간에서 시각화하는 도구이며, 디자인 컨셉이나 로드맵과는 다릅니다.",
    17: "정답은 '② FDM 방식'입니다. 열가소성 수지를 녹여 적층하는 방식이 FDM입니다. SLS, SLA, MJM은 전혀 다른 기술 원리입니다."
}

st.write("틀린 문항 : 3번, 7번, 9번, 13번, 7번")
st.write("총 5문항")

st.markdown("### ❌ 틀린 문제 분석")

for num in wrong_answers:
    st.write(f"**문제 {num}번:**")
    st.write(explanations[num])
    st.markdown("---")


st.markdown("\n")
st.markdown("\n")
# 대화형 질문-답변 창 만들기
# 미리 정의된 질문과 답변
qa_pairs = [
    ("3번 문제를 잘 모르겠어 좀더 자세하게 설명 해 줘!", "3번 문제는 CAD 소프트웨어에 대한 이해를 묻는 문제예요. 'Auto CAD'는 건축, 기계, 토목 등 다양한 분야에서 도면을 설계할 때 사용하는 전문 소프트웨어입니다. 반면 Photoshop이나 Illustrator는 그래픽 디자인용이고, Premiere는 영상 편집 도구입니다. 따라서 정답은 도면을 설계하는 데 특화된 '① Auto CAD'가 맞습니다."),
]

# 출력 (최근 질문이 위로)
for q, a in reversed(qa_pairs):
    st.markdown(f"**🙋 질문:** {q}")
    st.markdown(f"**🤖 답변:** {a}")
    st.markdown("---")

# 입력창만 보여주기 (플레이스홀더 포함, 라벨 없음)
st.text_input(label="궁금한 점을 입력해 보세요", placeholder="")