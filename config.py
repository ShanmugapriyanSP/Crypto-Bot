
binance_test = False

# bitmex_auth = {'apiKey': 'jFJQfp3GQFBEw2dvW9s0VKUL',
#                'secret': 'pUCJphetpR8c86HdQKkYqf1DUhP0BSqXw09KUCIwh0ZLD9hb',
#                }
binance_auth = {'apiKey': 'mPdPO45Augx7jnQogJexCJzHH9kimiIrZ7HsroZbMKdrtHEd2TR2Eiw4MNTLQVkE',
               'secret': 'LzwoKpIiyTO7MUAx8R150LBvQdaQXMyyIZXPQfMmEOM1Z54NGvNbj3zPEE0heBB9',
               }
# twilio_conf = {
#     'account_sid': '',
#     'auth_token': '',
#     'tonumber': '',
#     'fromnumber': '',
#     'msgprefix': ''
# }

sms_url = "https://www.fast2sms.com/dev/bulk"

headers = {
'authorization': "W50qsiUKXPExwoQenCkBlZVjI1YcSLH2RFMDTuvg8NJbyftdArUZ0LaJfVAdbz6cY7spBM5qyOlvHXhT",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}

logfiles = {'main': 'main.log',
            'debug': 'debug.log'
            }

ordersize = 1

# stoploss and take-profit thresholds for bracket in %
sl = 5
tp = 3
