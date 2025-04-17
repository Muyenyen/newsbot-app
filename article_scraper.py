import trafilatura

def scrape_article_from_url(url):
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded)
    return None

def scrape_batch(urls, limit=5):
    extracted = {}
    for url in urls[:limit]:
        content = scrape_article_from_url(url)
        if content:
            extracted[url] = content
    return extracted
