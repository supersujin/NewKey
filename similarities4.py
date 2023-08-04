import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt

#한글이랑 영어만 남기고 특수문자, 한자 등을 제거
import re
p=re.compile('[가-횧a-zA-Z]*') #정규식 패턴

# 이전 포스팅에서 크롤링 결과 저장한 것 불러오기
final = pd.read_csv('한국언론진흥재단_수정본.csv', encoding='utf-8')

# '키워드' 열에 있는 값을 문자열로 변환하고, 한글과 영어만 추출
final['키워드'] = final['키워드'].apply(lambda x: ' '.join(p.findall(str(x))))

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
df = final['키워드'].apply(lambda x: pd.Series(extractKeywords(okt, x)))
df.columns = ['noun', 'verb', 'adj']

# 앞서 크롤링 했던 DataFrame이랑 합치기
df_final = pd.concat([final, df], axis=1)

# 'all' 컬럼 생성
df_final['all'] = df_final['noun'] + ' ' + df_final['verb'] + ' ' + df_final['adj']

# df_final['all']에 TF-IDF 적용
from sklearn.feature_extraction.text import TfidfVectorizer

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

# 폰트 경로 지정 (Malgun Gothic 폰트를 사용하도록 설정)
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 폰트 경로는 각자의 환경에 맞게 설정해야 합니다.

wc = WordCloud(font_path=font_path, width=800, height=400, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(c)
plt.figure(figsize=(10, 5))
plt.imshow(gen)
plt.axis('off')
plt.show()
