from flask import Flask, request
import requests
import json
import slackweb
import time
import copy
import numpy as np
from bakara.card import num2symbol
from bakara.deck import Deck
from bakara.player import Player 
from bakara.banker import Banker 

class STATUS:
    WAITING = 0
    SELECTING =1


app = Flask(__name__)
mattermost = slackweb.Slack(url="http://192.168.11.10:8065/hooks/yyejzfdg6bdsxpkzb5k166pjmy")

status = STATUS.WAITING

with open("***.yaml", 'r') as f:
    images_dict = yaml.load(f)
members = list(images_dict.keys())

@app.route('/')
def welcome():
    html = '<html><title>welcome</title>'
    html = html + '<body>This is a BAKARA Server</body></html>'
    return html

# text input : "<you>hogehoge"
@app.route('/matter', methods=['POST'])
def post():
    data = request.json
    text = data['text']

    agent, text = get_called_agent_and_message(text)

    if agent.find('<bakara>') < 0:
        print("calling agent is invalid")
        return json.dumps(dict())

    if status == STATUS.WAITING:
        if text.find("start") >= 0:
            player_name, banker_name = np.random.choice(members, 2, replace=False)

            player_attachments = [{
                "text": "Playerは {} です。".format(player_name),
                "image_url": images_dict[player_name]
                }]
            mattermost.notify(attachments=player_attachments)

            banker_attachments = [{
                "text": "Bankerは {} です。".format(banker_name),
                "image_url": images_dict[banker_name]
                }]
            mattermost.notify(attachments=banker_attachments)

            mattermost.notify(text='彼女たちがあなたの応援を必要としています。PlayerとBankerのどちらが勝つか予測してください。英語の大文字小文字は問いません。')

            status = STATUS.SELECTING
        else:
            mattermost.notify(text='バカラをプレイしたい場合は start を入力してください。')
            return json.dumps(dict())

    elif status == STATUS.SELECTING:
        if text.find('player') >= 0 or text.find('Player') >= 0:
            bet = 'Player'
        elif text.find('banker') >= 0 or text.find('Banker') >= 0:
            bet = 'Banker'
        else:
            mattermost.notify(text='無効な入力を検知しました。初期状態に戻ります。')
            return json.dumps(dict())

        mattermost.notify(text='あなたは{}の勝利に賭けました。ゲームを始めます。'.format(bet))

        # カードとプレイヤー、バンカーを用意する
        deck = Deck()
        deck.shuffle()
        player = Player()
        banker = Banker()
        print("0th deck info:", len(deck.deck))

        # 1st round
        mattermost.notify(text='1st roundに入ります。カードをオープンします。')
        player.first_action(deck)
        banker.first_action(deck)
        _dealer_message(1, deck, player, banker)


        # 2nd round
        mattermost.notify(text='2nd roundに入ります。PlayerおよびBankerのスコアに応じてカードがオープンされるかどうかが変わります。')
        player.second_action(deck)
        banker.second_action(deck, player=player)
        _dealer_message(2, deck, player, banker)

        # show result
        player_score = player._get_score()
        banker_score = banker._get_score()
        if player_score > banker_score:
            res = 'Player'
            mattermost.notify(text='Playerの勝利です。')
        elif player_score == banker_score:
            res = 'Tie'
            mattermost.notify(text='引き分けです。')
        else:
            res = 'Banker'
            mattermost.notify(text='Bankerの勝利です。')

        if res == bet:
            mattermost.notify(text='おめでとうございます。あなたの予想は当たりました。勝利です。')
        else:
            mattermost.notify(text='残念でした。あなたの予想は外れました。敗北です。')

        status = STATUS.WAITING
    else:
        raise ValueError("invalid status")

    return json.dumps(dict())


def get_called_agent_and_message(text):
    index_1 = text.find('<')
    index_2 = text.find('>')
    if index_1 < 0 or index_2 < 0:
        raise ValueError("text is invalid")

    agent = text[(index_1 + 1):index_2]
    message = text[(index_2 + 1):]

    return agent, message

def _dealer_message(round_number, _deck, _player, _banker, is_debug=True):
    deck = copy.deepcopy(_deck)
    player = copy.deepcopy(_player)
    banker = copy.deepcopy(_banker)

    _card_info = ":{}: **{}** "
    mark2mark = {'H': 'heart', 'D': 'diamonds', 'C': 'clubs', 'S': 'spades'}

    if round_number == 1:
        print("@@@ 1st round @@@")
    elif round_number == 2:
        print("@@@ 2nd round @@@")
    else:
        raise ValueError()

    print("=== Player ===")
    player_text = ''
    for c in player.have_cards:
        player_text += _card_info.format(mark2mark[c.get_mark()], num2symbol(c.get_number()))
    print(player_text)
    print("player score:", player._get_score())
    print("*** Banker ***")
    banker_text = ''
    for c in banker.have_cards:
        banker_text += _card_info.format(mark2mark[c.get_mark()], num2symbol(c.get_number()))
    print(banker_text)
    print("banker score:", banker._get_score())

    mattermost.notify(text='Player {} : スコアは {} です。'.format(player_text, player._get_score()))
    mattermost.notify(text='Banker {} : スコアは {} です。'.format(banker_text, banker._get_score()))

    if round_number == 1:
        print("1st deck info:", len(deck.deck))
    else:
        print("2nd deck info:", len(deck.deck))
    
    print("@@@@@@@@@@@@@@@@@")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)
