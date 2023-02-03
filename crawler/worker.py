from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier

        # temporary
        self.fingerprints = dict()

        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):

        max_runs = 10
        current_runs = 0
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                current_runs+=1
                if(current_runs > max_runs):
                    break
                else:
                    continue
            elif tbd_url == 'wait':
                self.logger.info("No open domains, waiting crawler.")
                time.sleep(self.config.time_delay)
                continue
            
            current_runs = 0

            time.sleep(self.config.time_delay)

            self.logger.info(f'Trying to download {tbd_url}')
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            
            if not resp.error:
                scraped_urls = scraper.scraper(tbd_url, resp, self.fingerprints)
                for scraped_url in scraped_urls:
                    self.frontier.add_url(scraped_url)

            self.frontier.mark_url_complete(tbd_url)
            #time.sleep(self.config.time_delay)
        
        print('----ending worker----')
