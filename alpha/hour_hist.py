import requests
import pandas as p
import datetime as dt
import os
import threading
import urllib2
import time
from time import sleep
from tqdm import tqdm


class GetHourHist(object):

    def __init__(self, symbol_list, exchanges, chunksize):
        self.symbol_list = symbol_list
        self.exchanges = exchanges
        self.chunksize = chunksize

    def get_hour_hist(self,symbol,error_symbols):
        currentts = str(int(time.time()))
        cwd = os.getcwd()
        frames = []
        for exchange in self.exchanges:
            url = "https://min-api.cryptocompare.com/data/histohour"

            querystring = {"fsym":symbol,"tsym":"USD","limit":"2000","aggregate":"3","e":exchange,"toTs":currentts}

            headers = {
                'cache-control': "no-cache",
                'postman-token': "e00df90c-b8b6-cb28-54ff-88c19b883e0a"
            }
            try:
                response = requests.request("GET", url, headers=headers, params=querystring)

                if response.status_code == 200:
                    data = response.json()

                    if data["Data"] != [] and data["Response"] == "Success":
                        df = p.DataFrame(data["Data"])
                        df = df.assign(symbol = symbol, coin_units = 1, timestamp_api_call = dt.datetime.now(),computer_name = 'JordanManual',exchange = exchange )
                        frames.append(df)
                        my_file = cwd+'/data/hour_data/'+symbol+'_hour.csv'
                        if os.path.isfile(my_file):
                            df_resident = p.read_csv(my_file)
                            frames.append(df_resident)
                        else:
                            pass
                        df = p.concat(frames)
                        if not df.empty:
                            df = df.drop_duplicates(['time','exchange','coin'], keep='last')
                            df = df.sort_values('time')
                            df = df.reset_index(drop=True)
                            df.to_csv(my_file, index = False) #need to add this
                            #print 'Updated trade pair: '+str(my_file)
                        else:
                            pass

                    else:
                        pass
                else:
                    pass
            except requests.exceptions.RequestException as e:
                #print(e)
                error_symbols.append(symbol)
                #.append(symbol)
                sleep(0.2)
                #print 'request error'
                pass
            except OverflowError:
                print 'OverflowError: '+str(symbol)
                pass
            except Exception as e:
                #print(e)
                #print 'exception'
                pass

    def main(self):
        error_symbols = []
        gmt = GetHourHist(self.symbol_list,self.exchanges,self.chunksize)

        xsymbols = [self.symbol_list[x:x+self.chunksize] for x in xrange(0, len(self.symbol_list), self.chunksize )]

        print 'Begin: get_hour_hist'

        for symbol_list in tqdm(xsymbols,desc='get_hour_hist'):

            threads = [threading.Thread(target=gmt.get_hour_hist, args=(symbol,error_symbols,)) for symbol in symbol_list]

            for thread in threads:
                thread.start()

            #for thread in tqdm(threads,desc='Closed Threads'):
            for thread in threads:
                thread.join()

                if len(error_symbols) > 0:
                    xsymbols.append(error_symbols)
                    #print 'appending: errors: '+ str(error_symbols)
                    error_symbols = []
                else:
                    pass
        print 'DONE'




if __name__ == '__main__':
    exchanges =['Bitfinex','Bitstamp','coinone','Coinbase','CCCAGG']
    #cwd = os.getcwd()
    #df = p.read_csv(cwd+'/data/coinlist_info.csv')
    #ls_has = df["Symbol"].tolist()
    #ls_has = ls_has[:100]
    runner = GetHourHist(['SMT'],exchanges, 50 )
    #start_time = dt.datetime.now()
    print '--------------------------------------------------------------------------'
    runner.main()
    print '--------------------------------------------------------------------------'
    # x =  dt.datetime.now() - start_time
    #print 'Completion time: '+str(x)

    #7 seconds 100 records