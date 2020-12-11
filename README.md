# ItemMonitor
simple scraper to check when an sold out item is finally available  
Does not work with Amazon (requests a captcha eventually), but works fine with Newegg, Best Buy, and a few others.

## Setup
To set up, you can use your own config.json, based on a copy of config-default.json.  
Each item is an url to scrape, and triggers are based on regex parsing, which every one says you shouldn't do, but I did, and it's working fine, but still, do it at your own risk.  
<i>sold_out_regex</i> is the regex that, if it doesn't match, means the item is available => triggers a notification  
<i>sold_out_regex</i> is a regex to capture the price, and only notify tou if it's below your threshold  

Example of item configuration:
~~~     
      {
        "name": "Newegg - 5600X",
        "url": "https://www.newegg.com/amd-ryzen-5-5600x/p/N82E16819113666",
        "sold_out_regex": "CURRENTLY SOLD OUT",
        "price_regex": "<span class=\"list_price\">?([0-9.]*)</span>",
        "max_price": 300,
        "frequency_seconds": 2
      },
~~~
