import src.database_operations as dbo
import src.miningfeeds_scraper as feed


class MinerNewsLoader():

    def __init__(self):
        self.conn = dbo.db_connect()

    def insert_miner(self, miner):
        data = [(miner["name"], miner["url"], miner["ticker"], miner["market_cap"])]
        query = "INSERT INTO companies VALUES (%s, %s, %s, %s)"
        dbo.execute_query(self.conn, query, data, multiple=True)
        return

    def insert_miner_news(self, article):
        data = [(article["link"], article["title"], article["ticker"],
                article["source"], article["desc"], article["date"])]

        try:
            query = "INSERT INTO company_news VALUES (%s, %s, %s, %s, %s, %s)"
        except:
            print("Issue inserting data:")
            print(data)

        dbo.execute_query(self.conn, query, data, multiple=True)
        return

    def load_miner_news(self):
        miners_list = feed.get_miners_list(max_miners=30)
        news_list = feed.get_miners_news(miners_list, max_items=20)

        for miner in miners_list:
            self.insert_miner(miner)

        for news in news_list:
            self.insert_miner_news(news)

if __name__ == "__main__":
    loader = MinerNewsLoader()
    loader.load_miner_news()
