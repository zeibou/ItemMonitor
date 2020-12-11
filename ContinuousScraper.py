import time
import datetime as dt
import heapq
import playsound
import Notifier
import configuration as cfg
from configuration import ScraperItem
from Scraper import Scraper


class ItemChecker:
    def __init__(self, item: ScraperItem):
        self.scraper = Scraper()
        self.item = item
        self.sold_out = True
        self.triggered = False

    def find_price(self):
        price_matched = self.scraper.find(self.item.price_regex)
        if price_matched:
            return float(price_matched[0])

    def poll(self):
        self.scraper.refresh(self.item.url)
        if self.scraper.find(self.item.failed_load_regex):
            print(f"failed loading {self.item.name}")
            return
        sold_out_match = self.scraper.find(self.item.sold_out_regex)
        if not sold_out_match:
            price = self.find_price()
            if price and price > self.item.max_price:
                print(f"Available but price too high: {price}")
            elif self.sold_out:
                now = str(dt.datetime.now())
                print(f"{self.item.name} AVAILABLE at {now} for {price}: {self.item.url}")
                if not self.triggered:
                    playsound.playsound(nc.sound)
                    Notifier.send_email(self.item.name, "Item available", nc)
                    self.scraper.save(nc.output_path, f"available_{self.item.name}_{now}.html")
                self.sold_out = False
        else:
            if not self.sold_out:
                now = str(dt.datetime.now())
                print(f"{self.item.name} Sold out again at {now}")
                if not self.triggered:
                    Notifier.send_email(self.item.name, "Item sold out", nc)
                    self.scraper.save(nc.output_path, f"soldout_{self.item.name}_{now}.html")
                self.sold_out = True
                self.triggered = True


nc = cfg.get_configuration().notifier
sc = cfg.get_configuration().scraper
# only needed when running the first time
# playsound.playsound(nc.sound)
# Notifier.send_email("scraper test", "Test notifications", nc)

items = [(0, k, ItemChecker(i)) for k, i in enumerate(sc.items) if i.enabled]
t = time.time()
n = 0
heapq.heapify(items)

while True:
    if time.time() - t > 60 * 10:
        print(dt.datetime.now(), f"  - checked {n} urls in the past 10 minutes")
        t = time.time()
        n = 0

    it, k, ii = heapq.heappop(items)
    while it > time.time():
        time.sleep(0.25)
    ii.poll()
    heapq.heappush(items, (time.time() + ii.item.frequency_seconds, k, ii))
    n += 1
