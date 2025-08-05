##  Final `README.md` for **Resume-Rating-Tool**

````markdown
# Resume-Rating-Tool

**Resume-Rating-Tool** is an AI-powered web application that evaluates resumes based on layout, content, and structure. Users upload a resume in PDF format, and the app uses Google's Gemini 2.5 flash model to generate a rating (out of 10) and actionable suggestions to improve the resume.

---

## Features

- Upload resumes in PDF format through a web interface
- Automatically converts the PDF into an image
- Sends the image to Gemini for analysis
- Extracts and displays a rating using a circular gauge
- Lists suggestions to improve the resume’s quality and presentation
- Simple, modern user interface built with Streamlit

---

## Technologies Used

| Technology            | Purpose                             |
|------------------------|--------------------------------------|
| Python                 | Main programming language            |
| Streamlit              | UI framework                         |
| PyMuPDF (`fitz`)       | PDF to image conversion              |
| Plotly                 | Ring-style gauge visualization       |
| `google-generativeai` | Gemini 1.5 Pro API interaction        |

---

## Setup Instructions

This guide will help you recreate the project on your local machine.

### 1. Prerequisites

- Python 3.9 or higher
- A Google account to generate a Gemini API key
- An internet connection
- (Optional) Anaconda and Visual Studio Code

---

### 2. Create a Python Environment (Recommended)

Using Anaconda Prompt:

```bash
conda create -n resume-rating python=3.11
conda activate resume-rating
````

---

### 3. Install Dependencies

Install the required libraries using pip:

```bash
pip install streamlit PyMuPDF google-generativeai plotly
```

---

### 4. Generate Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the key
5. Paste it into your `app.py` script as shown below

---

### 5. Save the Application Code

Create a file called `app.py` and paste the following code into it:

```python
import streamlit as st
import fitz  # PyMuPDF
from google import generativeai as genai
import re
import plotly.graph_objects as go

genai.configure(api_key="YOUR_API_KEY_HERE")

st.set_page_config(page_title="Resume Rating")
st.markdown(
    """
    <h1 style='text-align: center; font-family: Arial; color: #003366;'>
        ResumeIQ
    </h1>
    """,
    unsafe_allow_html=True
)

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

    model = genai.GenerativeModel("gemini-1.5-pro")
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
```

Replace `"YOUR_API_KEY_HERE"` with your actual Gemini API key.

---

### 6. Run the Application

In your terminal or Anaconda Prompt, run:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Project Structure

```
Resume-Rating-Tool/
├── app.py                # Main Streamlit app
├── resume_page.png       # Temporary image file (created at runtime)
└── README.md             # Project documentation

```

---

## Optional Enhancements

* Save feedback to a text or PDF report
* Add text-based analysis alongside image review
* Compare multiple resumes side-by-side
* Deploy the app to the web using Streamlit Cloud or Render
* Enable light/dark mode themes

---





## Credits

This application was built using:

* [Streamlit](https://streamlit.io)
* [Google Gemini API](https://ai.google.dev/)
* [PyMuPDF](https://pymupdf.readthedocs.io/)
* [Plotly](https://plotly.com/)

```

---


