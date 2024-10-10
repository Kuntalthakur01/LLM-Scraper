

import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
from llm_insights import generate_llm_insights
from PIL import Image
from io import BytesIO
import base64
import plotly.express as px
import pandas as pd

# Function to convert image to base64


def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


# Set up Streamlit page configuration
st.set_page_config(page_title="LLM Web Scraper",
                   page_icon="image (1).jpeg", layout="wide")

# Load and display the AI-generated image
ai_image = Image.open(
    "/Users/kuntal/Documents/Github/LLM-Scraper/AI-Web-Scraper-main/image (1).jpeg")
img_base64 = image_to_base64(ai_image)
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/jpeg;base64,{img_base64}" width="600"/>
    </div>
    """, unsafe_allow_html=True
)


def show_insights_page(parsed_results):
    if parsed_results:
        st.write("Generating insights... .. ..")
        insights = generate_llm_insights(parsed_results)  # Corrected call
        st.write("### Insights Generated:")
        st.write(insights)
    else:
        st.error(
            "No parsed results available to generate insights. Please parse some content first.")

# Function to show insights page
# def show_insights_page(parsed_results):
#     if parsed_results:
#         st.write("Generating insights... .. ..")
#         insights = generate_llm_insights(parsed_results)
#         if isinstance(insights, dict) and 'text' in insights:
#             st.write("### Insights Generated:")
#             st.write(insights['text'])

#             # Check if visualizations are present and not empty
#             if 'visualizations' in insights and insights['visualizations']:
#                 for viz in insights['visualizations']:
#                     try:
#                         if viz['type'] == 'bar_chart':
#                             df = pd.DataFrame(viz['data'])
#                             fig = px.bar(df, x='X', y='Y', title=viz['title'])
#                             st.plotly_chart(fig)
#                         elif viz['type'] == 'pie_chart':
#                             df = pd.DataFrame(viz['data'])
#                             fig = px.pie(df, names='labels',
#                                          values='values', title=viz['title'])
#                             st.plotly_chart(fig)
#                         elif viz['type'] == 'line_chart':
#                             df = pd.DataFrame(viz['data'])
#                             fig = px.line(df, x='X', y='Y', title=viz['title'])
#                             st.plotly_chart(fig)
#                         # Add more visualization types as needed
#                     except Exception as e:
#                         st.write(f"Error generating visualization: {e}")
#                         st.write("Data not sufficient for visualization.")
#             else:
#                 st.write("Data not sufficient for visualization.")
#         else:
#             st.error("Unexpected insights format. Please check the LLM output.")
#     else:
#         st.error(
#             "No parsed results available to generate insights. Please parse some content first."
#         )


# Header and title styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 3rem;
        color: #ff6347;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 3px 3px 2px #FFFF;
    }
    .sub-title {
        font-size: 1.5rem;
        color: #4f8a8b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .button-style {
        background-color: #00c2cb;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1rem;
        transition: 0.3s;
    }
    .button-style:hover {
        background-color: #28a745;
        color: #fff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>LLM Web Scraper</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<p class='sub-title'>Scrape any website using LLM Scraper supercharged by Large Language Model.</p>",
    unsafe_allow_html=True
)

# Input for website URL
url = st.text_input("Enter Website URL")

# Sequential process - Scraping first
if st.button("Scrape Website", key="scrape"):
    if url:
        st.write("Scraping the website...")
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)
        st.session_state.dom_content = cleaned_content
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)

if 'dom_content' in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")
    if st.button("Parse Content"):
        parsed_results = parse_with_ollama(
            [st.session_state['dom_content']], parse_description)
        # Store parsed results in session state
        st.session_state['parsed_results'] = parsed_results
        st.write("### Parsed Result:")
        st.write(parsed_results)

    if st.button('Generate Insights') and 'parsed_results' in st.session_state:
        # Pass parsed results to insights generation function
        show_insights_page(st.session_state['parsed_results'])

# Function to show insights page
