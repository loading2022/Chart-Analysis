import streamlit as st
import io
import os
import base64
from PIL import Image
from openai import OpenAI


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
def analyze_image(image):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "請問x軸y軸是什麼意思，有幾個顯示的目標、物件或是曲線，接下來標的或物件之間有和關聯，再來有沒有特殊的現象呈現，最後再請把前面所有內容彙整成一個精簡報告。請注意將顏色辨識正確，並且適當進行分析"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/*;base64,{image}",
                        }
                    },
                ],
            }
        ],
    )

    result = completion.choices[0].message.content
    return result

st.title('Image Upload and Analysis Demo')
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    image = Image.open(io.BytesIO(bytes_data))
    st.image(image, caption='Uploaded Image', use_column_width=True)
    base64_image = base64.b64encode(bytes_data).decode()
    result = analyze_image(base64_image)
    st.write(result)
