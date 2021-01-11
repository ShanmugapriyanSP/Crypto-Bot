import os

binance_test = False

# bitmex_auth = {'apiKey': 'jFJQfp3GQFBEw2dvW9s0VKUL',
#                'secret': 'pUCJphetpR8c86HdQKkYqf1DUhP0BSqXw09KUCIwh0ZLD9hb',
#                }
binance_auth = {'apiKey': os.environ.get("BINANCE_API_KEY"),
                'secret': os.environ.get("BINANCE_SECRET"),
                }
# twilio_conf = {
#     'account_sid': '',
#     'auth_token': '',
#     'tonumber': '',
#     'fromnumber': '',
#     'msgprefix': ''
# }

sms_url = "https://www.fast2sms.com/dev/bulk"

mail_user = os.environ.get("MAIL_USER")
mail_password = os.environ.get("MAIL_PASSWORD")

headers = {
    'authorization': "W50qsiUKXPExwoQenCkBlZVjI1YcSLH2RFMDTuvg8NJbyftdArUZ0LaJfVAdbz6cY7spBM5qyOlvHXhT",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
}

logfiles = {'main': 'logs/main.log',
            'debug': 'logs/debug.log'
            }

ordersize = 1

# stoploss and take-profit thresholds for bracket in %
sl = 5
tp = 3
