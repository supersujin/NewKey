import time
import requests
from bs4 import BeautifulSoup
import boto3
import csv
import io

s3 = boto3.resource('s3')
bucket_name = 'newkeybucket'  # S3 버킷 이름
object_name = 'news.csv'  # S3에 업로드될 CSV 파일 이름


def ex_tag(sid1, sid2, page):
    ### 뉴스 분야(sid)와 페이지(page)를 입력하면 그에 대한 링크들을 리스트로 추출하는 함수 ###

    ## 1. 정치는 100, 경제는 101, 사회는 102, 생활 / 문화는 103, 세계는 104, IT / 과학은 105
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
                # print(a["href"])
                if (f"sid={sid1}" in a["href"]) and ("article" in a["href"]):
                    print(a["href"])
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
    print(re_lst)
    print(len(re_lst))

    return re_lst


all_hrefs = {}
sids1 = [100, 101, 102, 103, 104, 105, 110, 120, 130]  # 정치,경제,사회,생활/문화,세계,IT/과학,오피니언,스포츠,연예
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
    if (sid1 == 100) or (sid1 == 101) or (sid1 == 102) or (sid1 == 103) or (sid1 == 104) or (sid1 == 105) or (
            sid1 == 110):
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
    # print(art_dic["date"])
    # print(art_dic["content"])

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

    cols = ['title', 'date', 'content', 'section1', 'section2', 'url']

    with open("news2.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writeheader()
        writer.writerows(artdic_lst)

    # CSV 파일 가져오기
    csv_object = s3.Object(bucket_name, object_name)
    csv_content = csv_object.get()['Body'].read().decode('utf-8')

    # CSV 파일 수정하기
    output = io.StringIO()
    cols = ['title', 'date', 'content', 'section', 'url']

    writer = csv.DictWriter(output, fieldnames=cols)
    writer.writeheader()

    for row in artdic_lst:
        writer.writerow(row)

    # 수정된 CSV 파일 가져오기
    csv_content += output.getvalue()

    # 수정된 CSV 파일 S3에 업로드
    csv_object.put(Body=csv_content)


def realTime_crawl():
    while True:
        collect_data()
        time.sleep(60)  # 60초 간격 크롤링

realTime_crawl()
