#받은 news df 전처리 & 추천 알고리즘 짜기(채은&예슬이가 수정)
import boto3
from flask import Flask,request
import pandas as pd
import ast
import re
#from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
#import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#다른 팀원들은 s3 접근 권한 없어 오류날 것이므로 이 코드 주석 처리 후 news.csv파일 따로 가져오기
client=boto3.client('s3')
news_path='s3://newkeybucket/newkey.csv'
news=pd.read_csv(news_path, encoding='cp949')

'''
news['title_content']=news['title']+news['content']

# 정규 표현식을 통한 한글 외 문자 제거
news['title_content'] = news['title_content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

#결측치 삭제
news.dropna(subset=['title_content'], inplace=True)
print(news)

# 불용어 정의
stopwords = ['의','가','이','은','들','는','다소','잘','과','도','를','을','으로','에','와','하다','것','이지','대해','에서','되다','있다','하지만','정말','라면','일단','그렇게','이제']

# 토큰화
okt = Okt()
news['token'] = news['title_content'].apply(lambda x: ' '.join([word for word in okt.morphs(x, stem=True) if not word in stopwords]))
cv=CountVectorizer(max_features=1000)
vectors=cv.fit_transform(news['token']).toarray()

#유사도 행렬
similarity=cosine_similarity(vectors)
'''

#추천
def recommend(n):
    '''
    mlist = []
    news_index = news[news['title'] == n].index[0]
    distances = similarity[news_index]
    news_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:3]

    for i in news_list:
        print(news.loc[i[0], 'title'])
        mlist.append(news.loc[i[0], 'title'])

    return mlist
    '''
    return "recommend"


#안드로이드와 통신을 위한 서버
app = Flask(__name__)

@app.route('/')
def hello():
    news_json=news.to_json(orient='records',force_ascii=False)
    return news_json

@app.route('/politic')
def politic():
    politic_json=news[news['section1']==100].to_json(orient='records',force_ascii=False)
    return politic_json

@app.route('/economic')
def economic():
    economic_json=news[news['section1']==101].to_json(orient='records',force_ascii=False)
    return economic_json

@app.route('/social')
def social():
    social_json=news[news['section1']==102].to_json(orient='records',force_ascii=False)
    return social_json

@app.route('/life')
def life():
    life_json=news[news['section1']==103].to_json(orient='records',force_ascii=False)
    return life_json

@app.route('/world')
def world():
    world_json=news[news['section1']==104].to_json(orient='records',force_ascii=False)
    return world_json

@app.route('/it')
def it():
    it_json=news[news['section1']==105].to_json(orient='records',force_ascii=False)
    return it_json

@app.route('/opinion')
def opinion():
    opinion_json=news[news['section1']==110].to_json(orient='records',force_ascii=False)
    return opinion_json

@app.route('/sport')
def sport():
    sport_json=news[news['section1']==120].to_json(orient='records',force_ascii=False)
    return sport_json

@app.route('/entertainment')
def entertainment():
    entertainment_json=news[news['section1']==130].to_json(orient='records',force_ascii=False)
    return entertainment_json

@app.route('/recommend',methods=['POST'])
def news_recommend():
    title=request.form['title']
    result=recommend(title)
    print(result)

    return result

@app.route('/wordcloud')
def wordcloud():
    p = re.compile('[가-횧a-zA-Z]*')  # 정규식 패턴

    # '키워드' 열에 있는 값을 문자열로 변환하고, 한글과 영어만 추출
    news['summary'] = news['summary'].apply(lambda x: ' '.join(p.findall(str(x))))

    # Headline 형태소 분석 (명사, 동사, 형용사)
    def extractKeywords(okt, text):
        nouns = []
        verbs = []
        adjectives = []
        for word, pos in okt.pos(text, stem=True):
            if pos == 'Noun':
                nouns.append(word)
            elif pos == 'Verb':
                verbs.append(word)
            elif pos == 'Adjective':
                adjectives.append(word)
        return ' '.join(nouns), ' '.join(verbs), ' '.join(adjectives)

    okt = Okt()
    df = news['summary'].apply(lambda x: pd.Series(extractKeywords(okt, x)))
    df.columns = ['noun', 'verb', 'adj']

    # 앞서 크롤링 했던 DataFrame이랑 합치기
    df_final = pd.concat([news, df], axis=1)

    # 'all' 컬럼 생성
    df_final['all'] = df_final['noun'] + ' ' + df_final['verb'] + ' ' + df_final['adj']

    # df_final['all']에 TF-IDF 적용
    tfidf = TfidfVectorizer()
    res = tfidf.fit_transform(df_final['all']).toarray()

    # TF-IDF 기준 상위 n_top 개수 키워드 추출
    n_top = 300
    importance = res.sum(axis=0)
    tfidf_feature_names = np.array(tfidf.get_feature_names_out())
    top_tfidf_indices = importance.argsort()[-n_top:][::-1]
    top_tfidf_keywords = tfidf_feature_names[top_tfidf_indices]

    # TF-IDF 기준 상위 top 개수만큼 품사별 키워드 추출 (명사, 동사, 형용사)
    def topKeywords(okt, keywords, n_top):
        keywords = ' '.join(keywords)
        nouns, verbs, adjectives = extractKeywords(okt, keywords)
        return nouns.split()[:n_top], verbs.split()[:n_top], adjectives.split()[:n_top]

    noun_top = 10
    verb_top = 10
    adj_top = 10
    noun, verb, adj = topKeywords(okt, top_tfidf_keywords, noun_top)

    print(f'top10 키워드:{top_tfidf_keywords}')
    print(f'명사 top:{noun}')
    print(f'동사 top: {verb}')
    print(f'형용사 top: {adj}')

    # 워드 클라우드 생성
    words = [n for n in noun if len(n) > 1]
    c = Counter(words)
    print(words)
    '''
        # 폰트 경로 지정 (Malgun Gothic 폰트를 사용하도록 설정)
        font_path = 'C:/Windows/Fonts/malgun.ttf'  # 폰트 경로는 각자의 환경에 맞게 설정해야 합니다.

        wc = WordCloud(font_path=font_path, width=800, height=400, scale=2.0, max_font_size=250)
        gen = wc.generate_from_frequencies(c)
        plt.figure(figsize=(10, 5))
        plt.imshow(gen)
        plt.axis('off')
        plt.show()
    '''

    #s3 저장소에 실시간으로 words 올리기

    return words

@app.route('/search',methods=['POST'])
def search():
    keyword=request.form['keyword']
    keyword_json = news[news['content'].str.contains(keyword)].to_json(orient='records', force_ascii=False)
    return keyword_json

@app.route('/click',methods=['POST'])
def user_click():
    user_id=request.form['user_id']
    click_news=request.form['click_news']

    click_path = 's3://newkeybucket/user.csv'
    uc = pd.read_csv(click_path)  # uc=userClick

    try: uc.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    uc['user_id'] = uc['user_id'].astype('str')

    row_index = uc[uc['user_id']==user_id].index[0] #현재 사용자 행
    click_news_list = ast.literal_eval(uc.at[row_index, 'click_news'])
    click_news_list.append(click_news) #클릭 뉴스 list에 추가
    click_news_list=list(set(click_news_list)) #같은 뉴스 클릭했을 경우 중복 제거
    uc.at[row_index, 'click_news'] = click_news_list
    uc.to_csv("user.csv")

    # S3 버킷 이름과 업로드할 파일 경로 지정
    bucket_name = 'newkeybucket'
    local_file_path = 'user.csv'
    s3_file_path = 'user.csv'

    # CSV 파일 S3에 업로드
    client.upload_file(local_file_path, bucket_name, s3_file_path)

    return "click"

@app.route('/register',methods=['POST'])
def register():
    user_id=request.form['user_id']
    click_news = request.form['click_news']
    select_cat=request.form['select_cat']
    select_cat = ast.literal_eval(select_cat)

    click_path = 's3://newkeybucket/user.csv'
    uc = pd.read_csv(click_path)  # uc=userClick

    try: uc.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    new_row = {'user_id': user_id, 'click_news': click_news, 'select_cat': select_cat}
    revise_uc = pd.concat([uc, pd.DataFrame([new_row])], ignore_index=True)
    revise_uc.to_csv("user.csv")

    # S3 버킷 이름과 업로드할 파일 경로 지정
    bucket_name = 'newkeybucket'
    local_file_path = 'user.csv'
    s3_file_path = 'user.csv'

    # CSV 파일 S3에 업로드
    client.upload_file(local_file_path, bucket_name, s3_file_path)

    return "register"


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)




