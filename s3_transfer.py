#csv 헤더 설정하기
#지난날 기사들 구해서 저장해두기
import boto3
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import nltk
import time
import csv
import io
nltk.download('punkt')

s3 = boto3.resource('s3')
bucket_name = 'newkeybucket'  # S3 버킷 이름
object_name = 'news.csv'  # S3에 업로드될 CSV 파일 이름
newsId=0

def fetch_top_news():
    site = 'https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko'
    op = urlopen(site)
    rd = op.read()
    op.close()
    sp_page = soup(rd, 'xml')
    news_list = sp_page.find_all('item')

    while True:
        display_news(news_list,20)
        time.sleep(4000000) #반나절

def display_news(list_of_news, news_quantity):
    c = 0
    dataList=[]
    global newsId
    for news in list_of_news:
        newsId += 1
        c += 1
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            print(e)

        data=[newsId,news.title.text,news_data.text,news.pubDate.text]
        dataList.append(data)

        if c >= news_quantity:
            # CSV 파일 가져오기
            csv_object = s3.Object(bucket_name, object_name)
            csv_content = csv_object.get()['Body'].read().decode('utf-8')

            # CSV 파일 수정하기
            output = io.StringIO()
            writer = csv.writer(output)
            for row in dataList:
                writer.writerow(row)

            # 수정된 CSV 파일 가져오기
            csv_content += output.getvalue()

            # 수정된 CSV 파일 S3에 업로드
            csv_object.put(Body=csv_content)

            break

fetch_top_news()

