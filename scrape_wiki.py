import requests
from bs4 import BeautifulSoup
import re

# specify the URL of the Wikipedia article to scrape
url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

# send a GET request to the URL
response = requests.get(url)

# parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# find the main content of the article (usually contained in a <div> element with the id "mw-content-text")
content_div = soup.find('div', {'id': 'mw-content-text'})

# remove any boilerplate formatting from the scraped text
text = re.sub(r'\[[0-9]+\]', '', content_div.get_text()) # remove citation numbers
text = re.sub(r'\s+', ' ', text) # remove excess whitespace
text = re.sub(r'\([^)]*\)', '', text) # remove text in parentheses
text = re.sub(r'\{\{.*?\}\}', '', text) # remove templates
text = re.sub(r'\[.*?\]', '', text) # remove text in square brackets
text = re.sub(r'<.*?>', '', text) # remove HTML tags
text = re.sub(r'\u200b', '', text) # remove zero-width space

# print the cleaned-up text
print(text)
import requests
from bs4 import BeautifulSoup
import re

# specify the URL of the Wikipedia article to scrape
url = "https://en.wikipedia.org/wiki/Web_scraping"

# send a GET request to the URL
response = requests.get(url)

# parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# find the main content of the article (usually contained in a <div> element with the id "mw-content-text")
content_div = soup.find('div', {'id': 'mw-content-text'})

# remove any boilerplate formatting from the scraped text
text = re.sub(r'\[[0-9]+\]', '', content_div.get_text()) # remove citation numbers
text = re.sub(r'\s+', ' ', text) # remove excess whitespace
text = re.sub(r'\([^)]*\)', '', text) # remove text in parentheses
text = re.sub(r'\{\{.*?\}\}', '', text) # remove templates
text = re.sub(r'\[.*?\]', '', text) # remove text in square brackets
text = re.sub(r'<.*?>', '', text) # remove HTML tags
text = re.sub(r'\u200b', '', text) # remove zero-width space

# print the cleaned-up text
print(text)
