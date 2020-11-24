from Scraper import NeweggScraper
import time
import datetime as dt
import playsound
import Notifier
import configuration as cfg

s = NeweggScraper()
t = 0
n = 0
sold_out = True

nc = cfg.get_configuration().notifier
sc = cfg.get_configuration().scraper
playsound.playsound(nc.sound)
Notifier.send_email(sc.item, "Test notifications", nc)

while True:
    if time.time() - t > 60 * 10:
        print(dt.datetime.now(), f"  - checked {n} times")
        t = time.time()
        n = 0
    s.load(sc.url)
    time.sleep(1)
    c = s.count_word(sc.grep, False)
    n += 1
    if c != 1:
        print(dt.datetime.now())
        s.count_word(sc.grep)
        print("AVAILABLE !?!")
        if sold_out:
            playsound.playsound(nc.sound)
            Notifier.send_email(sc.item, "Item available", nc)
            sold_out = False
    else:
        if not sold_out:
            Notifier.send_email(sc.item, "Item sold out", nc)
            sold_out = True

    time.sleep(1)
