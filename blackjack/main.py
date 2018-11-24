from flask import Flask, request
import requests
import json
import slackweb
import time
import copy
import numpy as np
from blackjack.card import num2symbol
from blackjack.deck import Deck
from blackjack.player import Player 
from blackjack.dealer import Dealer

class STATUS:
    WAITING = 0
    PLAYER_TURN =1


app = Flask(__name__)
mattermost = slackweb.Slack(url="http://192.168.11.10:8065/hooks/yyejzfdg6bdsxpkzb5k166pjmy")

status = STATUS.WAITING

# カードとプレイヤー、ディーラーを用意する
# とりあえずグローバル変数にしちゃったという突貫工事
deck = Deck()
player = Player()
dealer = Dealer()

@app.route('/')
def welcome():
    html = '<html><title>welcome</title>'
    html = html + '<body>This is a BLACLJACK Server</body></html>'
    return html


@app.route('/matter', methods=['POST'])
def post():
    global status, deck, player, dealer
    data = request.json
    text = data['text']

    agent, text = get_called_agent_and_message(text)

    if agent.find('blackjack') < 0 and agent.find('bj') < 0: 
        print("calling agent is invalid")
        return json.dumps(dict())

    if status == STATUS.WAITING:
        if text.find("start") >= 0:
            # 初期化
            deck.re_initialize()
            deck.shuffle()
            player.re_initialize()
            dealer.re_initialize()
            print("0th deck info:", len(deck.deck))

            player.first_action(deck)
            dealer.first_action(deck)

            mattermost.notify(text='カードをオープンします。')
            _dealer_message(deck, player, dealer, is_hide=True)
            mattermost.notify(text='ヒット("hit")かスタンド("stand")を選んでください。')

            status = STATUS.PLAYER_TURN
        else:
            mattermost.notify(text='ブラックジャックをプレイしたい場合は"start"を入力してください。')
            return json.dumps(dict())

    elif status == STATUS.PLAYER_TURN:
        if text.find('hit') >= 0:
            action = 'hit'
        elif text.find('stand') >= 0:
            action = 'stand'
        elif text.find('quit') >= 0:
            mattermost.notify(text='強制終了します。初期状態に戻ります。')
            return json.dumps(dict())
        else:
            mattermost.notify(text='無効な入力を検知しました。ヒット("hit")かスタンド("stand")を選んでください。ゲームを終了する場合は"quit"を入力してください。')
            return json.dumps(dict())

        if action == 'hit':
            score = player.hit(deck)
            if score <= 21:
                _dealer_message(deck, player, dealer, is_hide=True)
                mattermost.notify(text='ヒット("hit")かスタンド("stand")を選んでください。')
                return json.dumps(dict())
            else:
                _dealer_message(deck, player, dealer, is_hide=True)
                mattermost.notify(text='バーストしました。ディーラーのターンに移ります。')
                time.sleep(1)

        # この時点でスタンドかバーストになっているため、プレイヤーのターンは終わる
        for _, is_finish in dealer.second_action(deck):
            if is_finish:
                break
            else:
                _dealer_message(deck, player, dealer)

        _dealer_message(deck, player, dealer)

        player_score = player.get_score()
        dealer_score = dealer.get_score()
        player_value = player_score if player_score <= 21 else -1
        dealer_value = dealer_score if dealer_score <= 21 else -1
        if player_value > dealer_value:
            mattermost.notify(text='プレイヤーの勝利です。')
        elif player_value == dealer_value:
            mattermost.notify(text='引き分けです。')
        else:
            mattermost.notify(text='ディーラーの勝利です。')

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

def _dealer_message(_deck, _player, _dealer, is_hide=False,is_debug=True):
    deck = copy.deepcopy(_deck)
    player = copy.deepcopy(_player)
    dealer = copy.deepcopy(_dealer)

    _card_info = ":{}: **{}** "
    mattermost_text = "Player {} [Score is {}] vs Dealer {} [Score is {}]"
    mark2mark = {'H': 'heart', 'D': 'diamonds', 'C': 'clubs', 'S': 'spades'}

    print("@@@@@@@@@@@@@@")
    print("=== Player ===")
    player_text = ''
    for c in player.have_cards:
        player_text += _card_info.format(mark2mark[c.get_mark()], num2symbol(c.get_number()))
    player_score = player.get_score()
    print(player_text)
    print("player score:", player_score)
    print("*** Dealer ***")
    dealer_text = ''
    if is_hide:
        c = dealer.have_cards[0]
        dealer_text += _card_info.format(mark2mark[c.get_mark()], num2symbol(c.get_number()))
        dealer_text += _card_info.format('question', '?')
        dealer_score = dealer.get_score_only_first_one()
    else:
        for c in dealer.have_cards:
            dealer_text += _card_info.format(mark2mark[c.get_mark()], num2symbol(c.get_number()))
        dealer_score = dealer.get_score()
    print(dealer_text)
    print("dealer score:", dealer_score)

    time.sleep(1)
    mattermost.notify(text=mattermost_text.format(player_text, player_score, dealer_text, dealer_score))
    time.sleep(1)

    print("deck info:", len(deck.deck)) 
    print("@@@@@@@@@@@@@@@@@")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)
