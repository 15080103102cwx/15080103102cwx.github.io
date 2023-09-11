import jieba
import csv
import random
import math
import wordcloud
import matplotlib.pyplot as plt

def Restopwords():
    ''' 读取停用词函数'''
    with open("弹幕汇总.txt", 'r', encoding='utf-8') as f:
        stopwords = f.read().splitlines()  # 用splitlines()函数 将读取的每一行作为一个元素存入列表stopwords中
    return stopwords  # 返回停用词列表
def Comments_lines():
    '''读取数据集的函数'''
    with open("弹幕汇总.cvs", "r", encoding='utf-8') as f:
        reader = csv.reader(f)  # 使用reader()函数，将整个数据集每行作为一个元素，存入reader列表
        rows = [row[0] for row in reader]  # 对reader进行遍历，只取第一列弹幕作为元素
        rows = rows[0:5000]
    return rows  # 返回已每条弹幕作为元素的列表
def Word_frequ(rows, stopwords):
    '''这是一个统计词频的函数'''
    coms = []  # 这是一个承接所有词组的列表
    for row in rows:  # 对每条弹幕进行遍历
        com = jieba.lcut(row)  # 使用jieba库进行分词
        coms.extend(com)  # 将所有分出的词组加入coms列表
    counts = {}  # 这是一个统计词频的字典
    for word in coms:  # 对每个词进行遍历
        if len(word) == 1:  # 不使用单字作为一个词
            continue
        elif word in stopwords:  # 在停用词列表中的剔出
            continue
        else:
            counts[word] = counts.get(word, 0) + 1  # 如果该词在字典中存在，则值再加1，要是不存在就创建一个
    return counts

def get_danmaku_file(data):
    with open("弹幕排行.txt",mode='a+',encoding='utf-8') as f:
        for i in data:
            for a in i:
                f.write(str(a))
                f.write('\t')
            f.write('\n')
def Screen(counts):
    '''这是一个筛选词频的函数'''
    item = []
    for i in counts[:20]:
        # 如果词频小于20就将其保留
        item.append(i)
    counts1 = dict(item)
    return counts1

def Matrix(counts1, rows):
    '''这是一个根据弹幕生成向量矩阵的函数'''
    matrics = []
    n = len(counts1)
    items = list(counts1.keys())
    for row in rows:  # 对每条弹幕进行遍历
        words = jieba.lcut(row)  # 对一条弹幕进行分词
        if len(words) <= 7:  # 如果一条弹幕总词组数量小于7，则不计入矩阵
            pass
        else:
            # 找到对于单词对应的位置，在该位置设置标记
            lis = [0] * n
            for word in words:
                if word in items:
                    lis[items.index(word)] = 1
            matrics.append(lis)

    return matrics, n


def Distance(n, matrics):
    '''这是一个计算不同弹幕距离的函数'''
    sums = 0
    mole = 0
    # 随机找出矩阵中的两个向量
    for i in range(n):
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        sums = (matrics[x][i] - matrics[y][i]) ** 2 + sums
        mole = mole + matrics[x][i] * matrics[y][i]
    # 计算欧式距离
    distance_euc = math.sqrt(sums)
    sum1 = sum(matrics[x]);
    sum2 = sum(matrics[y])
    deno = math.sqrt(sum1 * sum2)
    # 计算余弦距离
    if deno == 0:
        distance_cos = 0
    else:
        distance_cos = mole / deno

    return distance_euc, distance_cos


def plot_Wc(counts1):
    '''这是将词频字典生成词云的函数'''
    # 主结构很像前端里面CSS的写法
    wc = wordcloud.WordCloud(  # 根据词频字典生成词云图
        max_words=100,  # 最多显示词数
        max_font_size=300,  # 字体最大值
        background_color="white",  # 设置背景为白色，默认为黑色
        width=1500,  # 设置图片的宽度
        height=960,  # 设置图片的高度
        margin=10,  # 设置图片的边缘
        font_path="msyh.ttc"
    )
    wc.generate_from_frequencies(counts1)  # 从字典生成词云
    wc.to_file("词云分析.png")
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像


def TF_IDF(counts1, rows):
    '''对TF_IDF进行构建'''
    n = len(counts1)
    m = len(rows)
    counts_IF = counts1
    for i in counts1:
        # 计算tf
        tf = counts1.get(i) / n
        count = 0
        for row in rows:
            words = jieba.lcut(row)
            if i in words:
                count = count + 1
        # 计算idf
        idf = math.log(m / count)
        # 两者求积得tf_idf
        tf_idf = tf * idf
        counts_IF[i] = tf_idf

    return counts_IF
def main():
    stopwords = Restopwords()  # 停用词列表
    rows = Comments_lines()  # 弹幕列表
    counts = Word_frequ(rows, stopwords)  # 词频列表
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    get_danmaku_file(sorted_counts)
    counts1 = Screen(sorted_counts)
    counts_IF = TF_IDF(counts1, rows)
    print(counts_IF)
    plot_Wc(counts1)

if __name__ == '__main__':
    main()