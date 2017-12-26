#!/usr/bin/env python

__author__ = 'jkail'

import requests
import pandas as p
import datetime as dt


class GetCoinLists(object):

    def __init__(self):
        """

        :return:
        """
        print 'ii'
        #self.df = self.func_get_coin_list()
        #exit()

    def func_get_coin_list(self):
        print "called function!!"
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

        df.to_csv('coinlist_info.csv',encoding='utf-8', index = False)
        #print df
        return df

    def main(self):
        """

        :return:
        """
        gcl = GetCoinLists()
        df = gcl.func_get_coin_list()
        #print df
        return df
if __name__ == '__main__':
    """

    :return:
    """
    test = 'a'
    runner = GetCoinLists()
    print runner
    print 'class done '
    runner.main()
    print 'end'

