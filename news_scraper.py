"""Provides a scraper for Google news articles"""

from bs4 import BeautifulSoup
import requests
import warnings


# Get soup object for a given url
def get_soup(url, filetype="lxml"):
    return BeautifulSoup(requests.get(url).text, filetype)


# Fetches google news search page for a given query and returns as a soup object
def get_news_soup(query):
    url = "https://news.google.com/news/section?q={}".format(query)
    return get_soup(url)


# Parses an article soup element and returns the news article
# elements (title, thumbnail, link, description) as a dictionary
def parse_article(article):
    # get title
    try:
        title = article.find('span', {'class': 'titletext'}).text
    except:
        title = None
        warnings.warn('Was not able to get title for this article.')

    # get thumbnail link
    try:
        # try getting 'src' element
        thumb = article.find('img', {'class': 'esc-thumbnail-image'})['src']
    except:
        # if fails, try getting 'imgsrc' element
        try:
            thumb = article.find('img', {'class': 'esc-thumbnail-image'})['imgsrc']
        # if all fails, return None
        except:
            thumb = None
            warnings.warn(
                'Was not able to get thumbnail address for article "{}". Returning None instead.'.format(title))

    # get link to article
    try:
        link = article.find('a', {'class': 'article'})['href']
    except:
        link = None
        warnings.warn('Was not able to get link for article "{}". Returning None instead.'.format(title))

    # get article short description
    try:
        desc = article.find('div', {'class': 'esc-lead-snippet-wrapper'}).text
    except:
        desc = None
        warnings.warn('Was not able to get short description for article "{}". Returning None instead.'.format(title))

    # package article properties in a dictionary and return
    article = {
        'title': title,
        'link': link,
        'desc': desc,
        'thumbnail': thumb
    }
    return article


# Return a list of dictionaries containing news articles
# elements (title, link, desc, thumbnail) for a given search query
def get_news_items(query, ignore_warnings=False):
    if ignore_warnings:
        warnings.filterwarnings("ignore", category=UserWarning)
    soup = get_news_soup(query)
    articles = soup.find_all('table', {'class': 'esc-layout-table'})
    return [parse_article(a) for a in articles]


if __name__ == "__main__":
    query = "Gold Miners"
    print get_news_items(query)