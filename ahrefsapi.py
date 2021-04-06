import pandas as pd
import requests
import json

domain = "shopee.co.th"

request = requests.post('https://apiv2.ahrefs.com/?token=09399bb9c2eda7e2da9c9e61001138d1e9259550&target=' + domain +'&limit=1000&output=json&from=positions_metrics&mode=domain')
request_json = request.json()
print(request_json["metrics"]["traffic"])