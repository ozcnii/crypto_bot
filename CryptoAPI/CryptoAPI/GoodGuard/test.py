import requests

import Tools
from GoodGuard.tokensFabric import decode_access_token, generate_access_token, generate_verification_code
from Tools import ContentUtils
from utils import *

"""
url = 'http://127.0.0.1:8000/'
js = {"Authorization1": "123453"}
response = requests.get(url, headers=js)



eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN0cmluZ0BnbWFpbC5jb20iLCJuYW1lIjoic3RyaW5nIiwicGFzc3dvcmQiOiI0NzMyODdmODI5OGRiYTcxNjNhODk3OTA4OTU4ZjdjMGVhZTczM2UyNWQyZTAyNzk5MmVhMmVkYzliZWQyZmE4IiwidG9rZW5faWQiOiIyZmMyYWIzZjcxN2E0MjA1Y2I1NmFlNjQwNzUxNDgxNTA0ZjlhZmRjOGM5YWY5MzZkODVjNmIxMzFjODI1NjUxIn0.VLIcKkXgN6t6Qgd6OA0n8WxBn1efNTsjlQAgcWLt0Fc



test\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN0cmluZ0BmZHNkZGQuY29rIiwibmFtZSI6InN0cmluZyIsInBhc3N3b3JkIjoiNDczMjg3ZjgyOThkYmE3MTYzYTg5NzkwODk1OGY3YzBlYWU3MzNlMjVkMmUwMjc5OTJlYTJlZGM5YmVkMmZhOCIsInRva2VuX2lkIjoiN2Q3YjI0YTM1MjQ3MzlkNzJmOTQyZmVmNWQzMDc5OWI3ZDViZjE4YTNkZjM4ZTVmMzQ5NTJjN2MxZGY3NTU0YiJ9.khCwjKVGv43Dm-ZPpncgj18RCAglXt7VPwh29OL0vQo
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZ2UiOjAsImVtYWlsIjoic3RyaW5nQGdtYWlsLmNvbSIsImFjdGl2aXR5IjpmYWxzZSwibmFtZSI6InN0cmluZyIsInBhc3N3b3JkIjoiNDczMjg3ZjgyOThkYmE3MTYzYTg5NzkwODk1OGY3YzBlYWU3MzNlMjVkMmUwMjc5OTJlYTJlZGM5YmVkMmZhOCIsInRva2VuX2lkIjoiOGI0Nzk5NDQ4YmNlZGNiMTZmNjEwMGJmZDZlNTIxYjEzMWQ2ZTdiYTk4NmFkODU2MWRkZjRmYTgxOTNlZDViOCJ9.mDZVDe_wBDqGENKbtZtPjgyxMINCA92m2qoD1NOLnHw
"""
import requests
import json

# # Формирование URL запроса
# url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={CRYPTO_ID}&range=1d&chartType=prices"
#
# # Добавьте заголовки с вашим API ключом
# headers = {"X-CMC_PRO_API_KEY": API_KEY}
#
# # Отправка запроса
# response = requests.get(url, headers=headers)
#
# # Проверка статуса ответа
# if response.status_code == 200:
#     # Получение данных в формате JSON
#     data = response.json()
#
#     # Вывод полученных данных
#     print(json.dumps(data, indent=4))
# else:
#     print("Произошла ошибка при запросе данных")

import matplotlib.pyplot as plt
from coinmarketcapapi import CoinMarketCapAPI

cmc = CoinMarketCapAPI()
rep = cmc.cryptocurrency_info(symbol='BTC')  # See methods below

print(rep.data)  # Whole repsonse payload
print(rep.data["BTC"]["logo"])  # Some data in response
print(rep.credit_count)  # API credits
print(rep.total_elapsed)  # Request time in ms

# Получение графика со свечами
candles = cmc.cryptocurrency_ohlcv_historical(symbol='BTC', count=10, interval='1d')
print(candles.data)