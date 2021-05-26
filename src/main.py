from AutoTrade import AutoTrader

me = 'gilfoyle0302'
cb = AutoTrader(me)
cb.keywords = ['doge', ]
symbol = 'DOGEUSDT'
cb.order_by_tweets(True, symbol, quantity=100, growth_rate=0.01,)


    
