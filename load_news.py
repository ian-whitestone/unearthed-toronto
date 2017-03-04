import random
import time

import src.database_operations as dbo
import src.news_scraper as news


class NewsLoader():

    def __init__(self):
        self.conn = dbo.db_connect()


## join to google_news, see if it's already been scraped
    def get_properties(self):
        query = "SELECT * FROM mines"
        resultset = dbo.select_query(self.conn, query, data=False, cols=True)
        return resultset

    def historize_results(self, prop, results):
        data = [(prop['mine_id'], prop['mine_name'], r['link'],
            r['title'], r['desc'], r['date']) for r in results]
        query = "INSERT INTO google_news VALUES (%s, %s, %s, %s, %s, %s)"
        dbo.execute_query(self.conn, query, data=True, multiple=True)
        return

    def load_news(self):
        properties = self.get_properties()
        # print (properties[0:10])
        for prop in properties[0:10]:
            keywords = ['mine', prop['mine_name'], 'gold']
            query = " ".join(keywords)
            print (query)
            results = news.get_news_items(query)
            if results:
                self.historize_results(prop, results)

            time.sleep(random.randint(2, 4))

loader = NewsLoader()
loader.load_news()
