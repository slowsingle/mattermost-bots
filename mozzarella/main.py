from flask import Flask, request
import requests
import json
import slackweb
import copy
import random

# コメントアウトがとても頭が弱い感じです。

app = Flask(__name__)
mattermost = slackweb.Slack(url="http://192.168.11.10:8065/hooks/yyejzfdg6bdsxpkzb5k166pjmy")

@app.route('/')
def welcome():
    html = '<html><title>welcome</title>'
    html = html + '<body>Moooooooooooozzarrrrrrrrrrrellaaaaaa</body></html>'
    return html

@app.route('/matter', methods=['POST'])
def post():
    print('debug:', 'OK')
    data = request.json
    text = data['text']

    _, mozzarella = text.split(' ')
    print('debug:', mozzarella)

    splited_mozzarella = split_mozzarella(mozzarella)
    print('debug:', splited_mozzarella)

    new_mozzarella = add_hogehoge(splited_mozzarella)
    print('debug:', new_mozzarella)

    text = ''.join(new_mozzarella)

    mattermost.notify(text=text)

    return json.dumps(dict())


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

    