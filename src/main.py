from AutoTrade import AutoTrader
import os

def __main__():
    os.system('clear')
    test_str = input("[ Wanna test mode first ? (Test mode will never trigger the real order in Binance) [yes/no] ]: ")
    test = True if test_str == "yes" else False
    screen_name = input("[ Twitter screen name which you wanna track, i.e. elonmusk. ]: ")
    cb = AutoTrader(screen_name)
    cb.keywords = input("[ Keywords which are included in the tweet will trigger automatic order in Binance, i.e. doge btc crypto. (Separate keyword by space and case insensitive here): ] ").split(" ")
    symbol = input("[ One symbol of coin pair, i.e. DOGEUSDT or DOGEBTC (Always use upper case here and always use the existing pair, e.g. 'USDTDOGE' does *not* exist)]: ")
    quantity = float(input("[ Quantity of the coin(left coin in symbol) you wanna buy, i.e. 100 or 0.5 ]: "))

    auto_price_str = input("[ Do you want the bot to set a sale price for you ? [yes/no] ]: ")
    growth_rate = None
    if auto_price_str == 'yes': auto_price = True 
    else:
        auto_price = False
        growth_rate = float(input("[ How much percentage do you wanna increase the current price to sell ? i.e. 0.05 or 0.1 (5% or 10%) ]: "))

    print("#" * 100)
    print("[ Please check the parameters you have inputed: ]")
    print(f"[ test mode ]: {test_str}")
    print(f"[ screen name ]: {screen_name}")
    print(f"[ keywords ]: {cb.keywords}")
    print(f"[ symbol ]: {symbol}")
    print(f"[ quantity ]: {quantity}")
    print(f"[ auto price ]: {auto_price_str}")
    if not auto_price: print(f"[ growth rate ]: {growth_rate}")

    ok_str = input("[ Are they correct? [yes/no] ]: ")
    if ok_str == "yes":
        print("Start tracking... press 'ctrl+c' to terminate ")
        cb.order_by_tweets(test, symbol=symbol, quantity=quantity, growth_rate=growth_rate, auto_price=auto_price)
    else: print("Please try again...")

__main__()

