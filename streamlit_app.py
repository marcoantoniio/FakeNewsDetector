import streamlit as st
from google import genai
from PIL import Image

API_KEY = st.secrets["google"]["api_key"]

client = genai.Client(api_key=API_KEY)

st.title("📰 Detector de Fake News com Gemini")
st.write("Envie uma imagem (notícia, postagem, manchete, etc.) e veja se parece ser fake news.")

uploaded_file = st.file_uploader("Envie uma imagem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem enviada", use_container_width=True)

    if st.button("Analisar imagem"):
        with st.spinner("Analisando com o modelo Gemini..."):
            try:
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash-lite",
                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": (
                                        "Analise esta imagem e diga se o conteúdo parece ser fake news. "
                                        "Explique brevemente o motivo da resposta."
                                    )
                                },
                                {
                                    "inline_data": {
                                        "mime_type": uploaded_file.type,
                                        "data": uploaded_file.getvalue()
                                    }
                                }
                            ]
                        }
                    ]
                )

                st.subheader("🧠 Resposta do Gemini:")
                st.write(response.text)

            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
