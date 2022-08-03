import requests
import pandas as pd

url = "https://api.nasdaq.com/api/screener/stocks?download=true"
headers = {"Accept-Language":"en-US,en;q=0.9",
"Accept-Encoding":"gzip, deflate, br",
"User-Agent":"Java-http-client/"}

response = requests.get(url, headers=headers)
data = response.json()