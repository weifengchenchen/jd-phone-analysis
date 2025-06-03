from time import sleep

from DrissionPage import Chromium
from DrissionPage import ChromiumPage
from DrissionPage.common import  Actions
import time
import csv
from spider import JDSpider
import pandas as pd
from drop_empty import drop



url_list={}
for i in url_list:
    spider=JDSpider(csv_filename=i,url=url_list[i])
    spider.crawl_comments(17,"好评")
    time.sleep(10)
    spider.crawl_comments(18,"中评")
    time.sleep(10)
    spider.crawl_comments(19,"差评")

#
# drop("IPhone 16 Pro Max.csv")