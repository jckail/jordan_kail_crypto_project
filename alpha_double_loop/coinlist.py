#!/usr/bin/env python

__author__ = 'jkail'

import requests
import pandas as p
import datetime as dt
import os
from tqdm import tqdm
from time import sleep


class GetCoinLists(object):

    def __init__(self, cwd):

        self.cwd = cwd

    def func_get_coin_list(self):
        try:
            frames = []
            source = "cryptocompare"
            url = "https://min-api.cryptocompare.com/data/all/coinlist"

            headers = {
                'cache-control': "no-cache",
                'postman-token': "a1299df4-9db1-44cc-376e-0357176b776f"
            }

            response = requests.request("GET", url, headers=headers)
            data = response.json()

            df = p.DataFrame.from_dict(data["Data"],orient='index', dtype=None)

            df = df.assign (timestamp_api_call = dt.datetime.now(),source = source )
            df = df.reset_index(drop=True)
            df = df.sort_values('Id')
            frames.append(df)

            my_file = self.cwd+'/data/coinlist_info.csv'
            if os.path.isfile(my_file):
                df_resident = p.read_csv(my_file,  encoding= 'utf-8')
                frames.append(df_resident)

            else:
                pass

            df = p.concat(frames)

            if not df.empty:
                df = df.drop_duplicates(['Symbol','source'], keep='last')
                df = df.reset_index(drop=True)
                df.to_csv(my_file, index = False,  encoding= 'utf-8') #need to add this
            else:
                pass
            print 'DONE'
        except requests.exceptions.RequestException as e:
            print e
        except Exception as e:
            print e

    def main(self):
        print 'begin: GetCoinLists.main'

        try:
            gcl = GetCoinLists(self.cwd)
            gcl.func_get_coin_list()

        except Exception as e:
            print e


        print 'end: GetCoinLists.main'


if __name__ == '__main__':
    """

    :return:
    """
    #cwd = '/Users/jkail/Documents/GitHub/lit_crypto/alpha/'
    runner = GetCoinLists()

    runner.main()


