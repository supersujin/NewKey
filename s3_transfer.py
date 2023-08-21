import time
import requests
from bs4 import BeautifulSoup
import boto3
import pandas as pd
import urllib.request
from urllib.parse import urlparse,parse_qs
from collections import OrderedDict
import chardet
import json
import openai
import re

s3 = boto3.resource('s3')
bucket_name = 'newkeybucket'  # S3 버킷 이름
object_name = 'newkey.csv'  # S3에 업로드될 CSV 파일 이름


def ex_tag(sid1, sid2, page):
    ### 뉴스 분야(sid)와 페이지(page)를 입력하면 그에 대한 링크들을 리스트로 추출하는 함수 ###

    # 정치는 100, 경제는 101, 사회는 102, 생활 / 문화는 103, 세계는 104, IT / 과학은 105
    if (sid1 == 100) or (sid1 == 101) or (sid1 == 102) or (sid1 == 103) or (sid1 == 104) or (sid1 == 105):
        url = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1={sid1}&sid2={sid2}"

    elif sid1 == 110:  # 오피니언
        url = "https://news.naver.com/opinion/"

        if sid2 == 111:
            url += "series"  # 연재
        elif sid2 == 112:
            url += "column"  # 칼럼
        elif sid2 == 113:
            url += "editorial"  # 사설

    elif sid1 == 120:  # 스포츠
        url = "https://sports.news.naver.com/"
        if sid2 == 121:
            url += "kbaseball/index"
        elif sid2 == 122:
            url += "wbaseball/index"
        elif sid2 == 123:
            url += "kfootball/index"
        elif sid2 == 124:
            url += "wfootball/index"
        elif sid2 == 125:
            url += "basketball/index"
        elif sid2 == 126:
            url += "volleyball/index"
        elif sid2 == 127:
            url += "golf/index"
        elif sid2 == 128:
            url += "general/index"

    elif sid1 == 130:  # 연예
        url = "https://entertain.naver.com/"
        if sid2 == 131:
            url += "home"
        elif sid2 == 132:
            url += "now?sid=309"

    url += f"#&date=%2000:00:00&page={page}"

    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0" \
                                                    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                                    "Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    a_tag = soup.find_all("a")

    ## 2.
    tag_lst = []
    for a in a_tag:
        if "href" in a.attrs:  # href가 있는 것만 고르는 것
            if (sid1 == 100) or (sid1 == 101) or (sid1 == 102) or (sid1 == 103) or (sid1 == 104) or (sid1 == 105):
                if (f"sid={sid1}" in a["href"]) and ("article" in a["href"]):
                    tag_lst.append(a["href"])
            elif sid1 == 110:
                if ("article" in a["href"]):
                    tag_lst.append(a["href"])
            elif sid1 == 120:
                if ("news" in a["href"]) and ("oid" in a["href"]) and ("news.naver.com" not in a["href"]):
                    a["href"] = "https://sports.news.naver.com" + a["href"]
                    tag_lst.append(a["href"])
            elif sid1 == 130:
                if sid2 == 131:
                    if ("read" in a["href"]) and ("https://entertain.naver.com" not in a["href"]):
                        a["href"] = "https://entertain.naver.com" + a["href"]
                        tag_lst.append(a["href"])
                elif sid2 == 132:
                    if ("read" in a["href"]) and ("now" in a["href"]) and (
                            "https://entertain.naver.com" not in a["href"]):
                        a["href"] = "https://entertain.naver.com" + a["href"]
                        tag_lst.append(a["href"])

    return tag_lst


def re_tag(sid1, sid2):
    ### 특정 분야의 100페이지까지의 뉴스의 링크를 수집하여 중복 제거한 리스트로 변환하는 함수 ###
    re_lst = []
    for i in range(1):
        lst = ex_tag(sid1, sid2, i + 1)
        re_lst.extend(lst)

    # 중복 제거
    re_set = set(re_lst)
    re_lst = list(re_set)

    return re_lst


all_hrefs = {}
sids1 = [100, 101, 102, 103, 104, 105, 110, 120, 130] # 정치,경제,사회,생활/문화,세계,IT/과학,오피니언,스포츠,연예
sids2 = [100264, 100265, 100266, 100267, 100268, 100269,
         101258, 101259, 101260, 101261, 101262, 101263, 101310, 101771,
         102249, 102250, 102251, 102252, 102254, 102255, 102256, 102257, 102276, 102596,
         103237, 103238, 103239, 103240, 103241, 103242, 103243, 103244, 103245, 103248, 103376,
         104231, 104232, 104233, 104234, 104322,
         105226, 105227, 105228, 105229, 105230, 105283, 105731, 105732,
         110111, 110112, 110113,
         120121, 120122, 120123, 120124, 120125, 120126, 120127, 120128,
         130131, 130132]

# 각 분야별로 링크 수집해서 딕셔너리에 저장
for s1 in sids1:
    all_hrefs[s1] = {}
    for s2 in sids2:
        s2_front = int(s2 / 1000)
        s2_back = int(s2 % 1000)

        if s2_front == s1:
            sid_data = re_tag(s1, s2_back)
            all_hrefs[s1][s2_back] = sid_data


def art_crawl(all_hrefs, sid1, sid2, index):
    art_dic = {}

    ## 1.
    if (sid1 == 100) or (sid1 == 101) or (sid1 == 102) or (sid1 == 103) or (sid1 == 104) or (sid1 == 105) or (sid1 == 110):
        title_selector = "#title_area > span"
        date_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans" \
                        "> div.media_end_head_info_datestamp > div:nth-child(1) > span"
        content_selector = "#dic_area"

    elif sid1 == 120:
        title_selector = "#content > div > div.content > div > div.news_headline > h4"
        date_selector = "#content > div > div.content > div > div.news_headline > div > span:nth-child(1)"
        content_selector = "#newsEndContents"

    elif sid1 == 130:
        title_selector = "#content > div.end_ct > div > h2"
        date_selector = "#content > div.end_ct > div > div.article_info > span > em"
        content_selector = "#articeBody"

    url = all_hrefs[sid1][sid2][index]
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 " \
                                                    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                                                    "Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")

    ## 2.
    # 제목 수집
    title = soup.select(title_selector)
    title_lst = [t.text for t in title]
    title_str = "".join(title_lst)

    # 날짜 수집
    date = soup.select(date_selector)
    date_lst = [d.text for d in date]
    date_str = "".join(date_lst)

    # 본문 수집
    content = soup.select(content_selector)
    content_lst = []

    for m in content:
        m_text = m.text
        m_text = m_text.strip()
        content_lst.append(m_text)
    content_str = "".join(content_lst)

    ## 3.
    art_dic["title"] = title_str
    art_dic["date"] = date_str
    if sid1 != 120:
        art_dic["content"] = content_str
    else:
        art_dic["content"] = content_str.split("기사제공")[0]

    print(art_dic["title"])

    return art_dic


# 모든 섹션의 데이터 수집 (제목, 날짜, 본문, section, url)
def collect_data():
    section1_lst = [100, 101, 102, 103, 104, 105, 110, 120, 130]
    section2_lst = [100264, 100265, 100266, 100267, 100268, 100269,
                    101258, 101259, 101260, 101261, 101262, 101263, 101310, 101771,
                    102249, 102250, 102251, 102252, 102254, 102255, 102256, 102257, 102276, 102596,
                    103237, 103238, 103239, 103240, 103241, 103242, 103243, 103244, 103245, 103248, 103376,
                    104231, 104232, 104233, 104234, 104322,
                    105226, 105227, 105228, 105229, 105230, 105283, 105731, 105732,
                    110111, 110112, 110113,
                    120121, 120122, 120123, 120124, 120125, 120126, 120127, 120128,
                    130131, 130132]
    artdic_lst = []

    for s1 in section1_lst:
        for s2 in section2_lst:
            s2_front = int(s2 / 1000)
            s2_back = int(s2 % 1000)

            if s2_front == s1:
                for i in range(len(all_hrefs[s1][s2_back])):
                    art_dic = art_crawl(all_hrefs, s1, s2_back, i)
                    art_dic["section1"] = s1
                    art_dic["section2"] = s2
                    art_dic["url"] = all_hrefs[s1][s2_back][i]

                    artdic_lst.append(art_dic)

    return artdic_lst


#데이터 전처리 & 기사 원본, 언론사,기자,기사 이미지,요약,키 컬럼 추가
def preprocess():
    news_list=collect_data()
    news = pd.DataFrame(news_list)
    news = news.dropna(subset='title', axis=0)
    news = news.dropna(subset='content', axis=0)

    #본문 전처리 전 컬럼 추가
    def origin(content):
        try:
            content_str = content[0].get_text(separator="<br/>")
            content_str = content_str.replace("<br/>", "", 1)
            content_str = content_str.replace("<br/>", "\n\n")
            content_str = re.sub('\n{3,}', '\n\n', content_str)
        except:
            print("origin error")
            return

        return content_str

    #news['origin_content'] = news['content'].apply(lambda x:origin(x))

    # 줄바꿈 제거
    def removeLB(x):
        return re.sub(r'\n+', ' ', x)

    # 탭 제거
    def removeTab(x):
        return re.sub(r'\t+', ' ', x)

    # 공백 여러자 -> 1자
    def removeMB(x):
        return ' '.join(x.split())

    # 제목,내용 정제
    news['title'] = news['title'].apply(lambda x: removeLB(x))
    news['title'] = news['title'].apply(lambda x: removeTab(x))
    news['title'] = news['title'].apply(lambda x: removeMB(x))

    news['content'] = news['content'].apply(lambda x: removeLB(x))
    news['content'] = news['content'].apply(lambda x: removeTab(x))
    news['content'] = news['content'].apply(lambda x: removeMB(x))

    # 날짜 정제
    cond1 = news['date'].str.count('2023') == 2
    cond2 = news['date'].str.contains('기사입력')

    def removeD1(x):
        idx1 = x.find('2023')
        idx2 = x.find('2023', idx1 + 1)

        return x[:idx2]

    def removeD2(x):
        return x.replace('기사입력', '')

    news.loc[cond1, 'date'] = news.loc[cond1, 'date'].apply(lambda x: removeD1(x))
    news.loc[cond2, 'date'] = news.loc[cond2, 'date'].apply(lambda x: removeD2(x))

    # 뉴스 id 추출
    def urlToId(url):

        if 'sports' in url or 'entertain' in url:
            pattern = r'aid=([0-9]+)'
            match = re.search(pattern, url)
            result = match.group(1)

        else:
            pattern = r'\/(\d+)[^\/]*$'
            match = re.search(pattern, url)
            result = match.group(1)

        return result

    news['id'] = news['url'].apply(lambda x: urlToId(x))

    # 중복 url 1개만
    news.drop_duplicates(subset=['id'], keep='first', inplace=True)
    # 중복 제목 1개만
    news.drop_duplicates(subset=['title'], keep='first', inplace=True)

    # id컬럼 맨 앞으로
    news = news[['id', 'title', 'date', 'content', 'section1', 'section2', 'url','origin_content']]

    # 언론사
    url_company = "https://news.naver.com/main/officeList.naver"
    html_company = urllib.request.urlopen(url_company).read()
    soup_company = BeautifulSoup(html_company, 'html.parser')
    title_company = soup_company.find_all(class_='list_press nclicks(\'rig.renws2pname\')')

    media_dict = {}
    for i in title_company:
        parts = urlparse(i.attrs['href'])
        media_dict[parse_qs(parts.query)['officeId'][0]] = i.get_text().strip()

    # https://news.naver.com/main/officeList.naver에 없는 언론사 따로 추가하기
    extra_dict = {
        '109': 'OSEN', '117': '마이데일리', '410': 'MK스포츠', '477': 'SPOTVnews', '076': '스포츠조선', '311': '엑스포츠뉴스',
        '065': 'JUMPBALL', '609': '뉴스엔', '108': '스타뉴스', '530': '더 스파이크',
        '413': '인터풋볼', '144': '스포츠경향', '112': '헤럴드POP', '468': '스포츠서울', '213': 'TV리포트', '398': '루키',
        '408': 'MBC연예', '343': '베스트일레븐', '445': 'MHN스포츠', '411': '포포투', '470': 'JTBC골프', '351': '바스켓코리아',
        '139': '스포탈코리아', '241': '일간스포츠', '312': '텐아시아', '435': '골프다이제스트', '438': 'KBS미디어', '396': '스포츠월드',
        '425': '마니아타임즈', '436': '풋볼리스트', '370': '한게임바둑', '450': 'STN스포츠', '353': '중앙SUNDAY'}

    media_dict.update(extra_dict)

    # 언론사 컬럼 추가
    def media(url):
        if 'oid' in url:
            pattern = r'oid=([0-9]+)'
        else:  # url에 oid가 없는 경우
            pattern = r"/article/(\d+)/"

        try:
            match = re.search(pattern, url)
            result = match.group(1)
            result = media_dict[result]  # result 한글 언론사로 바꾸기
        except:
            print('저장되지 않은 언론사입니다.')
            result = "none"

        return result

    news['media'] = news['url'].apply(lambda x: media(x))

    # 기자 컬럼 추가
    def report(url):
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0" \
                                                        "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                                        "Chrome/110.0.0.0 Safari/537.36"})

        soup = BeautifulSoup(html.text, "lxml")

        if 'entertain' in url:
            reportor_selector = "#content > div.end_ct > div > div.byline > p > span"
        elif 'sport' in url:
            reportor_selector = "#newsEndContents > p.byline"
        else:
            reportor_selector = "#contents > div.byline > p > span"

        try:
            reportor = soup.select(reportor_selector)
            reportor = reportor[0].get_text()
            pattern = r'[\w가-힣]+'
            match = re.search(pattern, reportor)
            reportor = match.group()

        except:
            if 'sport' in url:
                try:
                    reportor_selector = "#newsEndContents > div.reporter_area > div.reporter._type_journalist._JOURNALIST_15219 > div.reporter_profile > div > div.profile_info > a"
                    reportor = soup.select(reportor_selector)
                    reportor = reportor[0].get_text()
                    pattern = r'[\w가-힣]+'
                    match = re.search(pattern, reportor)
                    reportor = match.group()

                except:
                    reportor = "none"
            else:
                reportor = "none"

        return reportor

    news['reporter'] = news['url'].apply(lambda x: report(x))

    # 기자 잘못 추출된 것 수정
    cond1 = news['reporter'] == "서울월드컵경기장"
    cond2 = news['reporter'] == "실리콘밸리"
    cond3 = news['reporter'] == "후쿠오카"
    cond4 = news['reporter'] == "잠실"
    cond5 = news['reporter'] == "글"

    def reviseReporter1(url):
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0" \
                                                        "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                                        "Chrome/110.0.0.0 Safari/537.36"})

        soup = BeautifulSoup(html.text, "lxml")

        if 'entertain' in url:
            reportor_selector = "#content > div.end_ct > div > div.byline > p > span"
        elif 'sport' in url:
            reportor_selector = "#newsEndContents > p.byline"
        else:
            reportor_selector = "#contents > div.byline > p > span"

        try:
            reportor = soup.select(reportor_selector)
            reportor = reportor[0].get_text()
            pattern = r'=(\w+)'
            match = re.search(pattern, reportor)
            reportor = match.group(1)

        except:
            reportor="none"

        return reportor

    news.loc[(cond1 | cond2 | cond3 | cond4 | cond5), 'reporter'] = news.loc[(cond1 | cond2 | cond3 | cond4 | cond5), 'url'].apply(lambda x: reviseReporter1(x))

    def reviseReporter2(url):
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0" \
                                                        "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                                        "Chrome/110.0.0.0 Safari/537.36"})

        soup = BeautifulSoup(html.text, "lxml")
        reportor_selector = "#contents > div.byline > p > span"
        reportor = soup.select(reportor_selector)

        try:
            reportor = reportor[0].get_text()
            pattern = r'CBS노컷뉴스 (\w+)'
            match = re.search(pattern, reportor)
            reportor = match.group(1)
        except:
            reportor_selector = "#newsEndContents > p.byline"
            reportor = soup.select(reportor_selector)
            reportor = reportor[0].get_text()
            pattern = r'CBS노컷뉴스 (\w+)'
            match = re.search(pattern, reportor)
            reportor = match.group(1)

        return reportor

    news.loc[news['reporter'] == "CBS노컷뉴스", 'reporter'] = news.loc[news['reporter'] == "CBS노컷뉴스", 'url'].apply(lambda x: reviseReporter2(x))

    # 누적 클릭수 0으로 초기화
    news['accumulate_click'] = 0

    # 기사 이미지
    def findImg(url):
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0" \
                                                        "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                                        "Chrome/110.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(html.text, "lxml")

        # 모든 img 태그 찾기
        img_tags = soup.find_all('img')

        # img_tags 중 logo,origin,banner,scs-phinf,profile,type=nf112_112,journalist 제외
        valid_urls = [tag['src'] for tag in img_tags if
                      'src' in tag.attrs and 'logo' not in tag['src'] and 'origin' not in tag['src'] and 'banner' not in
                      tag['src']
                      and 'scs-phinf' not in tag['src'] and 'journalist' not in tag['src'] and 'profile' not in tag[
                          'src'] and 'type=nf112_112' not in tag['src']]

        if not valid_urls:
            valid_urls = [tag['data-src'] for tag in img_tags if
                          'data-src' in tag.attrs and 'logo' not in tag['data-src'] and 'origin' not in tag[
                              'data-src'] and 'banner' not in tag['data-src']
                          and 'scs-phinf' not in tag['data-src'] and 'journalist' not in tag[
                              'data-src'] and 'profile' not in tag['data-src'] and 'type=nf112_112' not in tag[
                              'data-src']]

        unique_urls = list(OrderedDict.fromkeys(valid_urls))

        try:
            result = unique_urls[0]
        except:
            result = "none"

        return result

    news['img'] = news['url'].apply(lambda x: findImg(x))

    # 자연어 처리
    # --Naver CLOVA api key
    client_id = 'client_id'
    client_secret = 'client_secret'
    url = 'https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'

    # --chatGPT api key
    openai.api_key = 'openai.api_key'
    openai.Timeout = 60 * 1000  # 10분으로 timeout 설정(너무 짧으면 에러 발생)

    def clean_text(text):
        cleaned_text = re.sub(r'[^가-힣.,\s]', '', str(text))
        return cleaned_text[:1998]

    # 요약
    def summary(id,secret,url,c):
        client_id = id
        client_secret = secret
        url = url
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-APIGW-API-KEY-ID': client_id,
            'X-NCP-APIGW-API-KEY': client_secret
        }

        content = clean_text(c)

        data = {
            "document": {
                "content": content
            },
            "option": {
                "language": "ko",
                "model": "news",
                "tone": 3,  # 말투 0: 했다. 1: 했어요. 2: 했습니다. 3: 함
                "summaryCount": 3
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(data).encode('UTF-8'))
        rescode = response.status_code

        if rescode == 200:
            response_data = json.loads(response.text)
            summary = response_data['summary']
        else:
            summary = "Error : " + response.text

        return summary

    news['summary'] = news['content'].apply(lambda c:summary(client_id,client_secret,url,c))
    print('Summary Update Complete!')

    class ChatGPT:
        def __init__(self, summary_content):
            self.content = f"Content: {summary_content}"

        def run_gpt(self, questions):
            MAX_RETRIES = 5
            RETRY_DELAY = 10

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
                            print("openai error")
                            return

                answer = response['choices'][0]['message']['content']

            return answer  # 답변의 문자열 반환

        def detect_encoding(self, file_path):
            with open(file_path, 'rb') as file:
                result = chardet.detect(file.read())
                return result['encoding']

        # 핵심 사건 추출
        def extract_key(self, summary):
            # 전처리(error/ blank 있는 row 제거)
            if summary.strip() == "" or summary.startswith("Error"):
                return "none"

            chat_bot_instance = ChatGPT(summary)
            key_question = ["이 기사는 어떤 사건에 대한 거야? 한국어 단답형 명사로 끝나도록 답해줘. 최대한 짧게."]
            answer = chat_bot_instance.run_gpt(key_question)

            answer = answer.replace("이 기사는 ", "")
            answer = answer.split('에 대한')[0].strip()
            answer = answer.split('에 관한')[0].strip()
            answer = answer.split('한 사건')[0].strip()
            answer = answer.split('와 관련된')[0].strip()
            answer = answer.split('과 관련된')[0].strip()
            answer = answer.split('한다는')[0].strip()
            answer = answer.split('을 하고')[0].strip()
            if answer.endswith('.'):
                answer = answer[:-1]

            print(answer)
            return answer

    # key 추출
    chat_gpt = ChatGPT(summary_content="")
    news['key']=news['summary'].apply(lambda s:chat_gpt.extract_key(s))

    news=news[news['summary'] != 'none']
    news.dropna(subset=['key'], inplace=True)
    print('Key Update Complete!')

    # 기존 CSV 파일 읽어오기
    client = boto3.client('s3')
    news_path = 's3://newkeybucket/newkey.csv'
    existing_news = pd.read_csv(news_path, encoding='UTF8')

    # 기존 DataFrame과 새로운 DataFrame 합치기
    combined_df = pd.concat([existing_news, news], ignore_index=True)

    # 합쳐진 DataFrame을 다시 CSV 파일로 저장
    combined_df.to_csv('newkey.csv', index=False)

    # s3 저장소에 실시간으로 words 리스트 올리기
    bucket_name = 'newkeybucket'
    local_file_path = 'newkey.csv'
    s3_file_path = 'newkey.csv'

    client.upload_file(local_file_path, bucket_name, s3_file_path)

    return "upload done"


# 실시간 크롤링 (중복 기사 삭제 필요)
def realTime_crawl():
    while True:
        preprocess()
        time.sleep(1200) # 20분 간격 크롤링


realTime_crawl()
