import chardet
import requests
import json
import pandas as pd
import openai
import time

#요약문(3줄) 추출
class SummaryBot:
    # 요약 api 실행을 위한 세팅
    def __init__(self, client_id, client_secret, input_file, output_file, url='https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-APIGW-API-KEY-ID': client_id,
            'X-NCP-APIGW-API-KEY': client_secret
        }
        self.input_file = input_file
        self.output_file = output_file

    # csv 파일 읽기


    # 요약
    def summarize(self, df):
        for index, row in df.iterrows():
            content = row["content"]
            if pd.isna(row['summary']):
                data = {
                    "document": {
                        "content": content
                    },
                    "option": {
                        "language": "ko",
                        "model": "news",
                        "tone": 3,   # 말투 0: 했다. 1: 했어요. 2: 했습니다. 3: 함
                        "summaryCount": 3
                    }
                }

                response = requests.post(self.url, headers=self.headers, data=json.dumps(data).encode('UTF-8'))
                rescode = response.status_code

                if rescode == 200:
                    response_data = json.loads(response.text)
                    summary = response_data['summary']
                else:
                    summary = "Error : " + response.text

                df.at[index, 'summary'] = summary
        return df




class ChatGPT():
    def __init__(self, summary_content):
        self.content = f"Content: {summary_content}"

    def run_gpt(self, questions):
        MAX_RETRIES = 3
        RETRY_DELAY = 10  # in seconds

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
                        temperature=0.8  # 원하는 temperature 값으로 설정 (기본값은 0.8)
                    )
                    break  # if successful, break out of the loop
                except openai.error.Timeout:
                    if attempt < MAX_RETRIES - 1:  # Don't sleep on the last attempt
                        time.sleep(RETRY_DELAY)
                    else:
                        raise  # re-raise the last exception if all retries fail

            answer = response['choices'][0]['message']['content']
            return answer

    def detect_encoding(self, file_path):
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
            return result['encoding']

    # key(핵심 사건)


    def extract_key(self, df):
        # Iterate through the rows of the DataFrame
        for index, row in df.iterrows():
            # 정상 실행을 위한 전처리(error/ blank 있는 row 제거)
            indices_to_drop = df[
                df['summary'].str.strip().str.startswith('Error', na=False) |
                (df['summary'].str.strip() == '')
                ].index
            df = df.drop(indices_to_drop)
            if pd.notna(row['summary']) and pd.isna(row['key']):
                # Get the summary to send to the chatbot
                summary = row['summary']

                # Create ChatGPT instance and run the GPT method
                chat_bot_instance = ChatGPT(summary)  # Change here, pass the summary content directly
                key_question = ["이 기사는 어떤 사건에 대한 거야? 한국어 단답형 명사로 끝나도록 답해줘. 최대한 짧게."]
                answer = chat_bot_instance.run_gpt(key_question)

                # Write the answer back to the 'key' column
                df.at[index, 'key'] = answer
        return df


def read_csv(input_file):
    with open(input_file, 'rb') as file:
        result = chardet.detect(file.read())
        encoding = result['encoding']
    return pd.read_csv(input_file, encoding=encoding)

def write_csv(df, output_file, encoding='utf-8'):
    with open(output_file, 'w', encoding=encoding, newline='') as file:
        df.to_csv(file, index=False)

# 실행 함수
def run_nlp(input_file, output_file):
    df = read_csv(input_file)
    summary_bot = SummaryBot(client_id='YOUR_CLIENT_ID',
                             client_secret='YOUR_CLIENT_SECRET',
                             input_file=input_file,
                             output_file=output_file)
    updated_sum = summary_bot.summarize(df)
    write_csv(updated_sum, output_file, encoding='utf-8')
    print('Summary Update Complete!')
    chat_gpt = ChatGPT(summary_content="")
    updated_key = chat_gpt.extract_key(df)   # key 추출
    write_csv(updated_key, output_file, encoding=chat_gpt.detect_encoding(input_file))  # df 쓰기
    print('Key Update Complete!')
    return updated_key


# --Naver CLOVA api key
client_id = 'aq7l2kiodi'
client_secret = '6h9XijGxdTxbcI3owFDVLwYtaJ0yk4dmbgRadLnK'

# --chatGPT api key
openai.api_key='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'
openai.Timeout = 60 * 10  # 10분으로 timeout 설정(너무 짧으면 에러 발생)

# --file path
input_file = 'newkey.csv'
output_file = 'newkey.csv'

# 실행
run_nlp(input_file, output_file)