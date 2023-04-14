import requests
from bs4 import BeautifulSoup

def scrape_wikipedia_article(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the article body
    article_body = ""
    for paragraph in soup.find_all("p"):
        article_body += paragraph.text

    # Extract citations
    citations = []
    for ref in soup.find_all("span", class_="reference-text"):
        citations.append(ref.text)

    # Extract extraneous information (info box, tables, etc.)
    extraneous_info = {}
    infobox = soup.find("table", class_="infobox")
    if infobox:
        extraneous_info["infobox"] = infobox.text

    tables = soup.find_all("table")
    if tables:
        extraneous_info["tables"] = []
        for table in tables:
            extraneous_info["tables"].append(table.text)

    return {
        "body": article_body,
        "citations": citations,
        "extraneous_info": extraneous_info,
    }

# Example usage:
# url = "https://en.wikipedia.org/wiki/OpenAI"
# result = scrape_wikipedia_article(url)
# print(result)