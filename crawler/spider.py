from DrissionPage import ChromiumPage
import time
import csv


class JDSpider:
    def __init__(self, csv_filename, url):
        self.csv_filename = csv_filename
        self.url = url
        self.dp = ChromiumPage()

        # 初始化CSV文件
        with open(self.csv_filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["评分", "评论内容"])
            writer.writeheader()
    def crawl_comments(self, div_position, comment_type):
        print(f"开始爬取{comment_type}...")
        # 基本页面操作
        self.dp.get(self.url)
        time.sleep(5)
        self.dp.ele('css:.all-btn').click()
        self.dp.ele(f'xpath://*[@id="rateList"]/div/div[2]/div/div[{div_position}]/span[1]').click()
        # 监听数据
        self.dp.listen.start('client.action')
        for page in range(1, 102):
            print(f'正在采集{comment_type}第{page}页')

            wait = self.dp.listen.wait()
            json_data = wait.response.body
            try:
                Error=json_data['result']
            except KeyError:
                break
            comments = json_data['result']['floors'][2]['data']
            # 写入数据
            with open(self.csv_filename, 'a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["评分", "评论内容"])
                for comment in comments:
                    try:
                        writer.writerow({
                            "评分": comment['commentInfo']['commentScore'],
                            "评论内容": comment['commentInfo']['commentData']
                        })
                    except:
                        pass

            # 滚动加载
            self.dp.ele('css:div._rateListContainer_1ygkr_45').scroll.to_bottom()

        print(f"{comment_type}爬取完成")


