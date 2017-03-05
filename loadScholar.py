import random
import time

import src.database_operations as dbo
import src.scholar_scraper as scholar


class ScholarLoader():

    def __init__(self):
        self.conn = dbo.db_connect()



    def get_properties(self):
        query = """
            SELECT a.*, COALESCE(scraped, 0) as scraped
            FROM mines a
            LEFT JOIN
            (
                SELECT mine_id, 1 as scraped
                FROM google_scholar
            ) AS b
            ON a.mine_id = b.mine_id
            WHERE COALESCE(scraped,0)=0
        """
        resultset = dbo.select_query(self.conn, query, data=False, cols=True)
        return resultset

    def historize_results(self, prop, results):
        data = [(prop['mine_id'], prop['mine_name'], r['link'],
            r['title'], r['citedby'], r['author']) for r in results]
        query = "INSERT INTO google_scholar VALUES (%s, %s, %s, %s, %s, %s)"
        dbo.execute_query(self.conn, query, data, multiple=True)
        return

    def load_scholars(self):
        properties = self.get_properties()
        for prop in properties:
            print ('Searching scholar articles for property %s' % prop['mine_name'])
            keywords = ['mine', prop['mine_name'], 'gold']
            query = " ".join(keywords)
            try:
                results = scholar.get_scholar_items(query, 2010, 2017, 10)
            except Exception as e:
                print ('Error: %s' % str(e))
            if results:
                self.historize_results(prop, results)

            time.sleep(random.randint(1, 3))

loader = ScholarLoader()
loader.load_scholars()
