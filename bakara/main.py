from flask import Flask, request
import requests
import json
import slackweb
import copy
from bakara.deck import Deck
from bakara.player import Player 
from bakara.banker import Banker 

app = Flask(__name__)
mattermost = slackweb.Slack(url="http://192.168.11.10:8065/hooks/yyejzfdg6bdsxpkzb5k166pjmy")

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

    if text.find('player') >= 0 or text.find('Player') >= 0:
        bet = 'Player'
    elif text.find('banker') >= 0 or text.find('Banker') >= 0:
        bet = 'Banker'
    else:
        mattermost.notify(text='PlayerかBankerのどちらかを指定してください。英語の大文字小文字は問いません。')
        return json.dumps(dict())

    mattermost.notify(text='あなたは{}の勝利に賭けました。ゲームを始めます。'.format(bet))

    # カードとプレイヤー、バンカーを用意する
    deck = Deck()
    deck.shuffle()
    player = Player()
    banker = Banker()
    print("0th deck info:", len(deck.deck))

    # 1st round
    player.first_action(deck)
    banker.first_action(deck)
    _dealer_message(1, deck, player, banker)


    # 2nd round
    player.second_action(deck)
    banker.second_action(deck, player=player)
    _dealer_message(2, deck, player, banker)

    # show result
    player_score = player._get_score()
    banker_score = banker._get_score()
    if player_score > banker_score:
        res = 'Player'
        mattermost.notify(text='playerの勝利です。')
    elif player_score == banker_score:
        res = 'Tie'
        mattermost.notify(text='引き分けです。')
    else:
        res = 'Banker'
        mattermost.notify(text='bankerの勝利です。')

    if res == bet:
        mattermost.notify(text='あなたの予想は当たりました。勝利です。')
    else:
        mattermost.notify(text='あなたの予想は外れました。敗北です。')

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
        player_text += _card_info.format(mark2mark[c.get_mark()], c.get_number())
    print(player_text)
    print("player score:", player._get_score())
    print("*** Banker ***")
    banker_text = ''
    for c in banker.have_cards:
        banker_text += _card_info.format(mark2mark[c.get_mark()], c.get_number())
    print(banker_text)
    print("banker score:", banker._get_score())

    mattermost.notify(text='Player {}'.format(player_text))
    mattermost.notify(text='Banker {}'.format(banker_text))

    if round_number == 1:
        print("1st deck info:", len(deck.deck))
    else:
        print("2nd deck info:", len(deck.deck))
    
    print("@@@@@@@@@@@@@@@@@")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8888)
