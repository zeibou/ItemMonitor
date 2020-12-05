import configuration as cfg
import urllib3

class Scraper:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.data = b""

    def refresh(self, url):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;Win64; x64)'}
        r = self.http.request('GET', url, headers=header)
        if r.status == 200:
            self.data = r.data
        else:
            print("Error when loading the page")
            print(r.data)

    def count_word(self, word, verbose=True):
        source = self.data.decode('utf8')
        l = source.lower()
        word = word.lower()
        c = l.count(word)
        if verbose:
            print(word + "  " + str(c))

        return c


if __name__ == "__main__":
    c = cfg.get_configuration()
    s = Scraper()
    s.refresh(c.scraper.url)
    s.count_word("out of stock")
    s.count_word("sold out")
    s.count_word(c.scraper.grep)
