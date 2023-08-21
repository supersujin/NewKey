import boto3
from flask import Flask,request,send_file
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import threading
import time
import csv
import openai
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import ast as ast
import math

#다른 팀원들은 s3 접근 권한 없어 오류날 것이므로 이 코드 주석 처리 후 news.csv파일 따로 가져오기
client=boto3.client('s3')
news_path='s3://newkeybucket/newkey.csv'
news=pd.read_csv(news_path, encoding='UTF8')
try: news.drop(['Unnamed: 0'], axis=1, inplace=True)
except: print("no Unnamed: 0")


def reset_accumulate_click():
    # 1시간마다 기사 누적 클릭수 초기화
    while True:
        time.sleep(3600)  # 3600초 = 1시간

        news = pd.read_csv(news_path, encoding='cp949')
        try: news.drop(['Unnamed: 0'], axis=1, inplace=True)
        except: print("no Unnamed: 0")

        news['accumulate_click'] = 0
        news.to_csv("newkey.csv")

        # S3 버킷 이름과 업로드할 파일 경로 지정
        bucket_name = 'newkeybucket'
        local_file_path = 'newkey.csv'
        s3_file_path = 'newkey.csv'

        # CSV 파일 S3에 업로드
        client.upload_file(local_file_path, bucket_name, s3_file_path)


# 별도의 스레드에서 reset_accumulate_click 함수 실행
reset_thread = threading.Thread(target=reset_accumulate_click)
reset_thread.daemon = True  # 메인 스레드 종료 시 함께 종료
reset_thread.start()


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
def recommend():
    news = pd.read_csv(news_path, encoding='UTF8')
    try: news.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    user_path = 's3://newkeybucket/user.csv'
    user = pd.read_csv(user_path)  # uc=userClick
    try: user.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    wordsList_path = 's3://newkeybucket/wordsList.csv'
    wordsList = pd.read_csv(wordsList_path)  # uc=userClick
    try: wordsList.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")
    wordsList = list(wordsList)

    user_id=request.form['user_id']

    # 뉴스 데이터 인덱스 열 새로 만들기
    news['index'] = news.index

    # 뉴스 인덱스를 리스트 형태로 변환하여 저장
    articles = news['index'].astype(int).tolist()

    # ast.literal_eval: list 형태의 문자열을 실제 사용 가능하도록 list로 변환
    user['click_news'] = user['click_news'].apply(ast.literal_eval)
    user['select_cat'] = user['select_cat'].apply(ast.literal_eval)

    # 뉴스 카테고리 개수
    categoryCount = 62

    # topK 개수 설정
    k = 30

    # user가 클릭한 뉴스 id 리스트
    try:
        user_click_news = user[user['user_id'] == user_id]['click_news'].iloc[0]
    except:
        user_click_news=[]

    # 사용자가 보지 않은 뉴스만 다시 추출
    news = news[~(news['id'].isin(user_click_news))]

    #### 1. 사용자 카테고리 기반 추천 ####

    def categoryBased(user_id):

        # topK 데이터를 담을 dataframe
        df_topK = pd.DataFrame()

        # 사용자가 선택한 관심 카테고리의 번호 취합
        user_select_cat = user[user['user_id'] == user_id]['select_cat'].iloc[0]
        user_select_cat_len = len(user_select_cat)

        for i in range(user_select_cat_len):

            # 사용자가 선택한 카테고리와 같은 카테고리의 기사
            df_select = news[news['section2'] == user_select_cat[i]]

            if df_select.empty:  # 만약 없다면
                pass
            elif df_select.shape[0] <= (k // user_select_cat_len):  # 있는데 개수가 적을 경우
                df_select = df_select.sample(frac=1)  # random
                df_topK = pd.concat([df_topK, df_select], ignore_index=True, axis=0)  # 그대로 저장
            else:  # 있고 데이터의 개수도 많을 경우
                df_select = df_select.sample(frac=1)  # random
                df_topK = pd.concat([df_topK, df_select.head(k // user_select_cat_len + 1)], ignore_index=True, axis=0)  # 개수를 제한하여 저장

        df_topK = df_topK.sample(frac=1).reset_index(drop=True)

        return df_topK

    #### 2. Item-Based CF ####

    def itemBasedCF(userId):
        user_history = {}
        for i, user_id in enumerate(user['user_id']):
            user_history[user_id] = user['click_news'][i]

        for user_id, articles_str in user_history.items():
            articles_int = [int(article) for article in articles_str]
            user_history[user_id] = articles_int

        class NewKeyRecommendationSystem:

            # 딕셔너리&변수 초기화
            def __init__(self):
                self.dictCount = {}
                self.dictBiCount = {}
                self.nTotal = 0

            # 사용자 기사 클릭 이력 학습
            # (input : 사용자 기사 클릭 이력)
            # (output : 각 기사 빈도 & 바이그램 빈도 업데이트)
            def train(self, user_history, time_window):
                for user in user_history:
                    articles = user_history[user]
                    self.nTotal += len(articles)  # self.nTotal : 총 모든 기사 조회수
                    for article in articles:  # articles에 있는 기사별 읽은 횟수 세기
                        self.dictCount[article] = self.dictCount.get(article, 0) + 1
                    for i in range(len(articles) - 1):  # 바이그램 활용하여 빈도 세기
                        vj = articles[i]
                        vk = articles[i + 1]
                        self.dictBiCount[vj, vk] = self.dictBiCount.get((vj, vk), 0) + 1

            # 특정 바이그램 빈도 반환
            def getCoOccurrence(self, vj, vk):
                return self.dictBiCount.get((vj, vk), 0)

            # PMI 점수 계산&반환
            def getPMI(self, vj, vk):
                co = self.getCoOccurrence(vj, vk)
                if not co:
                    return None
                p_vj = self.dictCount[vj] / self.nTotal
                p_vk = self.dictCount[vk] / self.nTotal
                p_vj_vk = co / self.nTotal
                return math.log(p_vj_vk / (p_vj * p_vk))

            # NPMI 점수 계산&반환
            def getNPMI(self, vj, vk):
                pmi = self.getPMI(vj, vk)
                if pmi is None:
                    return -1
                return -pmi / math.log(self.getCoOccurrence(vj, vk) / self.nTotal)

            # 사용자에게 추천할 기사 생성
            # NPMI 활용하여 상위 K개 추출
            def getRecommendations(self, user_history, user_id, k=1000):
                user_articles = user_history[user_id]
                recommendations = []  # NPMI 저장할 준비
                for vk in self.dictCount:  # 모든 기사 빈도수 저장
                    if vk not in user_articles:  # vk 안 읽은거라면 최솟값으로 초기화
                        max_npmi = -float('inf')
                        for vj in user_articles:  # 추천해줄 사용자가 소비한 vj NPMI 점수계산
                            npmi = self.getNPMI(vj, vk)
                            if npmi > max_npmi:
                                max_npmi = npmi
                        recommendations.append((vk, max_npmi))
                recommendations.sort(key=lambda x: x[1], reverse=True)  # 내림차순 정렬
                return recommendations[:k]

        # 네이버 뉴스 추천시스템 생성 및 학습
        news_rec_sys = NewKeyRecommendationSystem()
        news_rec_sys.train(user_history, time_window=7)

        # 추천 기사 목록 및 NPMI 점수 가져오기
        recommendations = news_rec_sys.getRecommendations(user_history, userId)

        # 추천 결과를 데이터프레임으로 생성
        recommendations_df = pd.DataFrame(recommendations, columns=["news", "NPMI"])

        # 추천된 기사 목록만 추출하여 데이터프레임 생성
        recommended_articles = recommendations_df["news"].tolist()
        recom_articles_df = news[news["id"].isin(recommended_articles)]

        # 추천된 기사를 NPMI 점수 기준으로 내림차순 정렬
        recom_articles_df = recom_articles_df.merge(recommendations_df, left_on="id", right_on="news")
        recom_articles_df = recom_articles_df.sort_values(by="NPMI", ascending=False)

        # 최종 결과 출력
        recom_articles_df.drop(['news', 'NPMI'], axis=1, inplace=True)

        return recom_articles_df.reset_index(drop=True)

    #### 3-1. 단기간 클릭수 기반 추천 ####

    def clickedBased():

        # 뉴스의 click수를 기준으로 정렬
        df_topK = news.groupby('accumulate_click', sort=True)

        # random으로 섞은 뉴스들을 담을 list
        shuffled_rows = []

        for _, group in df_topK:
            shuffled_group = group.sample(frac=1)  # 같은 click수를 가진 뉴스끼리 랜덤으로 섞기
            shuffled_rows.append(shuffled_group)

        shuffled_rows.reverse()  # 뉴스 click수 오름차순 -> 내림차순

        df_topK = pd.concat(shuffled_rows)

        return df_topK.reset_index(drop=True)

    #### 3-2. 실시간 키워드 기반 ####

    def keywordBased(keyword_list):

        df_keyword_list = []

        # 키워드가 들어간 기사 뽑아내기 & 사용자가 보지 않은 기사만 뽑아내기 & 최근순으로 정렬하기
        for keyword in keyword_list:
            df_keyword = news[news['content'].str.contains(keyword, case=False)]
            df_keyword = df_keyword.sort_values(by='date')
            df_keyword_list.append(df_keyword.head(k // len(keyword_list) + 1))  # 적절한 개수 정도만 list에 저장하기

        df_topK = pd.concat(df_keyword_list)

        # 높은 순위만 위에 고정적으로 노출되는 것을 방지하기 위해 random으로 섞기
        df_topK = df_topK.sample(frac=1)

        return df_topK.reset_index(drop=True)

    #### main ####

    result1 = categoryBased(user_id)
    result2 = itemBasedCF(user_id)
    result3_1 = clickedBased()
    result3_2 = keywordBased(wordsList)
    list_result = [result1, result2, result3_1, result3_2]

    new_result_rows = []

    # 모든 df들의 행을 번갈아가면서 가져와서 새로운 리스트에 추가
    max_rows = max(len(df) for df in list_result)  # 가장 큰 행 수를 찾음
    for i in range(max_rows):
        for df in list_result:
            if i < len(df):
                new_result_rows.append(df.iloc[i])

    # 새로운 df 생성
    df_result = pd.DataFrame(new_result_rows)
    df_result = df_result.drop(columns=['index'])
    df_result.reset_index(drop=True, inplace=True)
    df_result.drop_duplicates(inplace=True)

    result_json = df_result.to_json(orient='records', force_ascii=False)
    return result_json


@app.route('/wordsList')
def wordsList():
    words_path = 's3://newkeybucket/wordsList.csv'
    words = pd.read_csv(words_path)
    words=list(words)

    try: words.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    return words

@app.route('/wordsImage')
def wordsImage():
    news.dropna(subset=['key'], inplace=True)

    # KoNLPy의 Okt 객체 생성
    okt = Okt()

    # 텍스트 데이터에서 명사만 추출
    sentences = [okt.nouns(text) for text in news['key']]

    # 문서-단어 행렬 생성
    dictionary = corpora.Dictionary(sentences)
    corpus = [dictionary.doc2bow(text) for text in sentences]

    # LDA 모델 학습
    lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary)

    # LDA에서 추출한 주요 단어들
    words_lda = [word for idx, topic in lda_model.print_topics(-1) for word in topic.split('"')[1::2]]

    stop_words = ['대해','대한','기사','사건','발생',"관련",'한국','상승','결과','훈련','출시','이야기','여자',
                  '대회','발견','선수','대한민국','사업','행사','발령','내용','사고','시작','실적','경기','오픈',
                  '혐의','촉구','증가','정보','가격','승리','이용자','서비스','정상화','시즌','대표','방문','이벤트',
                  '진행','형님','판매','이용','지원','세계','남자','리그','발표','매출','인상','집회','복귀','공개',
                  '모델','활동','시범','개발']

    # TF-IDF 계산
    tfidf = TfidfVectorizer(stop_words=stop_words)
    res = tfidf.fit_transform(news['key']).toarray()
    tfidf_feature_names = np.array(tfidf.get_feature_names_out())
    importance = res.sum(axis=0)

    # LDA 단어들의 TF-IDF 가중치 계산, 단어 길이가 2 이상인 경우만 포함
    word_weights = {}
    for word in words_lda:
        if len(word) > 1 and word in tfidf_feature_names:  # 한 글자 단어 제외
            idx = list(tfidf_feature_names).index(word)
            word_weights[word] = importance[idx]

    words = list(word_weights.keys())[:10]
    print(words)

    with open('wordsList.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(words)

    # s3 저장소에 실시간으로 words 리스트 올리기
    bucket_name = 'newkeybucket'
    local_file_path = 'wordsList.csv'
    s3_file_path = 'wordsList.csv'

    client.upload_file(local_file_path, bucket_name, s3_file_path)

    c = Counter(words)

    # s3 저장소에 실시간으로 words 사진 올리기
    font_path = 'malgun.ttf' # 폰트 경로 지정
    wc = WordCloud(font_path=font_path, width=800, height=400, scale=2.0, max_font_size=250)
    gen = wc.generate_from_frequencies(c)
    gen.to_file("wordcloud.jpg")

    return send_file("wordcloud.jpg", mimetype='image/jpg')


@app.route('/search',methods=['POST'])
def search():
    keyword = request.form['keyword']
    keyword_rows = news[news['content'].str.contains(keyword, case=False)]
    result = keyword_rows.to_dict('records')
    return str(result)


@app.route('/keyword',methods=['POST'])
def keyword():
    keyword = request.form['keyword']
    keyword_rows = news[news['title'].str.contains(keyword, case=False)]
    result = keyword_rows.to_dict('records')
    return str(result)


@app.route('/click',methods=['POST'])
def user_click():
    user_id=request.form['user_id']
    click_news=request.form['click_news']

    user_path = 's3://newkeybucket/user.csv'
    uc = pd.read_csv(user_path)  # uc=userClick

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

    #단기간(1시간) 누적 뉴스 클릭수, 1시간마다 초기화
    news = pd.read_csv(news_path, encoding='UTF8')
    try: news.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    news['id'] = news['id'].astype('str')
    row_index = news[news['id'] == click_news].index[0]
    news.at[row_index,'accumulate_click']+=1
    news.to_csv("newkey.csv")

    # S3 버킷 이름과 업로드할 파일 경로 지정
    bucket_name = 'newkeybucket'
    local_file_path = 'newkey.csv'
    s3_file_path = 'newkey.csv'

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


@app.route('/selCat',methods=['POST'])
def selCat():
    user_path = 's3://newkeybucket/user.csv'
    uc = pd.read_csv(user_path)  # uc=userClick

    try: uc.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    userId = request.form['user_id']
    uc['user_id'] = uc['user_id'].astype('str')
    row_index = uc[uc['user_id'] == userId].index[0]
    select_cat_list = ast.literal_eval(uc.at[row_index,'select_cat'])
    return str(select_cat_list)


@app.route('/viewNews',methods=['POST'])
def viewNews():
    user_path = 's3://newkeybucket/user.csv'
    uc = pd.read_csv(user_path)  # uc=userClick

    try: uc.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    userId = request.form['user_id']
    uc['user_id'] = uc['user_id'].astype('str')
    row_index = uc[uc['user_id'] == userId].index[0]
    click_news_list = ast.literal_eval(uc.at[row_index, 'click_news'])

    news['id'] = news['id'].astype('str')

    view_rows = news[news['id'].isin(click_news_list)]
    result = view_rows.to_dict('records')
    return str(result)


def modify_answer(answer, index):
    sentences = answer.split('. ')
    if len(sentences) > 1:
        answer = sentences[1]
    if answer.endswith('.'):
        answer = answer[:-1]
    if '주체는 ' in answer:
        answer = answer.split('주체는 ')[1]
    answer = answer.replace("이 기사는 ", "")
    answer = answer.split('이다')[0].strip()
    answer = answer.split('되었음')[0].strip()
    answer = answer.split('입니다')[0].strip()
    if '됩' in answer:
        answer = answer.split('됩')[0].strip() + '됨'
    if '됐' in answer:
        answer = answer.split('됐')[0].strip() + '됨'
    if '된' in answer:
        answer = answer.split('된')[0].strip() + '됨'
    if '했' in answer:
        answer = answer.split('했')[0].strip() + '함'
    if '하였' in answer:
        answer = answer.split('하였')[0].strip() + '함'
    answer = answer.split('되었')[0].strip()
    answer = answer.split('합니다')[0].strip()
    if answer.endswith('목적으로'):
        answer = answer.split('목적으로')[0].strip() + ' 목적으로'
    if answer.endswith('때문에'):
        answer = answer.split('때문에')[0].strip() + ' 때문에'
    if answer.endswith('습니다'):
        answer = answer.split('습니다')[0].strip() + '음'
    # 누가
    if index == 0:
        answer = answer.split('이 ')[0].strip()
        answer = answer.split('가 ')[0].strip()
    # 언제
    if index == 1:
        answer = answer.split('에서')[0].strip()
        answer = answer.split('에 ')[0].strip()
        if '은 ' in answer:
            answer = answer.split('은 ')[1].strip()
        if '는 ' in answer:
            answer = answer.split('는 ')[1].strip()
        if '일' in answer:
            answer = answer.split('일')[0].strip() + '일'
    if index == 2:
        answer = answer.split('에서')[0].strip()
        if '은 ' in answer:
            answer = answer.split('은 ')[1].strip()
        if '는 ' in answer:
            answer = answer.split('는 ')[1].strip()
    if index == 4:
        if '위해' in answer:
            answer = answer.split('위해')[0].strip() + ' 위해'
    if answer.endswith('다'):
        answer = answer.split('다')[0].strip() + '음'

    return answer

# --chatGPT api key
openai.api_key = 'openai.api_key'
openai.Timeout = 60 * 1000  # 10분으로 timeout 설정(너무 짧으면 에러 발생)

class ChatGPT:
    def __init__(self, summary_content):
        self.content = f"Content: {summary_content}"

    def run_gpt(self, questions):
        MAX_RETRIES = 3
        RETRY_DELAY = 10
        answers = []  # 답변을 모을 리스트

        for question in questions:
            gpt_standard_messages = [
                {"role": "system", "content": self.content},
                {"role": "user", "content": question}
            ]

            for attempt in range(MAX_RETRIES):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=gpt_standard_messages,
                        temperature=0.8
                    )
                    break
                except:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_DELAY)
                    else:
                        raise

            answer = response['choices'][0]['message']['content']
            answers.append(answer)  # 답변을 리스트에 추가

        return answers  # 답변의 리스트 반환

    def extract_5w1h(self,summary,key):
        additional_content = "육하원칙에 대응하는 답을 짧게 단답형으로 대답해. 문장말고 단답!!"
        if key is not None: #key가 null이 아니면
            content = f"Content: {summary}\nAdditional Content: {additional_content}"
            self.content = content
            questions = [f"{key} 주체가 누구야?",
                         f"{key} 언제 일어났어?",
                         f"{key} 어디에서 일어났어?",
                         f"{key} 어떻게 일어났어?",
                         f"{key} 왜 일어났어?"]
            answers = self.run_gpt(questions)

            modified_answers = []
            for index, answer in enumerate(answers):
                modified_answers.append(modify_answer(answer, index))

        print(modified_answers)
        result = "- 누가: " + modified_answers[0] + "\n" + \
                 "- 언제: " + modified_answers[1] + "\n" + \
                 "- 어디서: " + modified_answers[2] + "\n" + \
                 "- 어떻게: " + modified_answers[3] + "\n" + \
                 "- 왜: " + modified_answers[4]

        return result


@app.route('/5w1h',methods=['POST'])
def fiveWOneH():
    newsId = request.form['id']
    summary = request.form['summary']
    key = request.form['key']

    fwoh_path = 's3://newkeybucket/5w1h.csv'
    fwoh = pd.read_csv(fwoh_path, encoding='UTF8')
    try: fwoh.drop(['Unnamed: 0'], axis=1, inplace=True)
    except: print("no Unnamed: 0")

    fwoh['id'] = fwoh['id'].astype('str')

    if any(newsId in value for value in fwoh['id']):
        row_index = fwoh[fwoh['id'] == newsId].index[0]
        result = fwoh.at[row_index, '5w1h']
        return str(result)

    else:
        chat_gpt = ChatGPT(summary_content="")
        result=chat_gpt.extract_5w1h(summary,key)

        new_row = {'id': newsId, '5w1h': result}
        revise_fwoh = pd.concat([fwoh, pd.DataFrame([new_row])], ignore_index=True)
        revise_fwoh.to_csv("5w1h.csv")

        # S3 버킷 이름과 업로드할 파일 경로 지정
        bucket_name = 'newkeybucket'
        local_file_path = '5w1h.csv'
        s3_file_path = '5w1h.csv'

        # CSV 파일 S3에 업로드
        client.upload_file(local_file_path, bucket_name, s3_file_path)

        return str(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)





