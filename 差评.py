
from DrissionPage import Chromium
from DrissionPage import ChromiumPage
from DrissionPage.common import  Actions
import time
import csv



f=open('京东商家 iPhone 16 Pro Max.csv',mode='w',encoding='Ansi')
write=csv.DictWriter(f,fieldnames=[  "评分","评论内容"])
dp = ChromiumPage()
ac=Actions(dp)
#访问目标网站
dp.get('https://item.jd.com/100118874245.html')
#睡眠
time.sleep(5)
#监听数据
#点击全部评论
dp.ele('css:.all-btn .arrow').click()
dp.ele('xpath://*[@id="rateList"]/div/div[2]/div/div[17]/span[1]').click()
dp.listen.start('client.action')
for page in range(1,102):
    print(f'正在采集好评第{page}页')
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
             write.writerow(Get_data)
        except:
            pass
    #定位评价窗口位置
    div=dp.ele('css:div._rateListContainer_1ygkr_45')
    div.scroll.to_bottom()


