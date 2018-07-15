import flask
import requests
from datetime import datetime
app = flask.Flask(__name__)

def mcafee():
    coin_json=requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
    if coin_json.status_code!=200:
        return {'s':'e','c':coin_json.json()}
    bpi = coin_json.json()['USD']
    tbpi = 2244.265
    grate = 0.7826319559
    days_elapsed = (datetime.now()-datetime.strptime('07 17 17','%m %d %y')).days
    days_left = (datetime.strptime('12 31 20','%m %d %y')-datetime.now()).days
    pprice = 10**(grate*(days_elapsed/365))*tbpi
    pdiff = ((bpi-pprice)/pprice)*100
    if pdiff in range(0,10):
        isdickonthemenu = "Maybe?"
    elif pdiff>10:
        isdickonthemenu = "No!"
    else:
        isdickonthemenu = "Yes!"
    pprice = float("%.2f" % pprice)
    pdiff = float("%.2f" % pdiff)
    return {
        's':'s',
        'c':{
            'isdickonthemenu':isdickonthemenu,
            'current_price':bpi,
            'tweet_price':tbpi,
            'goal_rate':grate,
            'days_elapsed':days_elapsed,
            'days_remaining':days_left,
            'parity_price':pprice,
            'difference_percent':pdiff,
            'info':{
                'docs':'https://will-mcafee-eat-his-own-dick.herokuapp.com/help',
                'github':'https://github.com/marios8543/will-mcafee-eat-his-own-dick'
            }
        }
    }

@app.route('/')
def index():
    res = mcafee()
    if res['s']=='e':
        return flask.make_response(flask.jsonify({'code':500,'error':'cryptocompare error','content':res['c']}))
    else:
        return flask.make_response(flask.jsonify(res['c']),200)

@app.route('/help')
def help():
    return flask.render_template('help.html',url=app.static_url_path,example=mcafee()['c'])

if __name__=='__main__':
    app.run(debug=True)     