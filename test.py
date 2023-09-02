# import requests
# import json
#
# url = "https://acdn.tinkoff.ru/pwa-ib-external-source-data/accounts-design.json"
# response = requests.get(url)
#
# body_dict = response.json()
# user_id = body_dict[0] # 1
# print(user_id)

import json

with open('accounts-design.json') as file:
  cards = json.load(file)

# print(type(cards)) # <class 'dict'>
for i in range(0, 321):
  features = cards[i]['card_name'] # ['5G', 'HD display', 'Dual camera']
  print(features)



