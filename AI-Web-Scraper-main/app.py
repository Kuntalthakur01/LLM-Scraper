from annoy import AnnoyIndex
import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
)
from parse import parse_with_ollama
from llm_insights import generate_llm_insights
from PIL import Image
from io import BytesIO
import base64
from sentence_transformers import SentenceTransformer
import asyncio


# Initialize the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to convert image to base64


def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


# Set up Streamlit page configuration
st.set_page_config(page_title="LLM Web Scraper",
                   page_icon="image (1).jpeg", layout="wide")

# Load and display the AI-generated image
ai_image = Image.open("image (1).jpeg")  # Update path as necessary
img_base64 = image_to_base64(ai_image)

st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/jpeg;base64,{img_base64}" width="600"/>
    </div>
    """, unsafe_allow_html=True
)

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
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>LLM-Powered Data Mining</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<p class='sub-title'>Revolutionizing Web Scraping with Large Language Models for Seamless Data Extraction and Insight Generation.</p>",
    unsafe_allow_html=True
)

# Input for website URL
url = st.text_input("Enter Website URL")

# Initialize session state variables
if 'dom_content' not in st.session_state:
    st.session_state.dom_content = None
if 'embedding_model' not in st.session_state:
    st.session_state.embedding_model = embedding_model


# Button to scrape website
if st.button("Scrape Website", key="scrape"):
    if url:
        st.write("Scraping the website...")
        try:
            # Run the async function in the event loop
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)
            st.session_state.dom_content = cleaned_content
        except Exception as e:
            st.error(f"Error scraping website: {str(e)}")

# Display the DOM content
if 'dom_content' in st.session_state and st.session_state.dom_content:
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", st.session_state.dom_content, height=300)

    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content") and parse_description:
        parsed_results = parse_with_ollama(
            [st.session_state['dom_content']], parse_description)
        st.session_state['parsed_results'] = parsed_results

# Check if parsed results exist and allow generating insights
if 'parsed_results' in st.session_state:
    st.write("### Parsed Result:")
    st.write(st.session_state['parsed_results'])

    user_role = st.text_input(
        "Enter your role or the type of actionable insights you want (e.g., student, recruiter, business person).\n For example: I am a recruiter wanting to know about the tech this user used for projects so give me insights for assessing this interviewee."

    )

    if st.button('Generate Insights'):
        if user_role:
            st.write("Generating insights...")
            insights = generate_llm_insights(
                st.session_state['parsed_results'], user_role)
            st.write(f"### Insights Generated:")
            st.write(insights)
        else:
            st.error(
                "Please enter your role or the type of actionable insights you want.")

# Functions used in the app (you can keep the embedding functions as per your project requirements)


def generate_embeddings(chunks, model):
    embeddings = [model.encode(chunk) for chunk in chunks]
    return embeddings


def store_embeddings(embeddings):
    dimension = len(embeddings[0])
    index = AnnoyIndex(dimension, 'angular')
    for i, vector in enumerate(embeddings):
        index.add_item(i, vector)
    index.build(10)
    return index


def retrieve_relevant_chunks(query, index, chunks, model, top_k=5):
    query_embedding = model.encode(query)
    nearest_indices = index.get_nns_by_vector(query_embedding, top_k)
    relevant_chunks = [chunks[i] for i in nearest_indices]
    return relevant_chunks
