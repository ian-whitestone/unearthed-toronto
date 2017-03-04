"""Provides a scraper for Google search results"""
from bs4 import BeautifulSoup
import requests
import warnings

# Get soup object for a given url
def get_soup(url, filetype="lxml"):
    return BeautifulSoup(requests.get(url).text, filetype)

# Fetches google news search page for a given query and returns as a soup object
def get_search_soup(query):
    url = "https://www.google.ca/search?q={}".format(query)
    return get_soup(url)


# Parses an article soup element and returns the news article
# elements (title, thumbnail, link, description) as a dictionary
def parse_search(result):
    # get title
    try:
        title = result.find('h3', {'class' : 'r'}).text
    except:
        title = None
        warnings.warn('Was not able to get title for this article.')

    # get link to article
    try:
        link = result.find('a')['href'].split("/url?q=")[-1]
    except:
        link = None
        warnings.warn('Was not able to get link for article "{}". Returning None instead.'.format(title))

    # get article short description
    try:
        desc = result.find('span', {'class' : 'st'}).text
    except:
        desc = None
        warnings.warn('Was not able to get short description for article "{}". Returning None instead.'.format(title))

    # package article properties in a dictionary and return
    search_result = {
        'title': title,
        'link': link,
        'desc': desc,
    }
    return search_result


# Return a list of dictionaries containing news articles
# elements (title, link, desc, thumbnail) for a given search query
def get_search_items(query, ignore_warnings=False):
    if ignore_warnings:
        warnings.filterwarnings("ignore", category=UserWarning)
    soup = get_search_soup(query)
    items = soup.find_all('div', {'class' : 'g'})
    return [parse_search(a) for a in items]


if __name__ == "__main__":
    query = "Mining Gold Nolan Creek"
    print(get_search_items(query))