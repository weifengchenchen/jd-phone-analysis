import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
import re
import jieba
from collections import Counter
import matplotlib as mpl

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文支持
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 打印当前使用的字体信息以便调试
print(f"当前使用的字体: {plt.rcParams['font.sans-serif']}")
print(f"当前字体路径: {mpl.matplotlib_fname()}")

# 获取所有CSV文件的路径
file_paths = glob.glob(r'D:\Deskop\Code\Python_code\Data\*.csv')

print(f"Found {len(file_paths)} CSV files:")
for file_path in file_paths:
    print(file_path)

# 初始化数据存储
data_list = []

# 更新品牌映射表（与标准化后的名称完全匹配）
brand_model_map = {
    'huawei_pura_70_pro_': {'品牌': '华为', '型号': 'Pura 70 Pro+'},
    'iphone_16_pro_max': {'品牌': '苹果', '型号': '16 Pro Max'},
    'redmik80': {'品牌': '红米', '型号': 'K80'},
    'vivo_iqoo_neo10': {'品牌': 'vivo', '型号': 'iQOO Neo10'},
    '一加_ace_5': {'品牌': '一加', '型号': 'Ace 5'}
}

def standardize_filename(filename):
    # 去除文件扩展名
    filename = os.path.splitext(filename)[0]
    # 替换所有非字母数字字符为下划线
    standardized_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', filename)
    # 转换为小写（保留中文）
    standardized_name = standardized_name.lower()
    return standardized_name

# 读取每个CSV文件
for file_path in file_paths:
    base_name = os.path.basename(file_path)
    file_key = os.path.splitext(base_name)[0]
    standardized_file_key = standardize_filename(file_key)

    print(f"Original: {file_key}, Standardized: {standardized_file_key}")

    if standardized_file_key in brand_model_map:
        brand_info = brand_model_map[standardized_file_key]

        try:
            # 尝试多种编码方式
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(file_path, encoding='gbk')
                except:
                    df = pd.read_csv(file_path, encoding='latin1')

            # 检查必要列是否存在
            required_columns = {'评分', '评论内容'}
            if not required_columns.issubset(df.columns):
                print(f"警告: 文件 {file_path} 缺少必要列，实际列: {df.columns.tolist()}")
                continue

            df['品牌'] = brand_info['品牌']
            df['型号'] = brand_info['型号']
            data_list.append(df)
            print(f"成功处理文件: {file_path}")

        except Exception as e:
            print(f"处理文件 {file_path} 失败: {str(e)}")
    else:
        print(f"未匹配: {standardized_file_key}")

# 合并数据
if data_list:
    data = pd.concat(data_list, ignore_index=True)
    print(f"\n合并后数据量: {len(data)} 条")
    print(data.head())
else:
    raise ValueError("没有有效数据可供分析")

# 中文文本处理
nltk.download('stopwords', quiet=True)
chinese_stopwords = set(stopwords.words('chinese'))
custom_stopwords = {"手机", "使用", "感觉", "购买", "东西", "产品", "就是", "还是", "真的", "非常", "比较", "有点"}
chinese_stopwords.update(custom_stopwords)

def clean_chinese_text(text):
    if pd.isna(text) or not isinstance(text, str):
        return ""
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
    text = re.sub(r'\d+', '', text)
    words = jieba.cut(text)
    words = [word for word in words if word not in chinese_stopwords and len(word) > 1]
    return ' '.join(words)

# 应用清洗
print("\n清洗评论内容...")
data['cleaned_review'] = data['评论内容'].apply(clean_chinese_text)
print(data['cleaned_review'].head())

# 情感分析
data['sentiment'] = data['评分'].apply(
    lambda x: '正面' if x >= 4 else ('中性' if x == 3 else '负面')
)

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    data['cleaned_review'], data['sentiment'], test_size=0.2, random_state=42
)

# 特征提取和模型训练
vectorizer = CountVectorizer(max_features=5000, token_pattern=r'\b\w+\b')
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_counts, y_train)

# 评估
y_pred = model.predict(X_test_counts)
print(f"\n准确率: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

# 可视化输出目录
output_folder = r'D:\Deskop\Code\Python_code\photo'
os.makedirs(output_folder, exist_ok=True)

# ==================== 1. 平均评分饼图 ====================
def plot_average_rating_pie(data):
    avg_rating = data.groupby('品牌')['评分'].mean()
    plt.figure(figsize=(8, 8))
    
    # 绘制饼图
    plt.pie(avg_rating, labels=avg_rating.index, autopct='%1.1f%%', startangle=140)
    plt.title('Average Rating Distribution by Brand', fontsize=24)
    
    # 保存饼图
    plt.savefig(os.path.join(output_folder, 'average_rating_distribution_pie_chart.png'), dpi=300, bbox_inches='tight')
    plt.show()

# ==================== 2. 所有品牌高频词汇柱形图与饼图 ====================
def plot_top_words_pie(text, title, top_n=20):
    words = text.split()
    word_counts = Counter(words)
    top_words = word_counts.most_common(top_n)

    # 绘制饼图
    plt.figure(figsize=(8, 8))
    plt.pie([count for word, count in top_words], labels=[word for word, count in top_words], autopct='%1.1f%%', startangle=140)
    plt.title(f'Top Words in {title} (Top {top_n})', fontsize=24)
    
    # 保存饼图
    plt.savefig(os.path.join(output_folder, f'top_words_in_{title}_pie_chart.png'), dpi=300, bbox_inches='tight')
    plt.show()

    # 绘制柱形图
    plt.figure(figsize=(16, 10))
    sns.barplot(x=[count for word, count in top_words], y=[word for word, count in top_words], palette='viridis')
    plt.title(f'Top Words in {title} (Top {top_n})', fontsize=24)
    plt.xlabel('Frequency', fontsize=20)
    plt.ylabel('Words', fontsize=20)
    
    # 保存柱形图
    plt.savefig(os.path.join(output_folder, f'top_words_in_{title}_bar_chart.png'), dpi=300, bbox_inches='tight')
    plt.show()

# ==================== 3. 设置背景图片 ====================
def set_background_image(image_path):
    # 读取背景图片
    img = plt.imread(image_path)
    plt.imshow(img, aspect='auto', extent=[0, 1, 0, 1], zorder=-1)

# 使用示例
background_image_path = r'D:\Deskop\可视化\static\images\background.jpg'  # 替换为你的背景图片路径
set_background_image(background_image_path)

# 绘制平均评分饼图
plot_average_rating_pie(data)

# 整体高频词
all_reviews = ' '.join(data['cleaned_review'].dropna())
plot_top_words_pie(all_reviews, "All Brands")

# ==================== 4. 情感分布对比 ====================
plt.figure(figsize=(18, 12))
ax = sns.countplot(x='品牌', hue='sentiment', data=data,
                   palette={'正面': '#2ca02c', '中性': '#ff7f0e', '负面': '#d62728'})
plt.title('各品牌情感分布对比', fontsize=24)
plt.xlabel('品牌', fontsize=20)
plt.ylabel('评论数量', fontsize=20)
plt.legend(title='情感', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)

# 标注柱状图上的数字
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height}',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                xytext=(0, 5),
                textcoords='offset points',
                fontsize=14)

# 设置刻度字体
plt.xticks()
plt.yticks()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(os.path.join(output_folder, '各品牌情感分布对比.png'), dpi=300, bbox_inches='tight')
plt.show()

# ==================== 4. 评分分布 ====================
# 使用更好的调色板
palette = sns.color_palette("husl", len(data['品牌'].unique()))

# 创建分面网格
g = sns.FacetGrid(data, col='品牌', col_wrap=3, height=5, aspect=1.2)
g.map_dataframe(sns.histplot, x='评分', bins=5, kde=True, color=palette[0], alpha=0.7)

# 添加平均线
for ax, brand in zip(g.axes.flat, data['品牌'].unique()):
    avg = data[data['品牌'] == brand]['评分'].mean()
    ax.axvline(avg, color='red', linestyle='--', linewidth=2)
    ax.text(avg + 0.1, ax.get_ylim()[1] * 0.9, f'平均: {avg:.2f}',
            color='red', fontsize=12)

# 设置标题和标签
g.set_titles('{col_name}', size=16, weight='bold')
g.set_axis_labels('评分', '评论数量', fontsize=14)
g.fig.suptitle('各品牌评分分布', y=1.05, fontsize=24, weight='bold')

# 设置刻度标签
for ax in g.axes.flat:
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.tick_params(axis='both', labelsize=12)

# 调整布局
plt.tight_layout()
plt.savefig(os.path.join(output_folder, '各品牌评分分布.png'), dpi=300, bbox_inches='tight')
plt.show()

print("所有分析及可视化已完成！结果已保存至:", output_folder)