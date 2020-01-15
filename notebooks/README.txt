TO run Flask:

Using Stacia Script:
sudo python myapp_sc.py
go to URL:  18.221.137.114
or ec2-18-221-137-114.us-east-2.compute.amazonaws.com:81

Using Phat Script:
sudo python myapp_pd.py
use the following python script to get return

import json
import requests
import pandas as pd
import sys
 
 
labels=['tweet']
#df = pd.DataFrame([sys.argv[1]])
df = pd.DataFrame(['realdonaldtrump'])
data = df.to_json(orient='records')
# data = {'Name':'heou87'}
header = {'Content-Type': 'application/json','Accept': 'application/json'}
 
# print(data['Name'])
    
resp = requests.post("http://ec2-18-221-137-114.us-east-2.compute.amazonaws.com:80/result", data = json.dumps(data), headers= header)
 
print(resp.json())

