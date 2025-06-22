<<<<<<< HEAD
# 京东手机数据爬取与分析大屏

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![DrissionPage](https://img.shields.io/badge/DrissionPage-%E2%9C%93-green)
![Pandas](https://img.shields.io/badge/Pandas-%F0%9F%93%8A-orange)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey)

一个基于 **DrissionPage** 的京东手机数据爬虫，结合数据清洗、情感分析和可视化大屏的完整项目()。

## 📌 项目概述

通过爬取京东手机商品数据（价格、评论、评分等），经数据清洗和分析后，使用 Flask 构建可视化仪表盘，展示：
- 品牌评分对比
- 用户情感分布
- 高频关键词分析

## 🛠️ 技术栈

| 模块          | 技术实现                                                                 |
|---------------|--------------------------------------------------------------------------|
| **爬虫**      | DrissionPage（无头浏览器模拟） + 反反爬策略（随机延迟、User-Agent轮换） |
| **数据处理**  | Pandas（数据清洗） + Jieba（中文分词） + NLTK（停用词过滤）             |
| **分析建模**  | Scikit-learn（朴素贝叶斯情感分类） + 文本词频统计                       |
| **可视化**    | Matplotlib/Seaborn（静态图表） + Flask（Web大屏）                       |
| **部署**      | 可本地运行  |


## 📂 项目结构
project/
├── crawler/ # 爬虫模块
│ ├──spider.py # 爬虫封装模块(该项目仅爬取了评分与评分内容,用户可根据自己的需求更改spider部分)
│ └── 封装爬虫脚本.py #demo
├── Data/ # 数据存储
│ ├── raw/ # 原始数据（CSV/JSON）
│ └── processed/ # 整合数据.py
├── analysis/ # 数据分析
│ ├── 数据分析.py #
├── visualization/ # 可视化
│ ├── app.py # Flask主程序
│ ├── templates/ # HTML模板
│ └── static/ # CSS/图片资源
└── README.md # 项目说明

# 1. 克隆项目
git clone https://github.com/weifengchenchen/jd-phone-analysis.git
cd jd-phone-analysis

# 2. 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# 3. 安装依赖
pip install -r requirements.txt

