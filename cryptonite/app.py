from gevent import monkey; monkey.patch_all()
from flask import Flask, render_template, Response, request, stream_with_context, url_for
from gevent.pywsgi import WSGIServer
from pycoingecko import CoinGeckoAPI
from flask_mail import Mail, Message
from flask_sse import sse
import time
import json


app = Flask(__name__)
cg = CoinGeckoAPI()


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "testdummyofthehood@gmail.com"
app.config['MAIL_PASSWORD'] = "thisaccountisatest"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)

miner = 'scripts/miner.js'
logo = 'logo.png'
currency = "cad"
xValues = [];
yValues = [];


def create_list(range):
    month = 0
    list = []
    length = range(range)

    for i in length:
        list.append(month)
        month += 1;

    return list


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/staking", methods = ['POST', 'GET'])
def staking():
    return render_template('staking.html')

    if request.method == 'POST':
        return redirect(url_for('/staking/graph'))


@app.route('/staking/graph', methods = ['POST', 'GET'])
def graph():

    interest = request.form['interest']
    months =  request.form['months']
    inflation = request.form['inflation']
    burn = request.form['burn']
    compound = request.form['compound']
    ticker = f"{request.form['ticker']}"
    amount = request.form['amount']

    return render_template('graphic.html', interest=interest, months=months, inflation=inflation, burn=burn, compound=compound, ticker=ticker, amount=amount)



@app.route("/mining", methods = ['POST', 'GET'])
def mining():
    return render_template('mining.html')

    if request.method == 'POST':
        return redirect(url_for('/mining/profit'))


@app.route('/mining/profit', methods = ['POST', 'GET'])
def profit():

    hash = request.form['hash']
    days = request.form['days']
    watts = request.form['watts']
    cost = request.form['cost']
    fee = request.form['fee']
    present_price = request.form['present_price']


    chosen = f"{request.form['chosen_crypto']}"

    if chosen == 'BTC':
        network_rate = 138000000000
        block_time = 658
        currency_name = 'BTC'
        block_reward = 6.25

    if chosen == 'ETH':
        network_rate = 609000
        block_time = 13.4
        currency_name = 'ETH'
        block_reward = 2.26

    if chosen == 'LTC':
        network_rate = 315000
        block_time = 164
        currency_name = 'LTC'
        block_reward = 12.5

    if chosen == 'XMR':
        network_rate = 2.4
        block_time = 120
        currency_name = 'XMR'
        block_reward = 1.09

    if chosen == 'DOGE':
        network_rate = 304000
        block_time = 1
        currency_name = 'DOGE'
        block_reward = 10000

    if chosen == 'BCH':
        network_rate = 2750000000
        block_time = 10
        currency_name = 'BCH'
        block_reward = 6.26

    return render_template('profit.html', hash=hash, days=days, watts=watts, cost=cost, network_rate=network_rate, block_time=block_time, currency_name=currency_name, block_reward=block_reward, present_price=present_price, fee=fee)






@app.route("/contact", methods = ['POST', 'GET'])
def contact():
    return render_template('contact.html')

    if request.method == 'POST':
        return redirect(url_for('/contact/send_form'))


@app.route('/contact/send_form', methods = ['POST', 'GET'])
def send_form():


    first_name = request.form['fname']
    last_name = request.form['lname']
    email = request.form['email']
    subject = request.form['subject']
    content = request.form['message']
    return render_template('send_form.html', first_name=first_name)


    msg = f'First name: {first_name}, Last name: {last_name}, Email: {email}, Subject: {subject}'
    message = Message("Krypto kollateral", sender="testdummyofthehood@gmail.com", recipients=["lemyted21@gmail.com"])
    message.body = msg
    mail.send(message)



counter = 100
btc = 0; btc_price = 0; btc_change_24 = 0; btc_change_7 = 0; btc_color_24 = 0; btc_color_7 = 0
eth = 0; eth_price = 0; eth_change_24 = 0; eth_change_7 = 0; eth_color_24 = 0; eth_color_7 = 0
rank_list = 0; rank_one = 0; rank_two = 0; rank_three = 0; rank_four = 0; rank_five = 0; rank_six = 0; rank_seven = 0; rank_eigth = 0; rank_nine = 0; rank_ten = 0


def get_color(change):
    string = f"{change}"

    if '-' in string:
        return '#ff4d4d'

    elif '-' not in string:
        return '#4dff4d'


def get_ranking():
    list1 = []
    list2 = []
    list3 = []

    list1 = f"{cg.get_coins_markets(vs_currency=currency)}".split('symbol')

    for i in list1:
        list2 = i[0:50].split(": ")
        for j in list2:
            j = j.split(",")
            if "http" not in j[0] and j[0] != "'" and "1" not in j[0]:
                list3.append(j[0].replace("'", ""))
    return list3[2:22]


@app.route("/listen")
def listen():

    def respond_to_client():
        while True:
            global counter
            global btc, eth, btc_price,btc_change_24, btc_change_7, btc_color_24, btc_color_7
            global eth_change_24, eth_change_7, eth_color_24, eth_color_7
            global rank_one, rank_two, rank_three, rank_four, rank_five, rank_six, rank_seven, rank_eigth, rank_nine, rank_ten

            if True:
                counter += 1
                btc = f"{cg.get_coins_markets(ids='bitcoin', vs_currency=currency, price_change_percentage='24h,7d')}"
                eth = f"{cg.get_coins_markets(ids='ethereum', vs_currency=currency, price_change_percentage='24h,7d')}"
                btc = btc.split(", '")

                btc_price = f"{btc[4][16:]} {currency.upper()}$"
                btc_change_24 = f"{btc[-2][41:48]} %"
                btc_change_7 = f"{btc[-1][41:48]} %"
                btc_color_24 = get_color(btc_change_24)
                btc_color_7 = get_color(btc_change_7)

                eth = eth.split(", '")
                eth_price = f"{eth[4][16:]} {currency.upper()}$"
                eth_change_24 = f"{eth[-2][41:48]} %"
                eth_change_7 = f"{eth[-1][41:48]} %"
                eth_color_24 = get_color(eth_change_24)
                eth_color_7 = get_color(eth_change_7)

                rank_list= get_ranking()
                rank_one = f"1. {rank_list[1]}"
                rank_two = f"2. {rank_list[3]}"
                rank_three = f"3. {rank_list[5]}"
                rank_four = f"4. {rank_list[7]}"
                rank_five = f"5. {rank_list[9]}"
                rank_six = f"6. {rank_list[11]}"
                rank_seven = f"7. {rank_list[13]}"
                rank_eigth = f"8. {rank_list[15]}"
                rank_nine = f"9. {rank_list[17]}"
                rank_ten = f"10. {rank_list[19]}"

                _data = json.dumps({
                "counter":counter,
                "btc_price":btc_price,"btc_change_24":btc_change_24,
                "btc_change_7":btc_change_7,"btc_color_24":btc_color_24,
                "btc_color_7":btc_color_7,"eth_price":eth_price,
                "eth_change_24":eth_change_24,"eth_change_7":eth_change_7,
                "eth_color_24":eth_color_24,"eth_color_7":eth_color_7,
                "rank_one":rank_one, "rank_two":rank_two,
                "rank_three":rank_three, "rank_four":rank_four,
                "rank_five":rank_five, "rank_six":rank_six,
                "rank_seven":rank_seven, "rank_eigth":rank_eigth,
                "rank_nine":rank_nine, "rank_ten":rank_ten
                })

                yield f"id: 1\ndata: {_data}\nevent: online\n\n"
            time.sleep(120)
    return Response(respond_to_client(), mimetype='text/event-stream')


if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=5000, debug=True)
    http_server = WSGIServer(("localhost", 5000), app)
    http_server.serve_forever()


#put css in different file
#enable send
#enable sse
#debug off
