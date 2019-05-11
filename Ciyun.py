import random
import time
import requests
import jieba
import codecs
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
from scipy.misc import imread
from bs4 import BeautifulSoup
def getHtml(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        return r.text
    except:
        return ''
def getComment(html):
    soup = BeautifulSoup(html, 'html.parser')  #初始化
    comments_list = []
    comment_nodes = soup.select('.comment > p') #筛选元素，用到的方法是 soup.select()，返回类型是 list，这里通过类名class查找（带符号逗点.）,组合查询，空格连接
    for node in comment_nodes:
        comments_list.append(node.get_text().strip().replace("\n", "") + u'\n')    #replace('\n','')把换行符替换成空，
    return comments_list
def saveCommentText(fpath):
    pre_url ="https://movie.douban.com/subject/1291546/comments?"
    depth = 8
    with open(fpath, 'a', encoding='utf-8') as f:
        for i in range(depth):
            url = pre_url+'start=' + str(20 * i) + '&limit=20&sort=new_score&' +'status=P'  #翻页地址，每页20条
            html = getHtml(url)
            f.writelines(getComment(html))
            time.sleep(1 + float(random.randint(1, 20)) / 20)## 设置随机休眠防止IP被封，好像也没有必要 01：通过time.sleep()阻塞线程若干秒,2：通过type()函数获取数据的类,03：通过random.randint()方法生成指定返回区间内的一个随机数(闭区间),04：通过int()函数把字符串转化为整数
#首先是豆瓣，豆瓣自从去年 10 月份已经全面禁止爬取数据，仅仅放出 500 条数据，豆瓣封 IP，白天一分钟可以访问 40 次，晚上一分钟可以访问 60 次，超过限制次数就会封 IP。
def cutWords(fpath):
    text = ''
    with open(fpath,'r', encoding='utf-8') as fin:
        for line in fin.readlines():
              line = line.strip('\n')
              text += ' '.join(jieba.cut(line))  #将一行字符串，分割成一个个单词
              text += ' '
    with codecs.open('text.txt', 'a', encoding='utf-8') as f: #文件读尽量用第二种方法，一般不会出现编码的问题
        f.write(text)
def drawWordcloud():
    with codecs.open('text.txt',encoding='utf-8') as f:
        comment_text = f.read()
    color_mask = imread('D:\\Python\\Python36\\pic.jpg')
    Stopwords = [u'就是', u'电影', u'你们', u'这么', u'不过', u'但是',
                          u'除了', u'时候', u'已经', u'可以', u'只是', u'还是', u'只有', u'不要', u'觉得',u'，'u'。']
    #mask指定词云形状，默认为长方形，需要引用imread()函数
    cloud = WordCloud(font_path="simhei.ttf",
                      background_color='white',
                      max_words=200,
                      max_font_size=200,
                      min_font_size=4,
                      mask=color_mask,
                      stopwords=Stopwords)
    word_cloud = cloud.generate(comment_text)
    image_colors = ImageColorGenerator(color_mask)
    plt.imshow(cloud)
    plt.axis("off")
    plt.figure()
    plt.imshow(cloud.recolor(color_func=image_colors))
    plt.axis("off")
    plt.figure()
    plt.imshow(color_mask, cmap=plt.cm.gray)
    plt.axis("off")
    plt.show()
    word_cloud.to_file("comment_cloud.jpg")
def main():
    fpath = 'comment.txt'
    saveCommentText(fpath)
    cutWords(fpath)
    drawWordcloud()
main()
