
""""
author jkail
prealpha
calls cryptocompareapi gets history by minute to get history for longer period change
"histominute"  to histohour or "histoday"

"""

import requests
import json
import pandas as p
import datetime as dt
from pandas.io.json import json_normalize

print '------------------ ------- -----  ---------'

coin_types = ["BTC"]

currency_conversion = "USD"

frames = []
limit = "2000"

for x in coin_types:
    url = "https://min-api.cryptocompare.com/data/histominute"
    'https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym='+ tsym +'&limit=2000&aggregate=1&e='+ exchange +'&toTs=' + currentTS
    #querystring = {"fsym":x,"tsym":currency_conversion,"limit":limit,"aggregate":"3","e":"CCCAGG"}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "7d32715c-d0cd-2d35-2b62-f20499f9a994"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    print x
    #test_df = p.DataFrame(data)
    print(response.text)
    status = data["Response"]
    print status
    print type(status)
    if status <> 'Error':
        print 'true'
        test_df = p.DataFrame.from_dict(data,orient='index', dtype=None)
        print test_df
        a1 = test_df
        test_df = p.DataFrame.transpose(test_df)

        data_extract = a1.loc["Data",0]
        data_extract = p.DataFrame(data_extract)
        data_extract = data_extract.assign (cointype = x,timestamp_api_call = dt.datetime.now() )

        frames.append(data_extract)
    else:
        print 'Error:'+x

df = p.concat(frames)
df['time'] = p.to_datetime(df['time'],unit='s') #converts to human from utcE GMT ******

#df.to_csv('test.csv',encoding='utf-8', index = False)
print df
#print data_extract