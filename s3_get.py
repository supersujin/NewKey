#받은 news df 전처리 & 추천 알고리즘 짜기(채은&예슬이가 수정)
import boto3
from flask import Flask,request
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#다른 팀원들은 s3 접근 권한 없어 오류나므로 이 코드 주석 처리 후 news.csv파일 따로 가져오기
client=boto3.client('s3')
path='s3://newkeybucket/news.csv'
news=pd.read_csv(path)

#'title' 컬럼에서 '-'를 기준으로 분할하여 뒷부분을 'press' 컬럼에 저장
news['press'] = news['title'].str.split('-').str[-1].str.strip()
news['title'] = news['title'].str.split('-').str[0].str.strip()
news['title_content']=news['title']+news['content']

# 정규 표현식을 통한 한글 외 문자 제거
news['title_content'] = news['title_content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

#결측치 삭제
news.dropna(subset=['title_content'], inplace=True)
print(news['title_content'])

# 불용어 정의
stopwords = ['의','가','이','은','들','는','다소','잘','과','도','를','을','으로','에','와','하다','것','이지','대해','에서','되다','있다','하지만','정말','라면','일단','그렇게','이제']

# 토큰화
okt = Okt() #한국어 맞춤
news['token'] = news['title_content'].apply(lambda x: ' '.join([word for word in okt.morphs(x, stem=True) if not word in stopwords]))
cv=CountVectorizer(max_features=1000)
vectors=cv.fit_transform(news['token']).toarray()

#유사도 행렬
similarity=cosine_similarity(vectors)

#추천
def recommend(n):
    mlist = []
    news_index = news[news['title'] == n].index[0]
    distances = similarity[news_index]
    news_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:3]

    for i in news_list:
        print(news.loc[i[0], 'title'])
        mlist.append(news.loc[i[0], 'title'])

    return mlist

#안드로이드와 통신을 위한 서버
app = Flask(__name__)

@app.route('/')
def hello():
    print('hello!!')

@app.route('/news',methods=['POST'])
def news_recommend():
    title=request.form['title']
    result=recommend(title)

    return str(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)




