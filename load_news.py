import random
import time

import src.database_operations as dbo
import src.news_scraper as news


class NewsLoader():

    def __init__(self):
        self.conn = dbo.db_connect()


    def get_properties(self):
        query = "SELECT * FROM mines"
        resultset = dbo.select_query(self.conn, query, data=False, cols=True)
        return resultset


    def load_news(self):
        properties = self.get_properties()
        # print (properties[0:10])
        for prop in properties[0:10]:
            keywords = ['mine', prop['mine_name'], 'gold']
            query = " ".join(keywords)
            print (query)
            results = news.get_news_items(query)
            if results:
                print (results)

loader = NewsLoader()
loader.load_news()
