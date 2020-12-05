import os
import json
import logging

CONFIG_FILE_DEFAULT = "./config-default.json"
CONFIG_FILE_PERSO = "./config.json"


class NotifierConfig:
    def __init__(self, dico):
        self.sender = dico.get("sender")
        self.password = dico.get("password")
        self.receivers = dico.get("receivers")
        self.sound = dico.get("sound")
        self.output_path = dico.get("output_path")


class ScraperConfig:
    def __init__(self, dico):
        self.items = [ScraperItem(i) for i in dico.get("items")]


class ScraperItem:
    def __init__(self, dico):
        self.enabled = dico.get("enabled", True)
        self.name = dico.get("name")
        self.url = dico.get("url")
        self.sold_out_regex = dico.get("sold_out_regex")
        self.price_regex = dico.get("price_regex")
        self.max_price = dico.get("max_price")
        self.failed_load_regex = dico.get("failed_load_regex")



class Configuration:
    # make it a singleton
    _instance = None
    _loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance

    notifier = None
    scraper = None

    def load(self, config_file_path, override_only=False):
        if not os.path.exists(config_file_path):
            logging.warning(f"{config_file_path} does not exist")
            return

        with open(config_file_path, 'r') as f:
            contents = json.load(f)
            for key in contents:
                if override_only and key not in self.__dict__:
                    logging.warning(f"Ignoring '{key}' because it is not an expected configuration item")
                else:
                    if key == "notifier":
                        self.notifier = NotifierConfig(contents[key])
                    elif key == "scraper":
                        self.scraper = ScraperConfig(contents[key])
                    else:
                        self.__dict__[key] = contents[key]
        self._loaded = True


def get_configuration():
    config = Configuration()
    if not config._loaded:
        config.load(CONFIG_FILE_DEFAULT)
        config.load(CONFIG_FILE_PERSO, override_only=True)
    return config


if __name__ == '__main__':
    configuration = get_configuration()
    print(configuration.notifier.receivers)
    print(configuration.scraper.url)

