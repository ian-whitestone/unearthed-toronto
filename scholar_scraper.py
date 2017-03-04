"""
Wrapper for scholarly package to return news search
results in format consistent with news_scraper.py
"""
import scholarly


def get_scholar_items(query, year_low=2016, year_high=None, max_articles=5):
    url = "/scholar.google.ca/scholar?q={}&hl=en&as_ylo={}&as_yhi={}".format(query, year_high, year_low)
    search_query = scholarly.search_pubs_custom_url(url)

    # iterate through search query max_acticles
    articles = []
    for i, result in enumerate(search_query):
        # stop is max article count is met
        if i > max_articles:
            break
        articles.append(get_article(result))
    return articles


# parses article as dictionary from scholarly.Publication result
def get_article(result):
    # get title
    try:
        title = result.bib["title"]
    except:
        title = None

    # get author
    try:
        author = result.bib["author"]
    except:
        author = None

    # get link
    try:
        link = result.bib["url"]
    except:
        link = None

    # get abstract
    try:
        abstract = result.bib["abstract"]
    except:
        abstract = None

    # get cited by count
    try:
        citedby = result.citedby
    except:
        citedby = None

    # wrap result in a dictionary and return
    article = {
        'title': title,
        'author': author,
        'link': link,
        'desc': abstract,
        'citedby': citedby
    }
    return article


if __name__ == "__main__":
    query = 'Gold Mining'
    print get_scholar_items(query)
