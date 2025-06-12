import streamlit as st

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

st.markdown("\n")
test_file = st.file_uploader("작성한 도면 PDF를 업로드하세요", type=["pdf", "jpg", "png"], key="test")
if test_file:
    st.markdown(f"**✅ 정답지 업로드됨:** `{test_file.name}`")