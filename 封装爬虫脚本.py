from time import sleep, process_time_ns

from DrissionPage import Chromium
from DrissionPage import ChromiumPage
from DrissionPage.common import  Actions
import time
import csv
from spider import JDSpider
import pandas as pd
from drop_empty import drop
import os
base_path = r"D:\Deskop\Code\Python_code\Data"


url_list={"iPhone 16 Pro Max":"https://item.jd.com/100118874245.html","一加 Ace 5":"https://item.jd.com/100132909701.html","vivo iQOO Neo10":"https://item.jd.com/100129509823.html"}
# for i in url_list:
#     spider=JDSpider(csv_filename=r"D:\Deskop\Code\Python_code\Data\+".csv",url=url_list[i])
#     spider.crawl_comments(17,"好评")
#     time.sleep(10)
#     spider.crawl_comments(18,"中评")
#     time.sleep(10)
#     spider.crawl_comments(19,"差评")

# spider=JDSpider(csv_filename=r"D:\Deskop\Code\Python_code\Data\iPhone 16 Pro Max"+".csv",url=url_list["iPhone 16 Pro Max"])
# spider.crawl_comments(17,"好评")
# time.sleep(10)
# spider.crawl_comments(18,"中评")
# time.sleep(10)
# spider.crawl_comments(19,"差评")


for i in url_list:
    csv_filename=os.path.join(base_path,i+".csv")
    drop(csv_filename)