import requests as req
from DrissionPage.common import Settings
from DrissionPage import Chromium
from DrissionPage import ChromiumPage
from DrissionPage.common import  Actions
import time
import csv

f=open('差评.csv',mode='w',encoding='utf-8')
write=csv.DictWriter(f,fieldnames=[ "评分","评论内容"])
dp = ChromiumPage()
ac=Actions(dp)
#访问目标网站
dp.get('https://item.jd.com/100157830530.html')
#睡眠
time.sleep(5)
#监听数据
dp.listen.start('client.action')
#点击全部评论
dp.ele('css:.all-btn .arrow').click()
dp.ele('xpath://*[@id="rateList"]/div/div[2]/div/div[18]/span[1]').click()
for page in range(1,19):

    #等待加载
    wait=dp.listen.wait()
    #获取响应数据
    json_data=wait.response.body
    comment_list=json_data['result']['floors'][2]['data']
    for comment in comment_list:
        try:
             Get_data={
                 "评分":comment['commentInfo']['commentScore'],
                 "评论内容":comment['commentInfo']['commentData']
             }
             print(Get_data)
             write.writerow(Get_data)
        except:
            pass
    #定位评价窗口位置
    div=dp.ele('css:div._rateListContainer_1ygkr_45')
    div.scroll.to_bottom()


