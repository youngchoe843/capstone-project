
import json
import requests
import pandas as pd
import sys


labels=['tweet']
df = pd.DataFrame([sys.argv[1]])
data = df.to_json(orient='records')
header = {'Content-Type': 'application/json',                   'Accept': 'application/json'}

resp = requests.post("http://0.0.0.0:5000/predict", data = json.dumps(data), headers= header)


print (resp.json())
