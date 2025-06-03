from time import sleep

from DrissionPage import Chromium
from DrissionPage import ChromiumPage
from DrissionPage.common import  Actions
import time
import csv
from spider import JDSpider
import pandas as pd
from drop_empty import drop

spider=JDSpider(csv_filename="IPhone 16 Pro Max.csv",url="https://item.jd.com/100118874245.html")

drop("IPhone 16 Pro Max.csv")