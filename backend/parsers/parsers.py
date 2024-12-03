import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crochet import setup, run_in_reactor
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal
from backend.core.models.scraped_data import ScrapedData

setup()

class ExampleSpider(scrapy.Spider):
    name = "example"

    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [str(url)]

    def parse(self, response):
        self.log(f"Visited: {response.url}")
        title = response.css('title::text').get()
        if title:
            self.save_to_db(response.url, title)
        else:
            self.log("No title found on the page")

    def save_to_db(self, url, title):
        db: Session = SessionLocal()
        try:
            scraped_data = ScrapedData(url=url, title=title)
            db.add(scraped_data)
            db.commit()
            self.log(f"Data saved to database: {url}, {title}")
        except Exception as e:
            self.log(f"Error saving to database: {e}")
            db.rollback()
        finally:
            db.close()

@run_in_reactor
def run_spider(url):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ExampleSpider, url=str(url))
    process.start()