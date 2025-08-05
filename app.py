import streamlit as st
import fitz  # PyMuPDF
from google import generativeai as genai
import re
import plotly.graph_objects as go

genai.configure(api_key="YOUR_API_KEY")

st.set_page_config(page_title="Resume Rating")
st.title("Resume Rating Tool")

uploaded_pdf = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_pdf:
    st.write(f"Uploaded File: **{uploaded_pdf.name}**")

    with st.spinner("Processing..."):
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=300)
        image_path = "resume_page.png"
        pix.save(image_path)

    with open(image_path, "rb") as f:
        image_data = f.read()

    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = "Rate this resume from 1 to 10. Start with the number only. Then give suggestions to improve this resume."

    with st.spinner("Getting feedback..."):
        response = model.generate_content([
            {"text": prompt},
            {"mime_type": "image/png", "data": image_data}
        ])

    full_response = response.text.strip()
    match = re.match(r"(\d+)", full_response)

    if match:
        rating = int(match.group(1))
        rating = min(max(rating, 0), 10)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=rating,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Resume Score (out of 10)"},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': "blue"},
                'bgcolor': "lightgray"
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Suggestions to Improve:")
        suggestions = full_response.split("\n", 1)[1] if "\n" in full_response else "No suggestions found."
        st.write(suggestions)
    else:
        st.error("Could not extract a numeric rating from Gemini's response.")
