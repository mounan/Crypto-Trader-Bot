# Auto Trader Bot

<img src="https://tva1.sinaimg.cn/large/008i3skNgy1gqw0r078s1j308g02kt8m.jpg" alt="スクリーンショット 2021-05-26 19.37.04" style="zoom:35%;" align='left' /><img src="https://tva1.sinaimg.cn/large/008i3skNgy1gqw0r54jnkj308i05g74e.jpg" alt="スクリーンショット 2021-05-26 19.42.12" style="zoom:25%;" />

## Description

Tracking a specific **[Twitter](https://twitter.com/home?lang=en)** user's tweet, and trigger the BUY and SELL order in **[Binance](https://www.binance.com/en)**.

#### Expectation

* Expect this bot to help you earn money in the short-term operations.

* Don't hesitate to [ask](https://twitter.com/Arumin78850081) questions, open issues, and making comments.



## Motivation 

<img src="https://tva1.sinaimg.cn/large/008i3skNgy1gqw0g7juq6j30wa0lwtt4.jpg" alt="スクリーンショット 2021-05-26 19.19.23" style="zoom:33%;" />

<img src="https://tva1.sinaimg.cn/large/008i3skNgy1gqw0gpmet3j30ac0lwjs8.jpg" alt="スクリーンショット 2021-05-26 19.23.57" style="zoom:33%;" />



## Wrokflow Example

For instance of tracking [Alice](https://en.wikipedia.org/wiki/Alice_and_Bob)'s tweet and you let the bot to listen keywords like 'doge' or 'btc' from Alice's new tweet. And you preset the bot to buy 300  [DOGEs](https://www.coindesk.com/price/dogecoin) using USDTs at the price when Alice tweets some triggers. And you want to sell them when the price of DOGE go up by like 10%.

And then Alice tweeted like this:

<img src="https://tva1.sinaimg.cn/large/008i3skNgy1gqw0gu8yzpj30lr07rq40.jpg" alt="IMG_9909" style="zoom:33%;" />

Then, your Binance account will do two things automaticlly below:

1. Order to buy 300 doges at current price (let's say buying_price) in seconds
2. If buying succeeds then it will set another order to sell 300 doges at  buying_price*1.1 (1.1 times much than buying price)

Fortunately, you will earn 30*buying_price which is a 10% profits.

After all of this, the bot will keep tracking.



## Warnings

* Always use the test mode at first when you activate the bot 🤖.
* Try a little money first.
* The bot will keep running unless you terminate it manually.
* The setting of the bot is immutable in the runtime.
* Long is always better than short.





## Table of Contents

* [src/AutoTrade.py](https://github.com/mounan/cryptobot/blob/main/src/AutoTrade.py): Central control of twitterBot and binanceBot. 
* [src/BinanceBot.py](https://github.com/mounan/cryptobot/blob/main/src/BinanceBot.py): Encapsulation method class based on Binance API.
* [src/TwitterBot.py](https://github.com/mounan/cryptobot/blob/main/src/TwitterBot.py): Encapsulation method class based on Twitter API. 
* [src/main.py](https://github.com/mounan/cryptobot/blob/main/src/main.py): Launcher of the program.
* [src/utils.py](https://github.com/mounan/cryptobot/blob/main/src/utils.py): Some global utilitiy methods. 
* [src/Exceptions](https://github.com/mounan/cryptobot/blob/main/src/Exceptions): Some global exception classes.



## Installation

In your shell, ```cd``` to a proper place and type:

```shell
git clone https://github.com/mounan/cryptobot.git
```



## Usage

Make sure you already download the whole project locally.

#### Preparation

0. Python version >= 3.8

1. Python dependencies

    In your shell, ```cd``` to the project directory and type:

    ```shell
    cd cryptobot
    pip install requirements.txt
    ```

2. API keys

    1. Apply your own Twitter API bearer token and Binance API key pair:

        * [How to generate a Twitter API bearer token](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens)
        * [How to get yout Binance API key pair](https://www.binance.com/en/support/faq/360002502072)

        ***Note: Do not tell anyone any of your own keys and please save them properly.**

    2. Add your own keys into the **config.yaml** file in to proper place.

        ***Note: This file will only be saved to your local location**

        * e.g.

    <img src="https://tva1.sinaimg.cn/large/008i3skNgy1gqw0gxhcehj31cu0ai41g.jpg" alt="スクリーンショット 2021-05-26 17.16.05" style="zoom:20%;" />

3. Some faits or cryptos in your Binance wallet.

#### Activate the bot

1. In your shell, ```cd``` to the ```src``` directory and type:

    ```shell
    cd src
    python main.py	
    ```

2. Input the required parameters and make the bot alive 🤖

    <img src="https://tva1.sinaimg.cn/large/008i3skNgy1gqw0h01w3wj31280u04lt.jpg" alt="スクリーンショット 2021-05-26 17.25.57" style="zoom:50%;" />

#### What else ?

* You can download the [Caffeine](https://caffeine.en.softonic.com/mac) to keep your screen on while runing program.

    

## Coming features

* Tweets text checking with the sentiment analysis.
* Recognize the images within the tweets and make this a trigger.



## Authors

* Munan Zou  -  *Owner/maintainer* - :octocat: [mounan](https://github.com/mounan)

    _Looking for maintainers!_

    

## Buy Me A Coffee! ☕

If you want to support me, thank you !

My crypto adresses :

DOGE : ```D85LSY7sUgZneZpmmzkc4A4GR9ZFicEkoC```

ETH : ```0x863AB67C1f1B11Afe91e83dAAdCE9d6AfCaAcB4C```

USDT : ```0x863AB67C1f1B11Afe91e83dAAdCE9d6AfCaAcB4C``` 

BTC : ```17Kyg52xqnG53sH43sbSRezT2sWk4Aoubh```



## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/mounan/cryptobot/blob/main/LICENSE) file for details.



## Reference

* [Binance API document](https://github.com/binance/binance-spot-api-docs)

* [Twitter API document](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline)

    