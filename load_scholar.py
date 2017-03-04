import random
import time

import src.database_operations as dbo
import src.scholar_scraper as scholar


class ScholarLoader():

    def __init__(self):
        self.conn = dbo.db_connect()


## join to google_news, see if it's already been scraped
    def get_properties(self):
        query = "SELECT * FROM mines"
        resultset = dbo.select_query(self.conn, query, data=False, cols=True)
        return resultset

    def historize_results(self, prop, results):
        data = [(prop['mine_id'], prop['mine_name'], r['link'],
            r['title'], r['citedby'], r['author']) for r in results]
        query = "INSERT INTO google_scholar VALUES (%s, %s, %s, %s, %s, %s)"
        dbo.execute_query(self.conn, query, data=True, multiple=True)
        return

    def load_scholars(self):
        properties = self.get_properties()
        # print (properties[0:10])
        for prop in properties[0:10]:
            keywords = ['mine', prop['mine_name'], 'gold']
            query = " ".join(keywords)
            results = scholar.get_scholar_items(query, 2010, 2017, 10)
            if results:
                print (results)
                # self.historize_results(prop, results)

            time.sleep(random.randint(2, 4))

loader = ScholarLoader()
loader.load_scholars()
