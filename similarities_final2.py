import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora
from gensim.models.ldamodel import LdaModel

# 한글과 영어만 남기고 특수문자, 한자 등 제거
p = re.compile('[가-횧a-zA-Z]*')

final = pd.read_csv('newkey.csv', encoding='cp949')
final['key'] = final['key'].apply(lambda x: ' '.join(p.findall(str(x))))

def extractKeywords(okt, text):
    excluded_words = ['사건', '기사', '여자', '남자', '세계', '한국', '발생', '결과', '관련']  # Words to be excluded
    nouns = []
    for word, pos in okt.pos(text, stem=True):
        if pos == 'Noun' and len(word) > 1 and word not in excluded_words:
            nouns.append(word)
    return ' '.join(nouns)

okt = Okt()
df = final['key'].apply(lambda x: pd.Series(extractKeywords(okt, x)))
df.columns = ['noun']

df_final = pd.concat([final, df], axis=1)
df_final['all'] = df_final['noun']

tfidf = TfidfVectorizer()
res = tfidf.fit_transform(df_final['all']).toarray()

n_top = 500
importance = res.sum(axis=0)
tfidf_feature_names = np.array(tfidf.get_feature_names_out())
top_tfidf_indices = importance.argsort()[-n_top:][::-1]
top_tfidf_keywords = tfidf_feature_names[top_tfidf_indices]

def topKeywords(okt, keywords, n_top, min_length):
    keywords = ' '.join(keywords)
    nouns = extractKeywords(okt, keywords)
    filtered_nouns = filter_short_keywords(nouns.split(), min_length)
    return filtered_nouns[:n_top]

def filter_short_keywords(keywords, min_length):
    return [keyword for keyword in keywords if len(keyword) >= min_length]

top_number = 10
min_keyword_length = 2
top_nouns = topKeywords(okt, top_tfidf_keywords, top_number, min_keyword_length)

print("\n키워드:")
print(", ".join(top_nouns))
print(top_tfidf_keywords)

# LDA 토픽 모델링
sentences = [text.split() for text in df_final['all']]
dictionary = corpora.Dictionary(sentences)
corpus = [dictionary.doc2bow(text) for text in sentences]
lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary)

# LDA를 이용해 주요 토픽별 주요 단어 추출하여 워드 클라우드 생성에 활용
words = [word for idx, topic in lda_model.print_topics(-1) for word in topic.split('"')[1::2]]

# 워드 클라우드 생성
c = Counter(words)
font_path = 'C:/Windows/Fonts/malgun.ttf'
wc = WordCloud(font_path=font_path, width=800, height=400, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(c)
plt.figure(figsize=(10, 5))
plt.imshow(gen)
plt.axis('off')
plt.show()
