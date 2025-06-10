# app.py
import os
import streamlit as st
from openai import OpenAI

# ——— 환경변수에 OPENAI_API_KEY 를 설정하세요. ———
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_checked_answers(img_bytes: bytes) -> str:
    """
    GPT-4o Vision API 를 호출해,
    ‘질문 번호(question)와 선택지(answer)를 JSON 리스트 형태로 반환’해 달라 요청합니다.
    """
    resp = client.chat.completions.create(
        model="gpt-4o",
        multimodal_inputs=[
            {"type": "image", "image": img_bytes},
            {"type": "text",  "text": (
                "이 이미지의 객관식 문항에서, 훈련생이 체크한 질문 번호(question)와 "
                "선택지(answer)를 JSON 리스트 형태로 알려주세요.\n"
                "예시: [{\"question\":1, \"answer\":2}, {\"question\":4, \"answer\":3}, ...]"
            )}
        ]
    )
    return resp.choices[0].message.content  # 이미 JSON 문자열 형태로 올 겁니다.


def main():
    st.set_page_config(page_title="체크된 객관식 답안 추출기", layout="wide")
    st.title("✅ 체크된 객관식 답안 추출기")

    st.markdown(
        """
        1️⃣ ‘이미지 파일 업로드’에서 다중 선택을 켭니다.  
        2️⃣ 한 번에 여러 이미지를 올린 뒤, ‘추출 시작’ 버튼을 누르면  
        3️⃣ 아래 채팅창 형태로 각각의 결과를 보여줍니다.
        """
    )

    uploaded_files = st.file_uploader(
        "이미지 파일 업로드 (다중 선택 가능)", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("🕵️‍♂️ 추출 시작"):
            for img in uploaded_files:
                # 사용자 메시지
                st.chat_message("user").write(f"🔍 `{img.name}` 이미지 분석해주세요.")
                img_bytes = img.read()

                # 어시스턴트 메시지 (API 호출 포함)
                with st.chat_message("assistant"):
                    with st.spinner(f"{img.name} 처리 중..."):
                        try:
                            result = extract_checked_answers(img_bytes)
                            st.write(result)
                        except Exception as e:
                            st.error(f"에러 발생: {e}")

if __name__ == "__main__":
    main()
