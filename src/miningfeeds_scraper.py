"""Provides a scraper for mining company news results"""
from bs4 import BeautifulSoup
import requests
import re
import datetime
import time


# Get soup object for a given url
def get_soup(url, filetype="lxml"):
    return BeautifulSoup(requests.get(url).text, filetype)

# Clean unicode and convert to ascii
def clean_unicode(x):
    return re.sub(r'[^\x00-\x7F]+', '', x).encode('ascii', 'ignore')


# Clean date string
def clean_date_string(date_str):
    # remove non-asci characters
    clean_string = clean_unicode(date_str)

    # convert string to datetime format
    if "min" in clean_string:
        mins = int(re.findall(r'\d+', clean_string)[0])
        date_obj = datetime.datetime.now() - datetime.timedelta(minutes=mins)
    elif "hour" in clean_string:
        hrs = int(re.findall(r'\d+', clean_string)[0])
        date_obj = datetime.datetime.now() - datetime.timedelta(hours=hrs)
    else:
        date_obj = datetime.datetime.strptime(clean_string, "%b %d, %Y")
    return date_obj


def get_miner(row):
    row = row.find_all('td')

    # get name
    try:
        name = clean_unicode(row[1].text)
    except:
        name = None

    # get ticker
    try:
        ticker = clean_unicode(row[2].text)
    except:
        ticker = None

    # get url
    try:
        url = "https://www.google.ca/finance/company_news?q={}".format(ticker)
    except:
        url = None

    # get market cap
    try:
        market_cap = clean_unicode(row[11].text)
        market_cap = float(market_cap.replace(',', ''))  # convert string to float
    except:
        market_cap = None

    # wrap mining company data in a dictionary and return result
    miner = {
        'name': name,
        'url': url,
        'ticker': ticker,
        'market_cap': market_cap
    }
    return miner


def get_miners_list(max_miners=4):
    url = "http://www.miningfeeds.com/gold-mining-report-all-countries"
    soup = get_soup(url)
    table = soup.find('table', {'id': 'sort1'})
    body = table.findChild('tbody')
    rows = body.find_all('tr')
    miners = []
    for i, row in enumerate(rows):
        if i >= max_miners:
            break
        miners.append(get_miner(row))
    return miners


def parse_news_item(article):
    byline = article.find('div', {'class': 'byline'})

    # get title
    try:
        title = clean_unicode(article.find('span', {'class': 'name'}).text)
    except:
        title = None

    # get link
    try:
        link = article.find('a')['href']
    except:
        link = None

    # get source
    try:
        source = clean_unicode(byline.find('span', {'class': 'src'}).text)
    except:
        source = None

    # get date
    try:
        date = clean_date_string(byline.find('span', {'class': 'date'}).text)
    except:
        date = None

    # get desc
    try:
        desc = clean_unicode(article.find('div', {'class': 'g-c'}).text)
    except:
        desc = None

    # wrap result in a dictionary and return
    result = {
        'title': title,
        'link': link,
        'source': source,
        'desc': desc,
        'date': date
    }
    return result


def get_news(miner, max_items=4):
    url = miner["url"]
    print url
    soup = get_soup(url)
    news_pane = soup.find('div', {'id': 'news-main'})
    articles = news_pane.find_all('div', {'class': 'news'})
    news_list = []
    for i, a in enumerate(articles):
        if i >= max_items:
            break
        news_list.append(parse_news_item(a))
    return news_list


def get_miners_news(miners_list, max_items=4):
    news = []
    for miner in miners_list:
        try:
            news_list = get_news(miner, max_items=max_items)
            news += news_list
        except:
            print "Unable to get news for miner {}".format(miner["name"])
        time.sleep(2)
    return news


if __name__ == "__main__":
    miners = get_miners_list()
    news = get_miners_news(miners)