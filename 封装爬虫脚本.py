from time import sleep

from DrissionPage import Chromium
from DrissionPage import ChromiumPage
from DrissionPage.common import  Actions
import time
import csv
from spider import JDSpider
import pandas as pd
from drop_empty import drop



url_list={"iPhone 16 Pro Max":"https://item.jd.com/100118874245.html","一加 Ace 5":"https://item.jd.com/100132909701.html"," vivo iQOO Neo10":"https://item.jd.com/100129509823.html"}
# for i in url_list:
#     spider=JDSpider(csv_filename=i+".csv",url=url_list[i])
#     spider.crawl_comments(17,"好评")
#     time.sleep(10)
#     spider.crawl_comments(18,"中评")
#     time.sleep(10)
#     spider.crawl_comments(19,"差评")

spider=JDSpider(csv_filename=r"C:\\Users\\16075\\Desktop\\Code\\Python_code\\Data\\Phone 16 Pro Max"+".csv",url=url_list["iPhone 16 Pro Max"])
spider.crawl_comments(17,"好评")
time.sleep(10)
spider.crawl_comments(18,"中评")
time.sleep(10)
spider.crawl_comments(19,"差评")
for i in url_list:
    drop(i+".csv")