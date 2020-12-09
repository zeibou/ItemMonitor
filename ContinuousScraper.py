import time
import datetime as dt
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

items = [ItemChecker(i) for i in sc.items if i.enabled]
t = time.time()
n = 0

while True:
    if time.time() - t > 60 * 10:
        print(dt.datetime.now(), f"  - checked {n} times")
        t = time.time()
        n = 0

    for i in items:
        i.poll()

    n += 1
    time.sleep(3)
