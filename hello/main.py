from flask import Flask, request
import requests
import json
import slackweb

app = Flask(__name__)
mattermost = slackweb.Slack(url="")

@app.route('/')
def welcome():
    html = '<html><title>welcome</title>'
    html = html + '<body>welcome</body></html>'
    return html

@app.route('/matter', methods=['POST'])
def post():
    data = request.json
    print(data)
    text = 'you said ' + incomeText + ' by your first machine.'

    mattermost.notify(text=text)

    return json.dumps(dict())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5353)