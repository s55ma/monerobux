#romerito -*- coding: UTF-8 -*-
import sopel.module
import requests
import time
import random

polourl = "https://poloniex.com/public?command=returnTicker"
poloxmrlendurl = "https://poloniex.com/public?command=returnLoanOrders&currency=XMR&limit=999999"
polobtclendurl = "https://poloniex.com/public?command=returnLoanOrders&currency=BTC&limit=999999"
prevamnt, prevtime = 0, 0
trexurl = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-"
cryptopiaurl = "https://www.cryptopia.co.nz/api/GetMarkets"
bitsquareurl = "https://market.bitsquare.io/api/ticker/?market=xmr_btc"
fixerurl = 'http://api.fixer.io/latest?base=USD'
finexbtc = 'https://api.bitfinex.com/v1/pubticker/XMRBTC'
finexusd = 'https://api.bitfinex.com/v1/pubticker/XMRUSD'
krakbtc = 'https://api.kraken.com/0/public/Ticker?pair=XMRXBT'
krakbtceur = 'https://api.kraken.com/0/public/Ticker?pair=XBTEUR'
krakusd = 'https://api.kraken.com/0/public/Ticker?pair=XMRUSD'
krakeur = 'https://api.kraken.com/0/public/Ticker?pair=XMREUR'
okcquar = 'https://www.okcoin.com/api/v1/future_ticker.do?symbol=btc_usd&contract_type=quarter'
krakusdt = 'http://api.kraken.com/0/public/Ticker?pair=USDTUSD'

@sopel.module.commands('bfx', 'bitfinex')
def bfx(bot, trigger):
    stringtosay = ''
    try:
        r = requests.get(finexbtc)
        j = r.json()
        stringtosay += "Last XMR/BTC trade at {0:.6f} on {1:.2f} 24 h XMR volume. ".format(float(j['last_price']), float(j['volume']))
    except:
        bot.say("Error getting XMR/BTC data")
    try:
        r = requests.get(finexusd)
        j = r.json()
        stringtosay += "Last XMR/USD trade at {0:.2f} on {1:.2f} 24 h XMR volume.".format(float(j['last_price']), float(j['volume']))
    except:
        bot.say("Error getting XMR/USD data")
    try:
        bot.say(stringtosay)
    except:
        bot.say("Error getting data")

@sopel.module.commands('krak', 'kraken')
def krak(bot, trigger):
    stringtosay = ''
    try:
        r = requests.get(krakbtc)
        j = r.json()
        stringtosay += "Last XMR/BTC trade at {0:.6f} on {1:.2f} 24 h XMR volume. ".format(float(j['result']['XXMRXXBT']['c'][0]), float(j['result']['XXMRXXBT']['v'][1]))
    except:
        bot.say("Error getting XMR/BTC data")
    try:
        r = requests.get(krakusd)
        j = r.json()
        stringtosay += "Last XMR/USD trade at {0:.2f} on {1:.2f} 24 h XMR volume. ".format(float(j['result']['XXMRZUSD']['c'][0]), float(j['result']['XXMRZUSD']['v'][1]))
    except:
        bot.say("Error getting XMR/USD data")
    try:
        r = requests.get('https://api.kraken.com/0/public/Ticker?pair=XMREUR')
        j = r.json()
        stringtosay += "Last XMR/EUR trade at {0:.2f} on {1:.2f} 24 h XMR volume. ".format(float(j['result']['XXMRZEUR']['c'][0]), float(j['result']['XXMRZEUR']['v'][1]))
    except:
        bot.say("Error getting XMR/EUR data")
    try:
        bot.say(stringtosay)
    except:
        bot.say("Error getting data")

@sopel.module.commands('usdt')
def usdt(bot, trigger):
    try:
        r = requests.get(krakusdt)
        j = r.json()
        stringtosay = "Last USDT/USD trade at ${0:.4f} on {1:.2f} USD 24 h volume. Highest bid at ${2:.4f}".format(float(j['result']['USDTZUSD']['c'][0]), float(j['result']['USDTZUSD']['v'][0]), float(j['result']['USDTZUSD']['b'][0]))
        bot.say(stringtosay)
    except:
        bot.say("Error getting USDT/USD data")

@sopel.module.commands('btckrak', 'btckraken', 'btceur')
def krakeur(bot, trigger):
    stringtosay = ''
    try:
        r = requests.get(krakbtceur)
        j = r.json()
        stringtosay += "Last BTC/EUR trade at €{0:.2f} on {1:.2f} BTC 24 h volume. ".format(float(j['result']['XXBTZEUR']['c'][0]), float(j['result']['XXBTZEUR']['v'][0]))
    except:
        bot.say("Error getting BTC/EUR data")
    try:
        bot.say(stringtosay)
    except:
        bot.say("Error getting data")

@sopel.module.commands('chart')
def chart(bot, trigger):
    bot.say('https://cryptowat.ch/poloniex/xmrbtc')

@sopel.module.commands('polo', 'poloniex', 'marco')
@sopel.module.interval(3600)
def polo(bot, trigger):
    if not trigger.group(2): 
        try:
            r=requests.get(polourl)
            j=r.json()
            xmr=j["BTC_XMR"]
            last=float(xmr['last'])
            change=float(xmr['percentChange'])
            vol=float(xmr['baseVolume'])
            if change >= 0: 
                sign = '+'
            else:
                sign = ''
            face = ''
            if change > 0.10:
                face = u'\u263d'.encode('utf8')
            if 0.10 >= change > 0.05:
                face = u'\u2661'.encode('utf8')
            if 0.05 >= change > 0.02:
                face = u'\u263a'.encode('utf8')
            if 0.02 >= change > -0.02:
                face = u'\u2694'.encode('utf8')
            if -0.02 >= change > -0.05:
                face = u'\u2639'.encode('utf8')
            if -0.05 >= change > -0.1:
                face = u'\u2620'.encode('utf8')
            if change < -0.1: 
                face = u'\u262d'.encode('utf8')
            bot.say("Poloniex at {0:.8f} BTC; {1}{2:.2f}% over 24 hours on {3:.3f} BTC volume {4}".format(last, sign, change*100, vol, face))
        except:
            bot.say("Error retrieving data from Poloniex")
    else:
        coin = trigger.group(2).upper()
        try:
            r=requests.get(polourl)
            j=r.json()
        except:
            bot.say("Error connecting to Poloniex")
        if len(coin) > 5 or len(coin) < 2:
            bot.say("Coin ticker is too long or short")
        # elif coin == "PASC":
        #     bot.say("COBOL only in #monero-markets")
        # elif coin == "NAUT":
        #     bot.say("That ship has sailed...")
        elif coin == "PIVX":
            bot.say("Masternodes + PoS...what could possibly go wrong?")
        else:
            label="BTC_" + coin
            try:
                ticker=j[label]
                last=float(ticker['last'])
                change=float(ticker['percentChange'])
                vol=float(ticker['baseVolume'])
                if change >= 0: 
                    sign = '+'
                else:
                    sign = ''
                bot.say("{0} at {1:.8f} BTC; {2}{3:.2f}% over 24 hours on {4:.3f} BTC volume".format(coin, last, sign, change*100, vol))
            except:
                bot.say("ERROR!")

@sopel.module.commands('lending')
def lending(bot, trigger):
    try:
        r=requests.get(poloxmrlendurl) 
        j=r.json()
        amnt=0
        currenttime=time.time()
        for i in j['offers']:
            amnt+=float(i['amount'])
        bot.say("Total amount of XMR available {0:,.2f}. Changed by {1:.2f} in the last {2:.2f} hours".format(amnt, amnt-prevamnt, (currenttime-prevtime)/3600))
        global prevamnt
        prevamnt=amnt
        global prevtime
        prevtime=currenttime
    except:
        bot.say("Something bad happened :o")
    

@sopel.module.commands('trex', 'bittrex')
def trex(bot, trigger):
    if not trigger.group(2):
         geturl = trexurl+'xmr'
    else: 
        geturl = trexurl + trigger.group(2)
    try:
        r = requests.get(geturl)
        j = r.json()
        xmr=j['result'][0]
        last=float(xmr['Last'])
        change=((last/float(xmr['PrevDay']))-1)
        vol=float(xmr['BaseVolume'])
        bot.say("Bittrex at {0:.8f} BTC; {1:.2f}% over 24 hours on {2:.3f} BTC volume".format(last, change*100, vol))
    except:
        bot.say("Error retrieving data from Bittrex")

@sopel.module.commands('bsq', 'bitsquare')
def bsq(bot, trigger):
    try:
        r = requests.get(bitsquareurl)
        j = r.json()
        xmr=j['xmr_btc']
        last=float(xmr['last'])
        vol=float(xmr['volume_right'])
        bot.say("Bitsquare at {0:.8f} BTC on {1:.3f} BTC volume".format(last, vol))
    except:
        bot.say("Error retrieving data from Bitsquare")

@sopel.module.commands('cryptopia')
def cryptopia(bot, trigger):
    try:
        if not trigger.group(2):
             coin = 'XMR'
             pair = 'BTC'
        else: 
            coin = trigger.group(2).split(' ')[0].upper()
            try:
                if len(trigger.group(2).split(' ')[1]) > 1:
                    pair = trigger.group(2).split(' ')[1].upper()
                else:
                    pair = "BTC"
            except:
                pair = "BTC"
        r = requests.get(cryptopiaurl)
        j = r.json()
        found = False
        for i in j["Data"]:
            if i["Label"] == coin+"/"+pair:
                last=float(i['LastPrice'])
                change=float(i['Change'])
                vol=float(i['Volume'])
                bot.say("{0} on Cryptopia at {1:.8f} {2}; {3:.2f}% over 24 hours on {4:.3f} {2} volume".format(coin, last, pair, change, vol*last))
                found = True
        if found == False:
            bot.say("This shit is too shitty even for shitopia")
    except:
        bot.say("Error retrieving data from Cryptopia")

@sopel.module.commands('cmc', 'coinmarketcap')
def cmc(bot, trigger):
    try:
        r = requests.get('https://api.coinmarketcap.com/v1/ticker?limit=500')
        j = r.json()
    except:
        bot.say("Can't connect to API")
    if not trigger.group(2):
        symbol = 'XMR'
    else:
        if trigger.group(2).isdigit():
            rank = trigger.group(2)
        elif trigger.group(2) == 'random':
            rank = random.randint(1,500)
        else:
            symbol = trigger.group(2)
            symbol = symbol.upper()
    try:
        for i in j:
            try:
                if i['symbol'] == symbol:
                    coin = i
            except: pass
            try:
                if i['rank'] == str(rank):
                    coin = i
            except: pass
        symbol = coin['symbol']    
        name = coin['name']
        rank = coin['rank']
        price_usd = float(coin['price_usd'])
        price_btc = float(coin['price_btc'])
        volume_usd = float(coin['24h_volume_usd'])
        market_cap_usd = float(coin['market_cap_usd'])
        available_supply = float(coin['available_supply'])
        total_supply = float(coin['total_supply'])
        percent_change_24h = float(coin['percent_change_24h'])
        bot.say("{0} ({1}) is #{2}. Last price ${3:.2f} / ฿{4:.8f}. 24h volume ${5:,.0f} changed {6}%. Market cap ${7:,.0f}. Available / total coin supply {8:,.0f} / {9:,.0f}.".format(name, symbol, rank, price_usd, price_btc, volume_usd, percent_change_24h, market_cap_usd, available_supply, total_supply)) 
    except:
        bot.say("Error parsing ticker")

@sopel.module.commands('okc', 'okcoin')
def okc(bot, trigger):
    try:
        r = requests.get(okcquar)
        j = r.json()
        xmr=j['ticker']
        last=float(xmr['last'])
        vol=float(xmr['vol'])
        bot.say("OKcoin quarterly futures at ${0:.2f} on {1:.0f} volume".format(last, vol))
    except:
        bot.say("Error retrieving data from OKCoin")

@sopel.module.commands('tux')
def tux(bot, trigger):
    try:
        r = requests.get('https://tuxexchange.com/api?method=getticker')
        j = r.json()
        if not trigger.group(2):
            ticker='XMR'
        else:
            ticker=trigger.group(2).upper()
        coin=j['BTC_{}'.format(ticker)]
        last=float(coin['last'])
        vol=float(coin['baseVolume'])
        change=float(coin['percentChange'])
        bot.say("{0} at {1:.8f} BTC on {2:.3f} BTC volume, changed {3:.2f}% over last 24 hr".format(ticker, last, vol, change))
    except:
        bot.say("Error retrieving data from Tuxexchange")

@sopel.module.commands('pepe', 'pepecash')
def pepe(bot, trigger):
    try:
        r = requests.get('https://tuxexchange.com/api?method=getticker')
        j = r.json()
        pepe=j['BTC_PEPECASH']
        last=float(pepe['last'])
        vol=float(pepe['baseVolume'])
        change=float(pepe['percentChange'])
        bot.say("Pepecash at {0:.8f} BTC on {1:.3f} BTC volume, changed {2:.2f}% over last 24 hr".format(last, vol, change))
    except:
        bot.say("Error retrieving data from Tuxexchange")

@sopel.module.commands('pepexmr')
def pepexmr(bot, trigger):
    try:
        r = requests.get('https://tuxexchange.com/api?method=getticker')
        j = r.json()
        pepe=j['BTC_PEPECASH']
        pepelast=float(pepe['last'])
        r=requests.get(polourl)
        j=r.json()
        xmr=j["BTC_XMR"]
        xmrlast=float(xmr['last'])
        bot.say("Pepe/XMR ratio is : {0:.8f}".format(pepelast/xmrlast))
    except:
        bot.say("FAILURE!")


@sopel.module.commands('tall')
def tall(bot, trigger):
    stringtosend = ''
    fixerurl = 'http://api.fixer.io/latest?base=USD'
    stampurl = 'https://www.bitstamp.net/api/ticker/'
    btceurl  = 'https://btc-e.com/api/3/ticker/btc_usd'
    finexurl = 'https://api.bitfinex.com/v1/pubticker/BTCUSD'
    # btccurl  = 'https://pro-data.btcc.com/data/pro/ticker?symbol=XBTCNY'
    btccurl  = 'https://data.btcchina.com/data/ticker?market=btccny'
    huobiurl = 'http://api.huobi.com/staticmarket/ticker_btc_json.js'
    gemiurl  = 'https://api.gemini.com/v1/pubticker/btcusd'
    gdaxurl  = 'https://api.coinbase.com/v2/exchange-rates?currency=BTC'
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdcny = fixerjson['rates']['CNY']
        usdeur = fixerjson['rates']['EUR']
    except:
        usdcny = 7
    # Bitstamp
    try: 
        stampresult = requests.get(stampurl)
        stampjson = stampresult.json()
    except:
	stampjson = False
    if stampjson:
        stringtosend += "Bitstamp last: {0:,.2f}, vol: {1:,.1f} | ".format(float(stampjson['last']), float(stampjson['volume']))
    # BTC-E
    try: 
        btceresult = requests.get(btceurl)
        btcejson = btceresult.json()
    except:
	btcejson = False
    if btcejson:
        stringtosend += "BTC-E last: {0:,.2f}, vol: {1:,.1f} | ".format(float(btcejson['btc_usd']['last']), float(btcejson['btc_usd']['vol_cur']))
    # Gemini
    try: 
        gemiresult = requests.get(gemiurl)
        gemijson = gemiresult.json()
    except:
	gemijson = False
    if gemijson:
        try:
            stringtosend += "Gemini last: {0:,.2f}, vol: {1:,.1f} | ".format(float(gemijson['last']), float(gemijson['volume']['BTC']))
        except:
            pass
    # Gdax
    try: 
        gdaxresult = requests.get(gdaxurl)
        gdaxjson = gdaxresult.json()
    except:
	gdaxjson = False
    if gdaxjson:
        stringtosend += "GDAX price: {0:,.2f} | ".format(float(gdaxjson['data']['rates']['USD']))
    # Bitfinex
    try: 
        finexresult = requests.get(finexurl)
        finexjson = finexresult.json()
    except:
	finexjson = False
    if finexjson:
        stringtosend += "Bitfinex last: {0:,.2f}, vol: {1:,.1f} | ".format(float(finexjson['last_price']), float(finexjson['volume']))
    # BTCC
    try: 
        btccresult = requests.get(btccurl)
        btccjson = btccresult.json()
    except:
	btccjson = False
    if btccjson:
        stringtosend += "BTCC last: {0:,.2f}, vol: {1:,.1f} | ".format(float(btccjson['ticker']['last'])/usdcny, float(btccjson['ticker']['vol']))
    # Huobi
    try: 
        huobiresult = requests.get(huobiurl)
        huobijson = huobiresult.json()
    except:
	huobijson = False
    if huobijson:
        stringtosend += "Huobi last: {0:,.2f}, vol: {1:,.1f} | ".format(float(huobijson['ticker']['last'])/usdcny, float(huobijson['ticker']['vol']))
    # Send the tickers to IRC
    bot.say(stringtosend)


@sopel.module.commands('usd')
def usd(bot, trigger):
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])
        bot.say("Monero price in USD = ${0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('aud')
def aud(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdaud = fixerjson['rates']['AUD']
    except:
        usdaud = 1.35
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdaud
        bot.say("Monero price in AUD = ${0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('cny')
def cny(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdcny = fixerjson['rates']['CNY']
    except:
        usdjpy = 6.8
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdcny
        bot.say("Monero price in CNY = ¥{0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('jpy')
def jpy(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdjpy = fixerjson['rates']['JPY']
    except:
        usdjpy = 110
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdjpy
        bot.say("Monero price in JPY = ¥{0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('eur')
def eur(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdeur = fixerjson['rates']['EUR']
    except:
        usdeur = 0.95
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdeur
        bot.say("Monero price in EUR = €{0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('cad')
def cad(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdcad = fixerjson['rates']['CAD']
    except:
        usdcad = 1.35
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdcad
        bot.say("Monero price in CAD = ${0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('gbp')
def gbp(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdgbp = fixerjson['rates']['GBP']
    except:
        usdgbp = 0.81
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdgbp
        bot.say("Monero price in GBP = £{0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('thb')
def thb(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdthb = fixerjson['rates']['THB']
    except:
        usdthb = 1.35
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdthb
        bot.say("Monero price in THB = ฿{0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('zar')
def zar(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdzar = fixerjson['rates']['ZAR']
    except:
        usdzar = 13.05
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdzar
        bot.say("Monero price in ZAR = R{0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('nzd')
def nzd(bot, trigger):
    # Get conversion rate
    try: 
        fixerresult = requests.get(fixerurl)
        fixerjson = fixerresult.json()
        usdnzd = fixerjson['rates']['NZD']
    except:
        usdnzd = 1.405
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdnzd
        bot.say("Monero price in NZD = ${0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('ntd')
def ntd(bot, trigger):
    # Get conversion rate
    try: 
        ntdurl = r'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("USDTWD")&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
        fixerresult = requests.get(ntdurl)
        fixerjson = fixerresult.json()
        usdntd = float(fixerjson['query']['results']['rate']['Rate'])
    except:
        bot.say("Failed to get NTD value")
        usdntd = 32
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdntd
        bot.say("Monero price in NTD = ${0:,.2f}".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('ugx')
def ugx(bot, trigger):
    # Get conversion rate
    try:
        ugxurl = r'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("USDUGX")&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
        fixerresult = requests.get(ntdurl)
        fixerjson = fixerresult.json()
        usdugx = florat(fixerjson['query']['results']['rate']['Rate'])
    except:
        usdugx = 3200
    try:
        r=requests.get('https://api.coinmarketcap.com/v1/ticker/monero/')
        j=r.json()
        price=float(j[0]['price_usd'])*usdugx
        bot.say("Monero price in UGX = {0:,.2f} shillings".format(price))
    except:
        bot.say("Failed to retrieve price.")

@sopel.module.commands('log')
def log(bot, trigger):
    volurl='https://c-cex.com/t/volume_btc.json'
    try:
        r=requests.get(volurl)
        j=r.json()
        last=float(j['ticker']['log']['last'])
        vol=float(j['ticker']['log']['vol'])
        bot.say("Last price on c-cex for LOG at {0:.8f} BTC on {1:.3f} BTC volume.".format(last, vol))
    except:
        bot.say("C-cex sucks")

@sopel.module.commands('price')
def price(bot, trigger):
    try:
        bot.say("1 XMR = $1000 USD (Offer valid in participating locations)")
    except:
        bot.say("C-cex sucks")
