from selenium import webdriver
import configuration as cfg

DEFAULT_DRIVER_PATH = './chromedriver'


class NeweggScraper:
    def __init__(self, driver_path=DEFAULT_DRIVER_PATH):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options, executable_path=driver_path)

    def load(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def count_word(self, word, verbose=True):
        source = self.driver.page_source
        l = source.lower()
        word = word.lower()
        c = l.count(word)
        if verbose:
            print(word + "  " + str(c))

        return c


if __name__ == "__main__":
    c = cfg.get_configuration()
    s = NeweggScraper()
    s.load(c.scraper.url)
    s.count_word("out of stock")
    s.count_word("sold out")
    s.count_word(c.scraper.grep)
    s.close()
