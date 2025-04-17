import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))
from email_reader import authenticate_gmail, fetch_news_links
from article_scraper import scrape_batch

st.set_page_config(page_title="AI Automation Hub", layout="wide")
st.sidebar.title("Workflow Navigator")
section = st.sidebar.radio("Choose Module", [
    "📩 Read Emails",
    "🌐 Scrape Articles",
    "🔢 Score & Select News",
    "🤖 Generate LinkedIn Posts",
    "🔍 Lead Detection",
    "✉️ Outreach & Messaging",
    "📰 Build Newsletters",
])

st.title("Custom Automation App")

if section == "📩 Read Emails":
    st.header("Step 1: Email Reader")
    st.info("Connect to your email and extract news links.")
    if st.button("Connect Gmail & Fetch Links"):
        service = authenticate_gmail()
        links = fetch_news_links(service)
        if links:
            st.success(f"Found {len(links)} links:")
            for link in links:
                st.markdown(f"- [{link}]({link})")
        else:
            st.warning("No links found.")

elif section == "🌐 Scrape Articles":
    st.header("Step 2: Article Scraper")
    st.info("Fetch and parse webpages linked in emails.")
    urls = st.text_area("Paste article URLs (one per line)", height=150)
    url_list = [u.strip() for u in urls.splitlines() if u.strip()]
    if st.button("Scrape Articles"):
        if url_list:
            with st.spinner("Scraping articles..."):
                articles = scrape_batch(url_list)
            if articles:
                st.success(f"Scraped {len(articles)} articles:")
                for url, content in articles.items():
                    st.subheader(url)
                    st.markdown(content[:1000] + "..." if len(content) > 1000 else content)
            else:
                st.warning("No articles could be scraped.")
        else:
            st.warning("Please enter at least one URL.")
