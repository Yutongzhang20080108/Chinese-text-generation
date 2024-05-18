import json
from openai import OpenAI
import opencc
client = OpenAI(
    api_key="sk-9qxqayMe8D42SRZ3r4yb4SRjdF0Xd2FwUmavZUJZXSTC6VnJ",
    base_url="https://api.chatanywhere.tech/v1"
)


path = "new_dataset/poet.tang.10000.json"
def translation(text):
    converter = opencc.OpenCC('t2s.json')
    new_text = converter.convert(text)
    return new_text

with open(path, "r", encoding="utf-8") as f:
    train_data = json.load(f)
with open("new_dataset/train_data.json", "r", encoding="utf-8") as f:
    train_data_before = json.load(f)
title = []
paragraphs = []
for each in train_data:
    paragraph_now = ""
    title_now = translation(each["title"])
    title.append(title_now)
    for each in each["paragraphs"]:
        paragraph_now = paragraph_now+translation(each)
    paragraphs.append(paragraph_now)
#print(paragraphs[5])
rejected = []
template = "请你围绕{theme}这个题目写一首诗歌"
#print(rejected)
token_num = []
from nltk.probability import FreqDist
for each in paragraphs:
    fdist = FreqDist(each)
    all = fdist.N()
    token_num.append(all)
for i in range(1000):
    prompt = template.format(theme=title[i])
    response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "你是一个智能助手"},
    {"role": "user", "content": prompt}
  ],
  max_tokens=token_num[i]
)
    rejected_now = response.choices[0].message.content
    rejected_now = rejected_now.replace("\n", '')
    rejected.append(rejected_now)
print(rejected)
data = []
for i in range(1000):
    dict1 = {}
    dict1["instruction"]=template.format(theme=title[i])
    dict1["input"]=''
    dict1["chosen"]=paragraphs[i]
    dict1["rejected"]=rejected[i]
    data.append(dict1)
for each in train_data_before:
    data.append(each)
print(len(data))
with open("train_data_3000.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)