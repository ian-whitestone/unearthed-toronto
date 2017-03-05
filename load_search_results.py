import random
import time

import src.database_operations as dbo
import src.search_scraper as feed


class SearchLoader():

    def __init__(self):
        self.conn = dbo.db_connect()


## join to google_news, see if it's already been scraped
    def get_properties(self):
        query = """
            SELECT a.*, COALESCE(scraped, 0) as scraped
            FROM mines a
            LEFT JOIN
            (
                SELECT mine_id, 1 as scraped
                FROM google_news
            ) AS b
            ON a.mine_id = b.mine_id
            WHERE COALESCE(scraped,0)=0
        """
        resultset = dbo.select_query(self.conn, query, data=False, cols=True)
        return resultset

    def historize_results(self, prop, results):
        pass

    def load_search_results(self):
        pass

if __name__ == "__main__":
    loader = SearchLoader()
    loader.load_search_results()
