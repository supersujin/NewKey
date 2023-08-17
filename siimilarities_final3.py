import matplotlib.pyplot as plt
from wordcloud import WordCloud
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
import numpy as np
import pandas as pd

# 데이터 로드
final = pd.read_csv('newkey.csv', encoding='cp949')

# KoNLPy의 Okt 객체 생성
okt = Okt()

# 텍스트 데이터에서 명사만 추출
sentences = [okt.nouns(text) for text in final['key']]

# 문서-단어 행렬 생성
dictionary = corpora.Dictionary(sentences)
corpus = [dictionary.doc2bow(text) for text in sentences]

# LDA 모델 학습
lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary)

# LDA에서 추출한 주요 단어들
words_lda = [word for idx, topic in lda_model.print_topics(-1) for word in topic.split('"')[1::2]]

# TF-IDF 계산
# '대해'를 stop words로 추가
stop_words = ['대해']
tfidf = TfidfVectorizer(stop_words=stop_words)
res = tfidf.fit_transform(final['key']).toarray()
tfidf_feature_names = np.array(tfidf.get_feature_names_out())
importance = res.sum(axis=0)

# LDA 단어들의 TF-IDF 가중치 계산, 단어 길이가 2 이상인 경우만 포함
word_weights = {}
for word in words_lda:
    if len(word) > 1 and word in tfidf_feature_names:  # 한 글자 단어 제외
        idx = list(tfidf_feature_names).index(word)
        word_weights[word] = importance[idx]

# 워드 클라우드 생성
font_path = 'C:/Windows/Fonts/malgun.ttf'
wc = WordCloud(font_path=font_path, width=800, height=400, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(word_weights)

plt.figure(figsize=(10, 5))
plt.imshow(gen)
plt.axis('off')
plt.show()
