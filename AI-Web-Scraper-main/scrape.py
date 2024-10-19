
import cloudscraper
from sentence_transformers import SentenceTransformer
import numpy as np
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time

from annoy import AnnoyIndex

from playwright.sync_api import sync_playwright

import streamlit as st


from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


# def scrape_website(website_url):
#     # Using cloudscraper to bypass 403 errors
#     scraper = cloudscraper.create_scraper()  # Create a cloudscraper instance
#     response = scraper.get(website_url)

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
#         # Use a browser context to set the user agent
#         context = browser.new_context(
#             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
#             viewport={'width': 1920, 'height': 1080}
#         )
#         page = context.new_page()

#         # Navigate to the website
#         page.goto(website_url)
#         page.wait_for_selector('body')  # Wait for the body to load
#         print("Page loaded...")

#         html = page.content()  # Get the HTML content of the page
#         browser.close()

#         return html

import cloudscraper
from bs4 import BeautifulSoup


def scrape_website(website_url):
    # Using cloudscraper to bypass 403 errors
    scraper = cloudscraper.create_scraper()  # Create a cloudscraper instance
    response = scraper.get(website_url)

    if response.status_code == 200:
        print("Page successfully scraped using cloudscraper...")
        html = response.content
    else:
        print(
            f"Failed to scrape the website. Status code: {response.status_code}")
        html = None

    return html


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, chunk_size=500):
    words = dom_content.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def generate_embeddings(chunks, embedding_model):
    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        batch_size=8  # Adjust batch size as needed
    )
    return embeddings


def store_embeddings(embeddings):
    dimension = embeddings.shape[1]
    index = AnnoyIndex(dimension, 'angular')
    for i, vector in enumerate(embeddings):
        index.add_item(i, vector)
    index.build(10)  # Number of trees
    return index

# When the user provides a parsing description, the function generates an embedding for the query using the same embedding model.
# It then searches the Annoy index to find the top k chunks that are most similar to the query embedding.


def retrieve_relevant_chunks(query, index, chunks, embedding_model, top_k=5):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True)
    indices = index.get_nns_by_vector(
        query_embedding[0], top_k, include_distances=False)
    relevant_chunks = [chunks[i] for i in indices]
    return relevant_chunks
