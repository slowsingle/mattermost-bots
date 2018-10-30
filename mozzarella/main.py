from flask import Flask, request
import requests
import json
import slackweb
import copy
import random

# コメントアウトがとても頭が弱い感じです。

app = Flask(__name__)
mattermost = slackweb.Slack(url="http://localhost:8065/hooks/yyejzfdg6bdsxpkzb5k166pjmy")

@app.route('/')
def welcome():
    html = '<html><title>welcome</title>'
    html = html + '<body>Moooooooooooozzarrrrrrrrrrrellaaaaaa</body></html>'
    return html

# text input : "<you>hogehoge"
@app.route('/matter', methods=['POST'])
def post():
    data = request.json
    text = data['text']

    agent, mozzarella = get_called_agent_and_message(text)
    print('debug:', agent, mozzarella)

    splited_mozzarella = split_mozzarella(mozzarella)
    print('debug:', splited_mozzarella)

    new_mozzarella = add_hogehoge(splited_mozzarella)
    print('debug:', new_mozzarella)

    new_text = ''.join(new_mozzarella)

    if len(new_text) < 30:
        attachments = [{"text": '### ' + new_text, "image_url": "https://i.imgur.com/jfe9foM.jpg"}]
    elif len(new_text) < 50:
        attachments = [{"text": '## ' + new_text, "image_url": "https://i.imgur.com/YJ9kY2F.png"}]
    elif len(new_text) < 75:
        attachments = [{"text": '# ' + new_text, "image_url": "https://i.imgur.com/6snXP9M.jpg"}]
    else:
        special_text = "いつまでやってるの？"
        attachments = [{"text": '#### ' + special_text, "image_url": "https://i.imgur.com/kyjW6W3.jpg"}]

    #mattermost.notify(text=text)
    mattermost.notify(attachments=attachments)

    return json.dumps(dict())


def get_called_agent_and_message(text):
    index_1 = text.find('<')
    index_2 = text.find('>')
    if index_1 < 0 or index_2 < 0:
        raise ValueError("text is invalid")

    agent = text[(index_1 + 1):index_2]
    message = text[(index_2 + 1):]

    return agent, message


'''
 input: ["モ", "ッッッッッッ", "ツ", "ア", "レ", "ラ", "チ", "ーーーーーー", "ズ", "！！！！"]
output: ["モ", "ッッッッッッッッ", "ツ", "アア", "レ", "ラ", "チ", "ーーーーーーーー", "ズ", "！！！！！！"]
'''
def add_hogehoge(splited_mozzarella):
    new_mozzarella = copy.deepcopy(splited_mozzarella)
    for i, elem in enumerate(splited_mozzarella):
        moji = elem[0]
        if moji in ["ァ", "ィ", "ェ","ッ", "ア", "イ", "エ", "ー", "!", "！"]:
            moji = elem[0]
            n_add = random.choice(range(1, 5))
            new_mozzarella[i] += (moji * n_add)

    return new_mozzarella


'''
 input: "モッッッッッッツアレラチーーーーーーズ！！！！"
output: ["モ", "ッッッッッッ", "ツ", "ア", "レ", "ラ", "チ", "ーーーーーー", "ズ", "！！！！"]
'''
def split_mozzarella(word):
    splited = list()
    last_i = -1
    for w in word:
        if last_i == -1 or splited[last_i][0] != w:
            splited.append(w)
            last_i += 1
        else:
            splited[last_i] += w

    return splited


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)