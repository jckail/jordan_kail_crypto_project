#!/usr/bin/env python

#mods
import argparse
import os
import pandas as p
from multiprocessing import Pool, TimeoutError
import time
import threading
#add arg focus symbols only
import datetime as dt


# classes
import buildcoinlist
import day_hist
import test
import setup
import fetchprice
import haspricing
import hour_hist
import minute_hist
import social
import miningdata
import tradepair
import fetchprice


class AlphaRunner(object):

    """
    This is the main runner
    """

    def __init__(self):
        self.args = self.get_args()
        self.run = self.args.run
        self.runfocus_symbols_only = self.args.runfocus_symbols_only
        self.runisprice = self.args.runisprice
        self.cwd = os.getcwd()
        self.focus_symbols = ['BTC','BCH','LTC','ETH']
        # FULL LIST exchanges = ['Cryptsy', 'BTCChina', 'Bitstamp', 'BTER', 'OKCoin', 'Coinbase', 'Poloniex', 'Cexio', 'BTCE', 'BitTrex', 'Kraken', 'Bitfinex', 'Yacuna', 'LocalBitcoins', 'Yunbi', 'itBit', 'HitBTC', 'btcXchange', 'BTC38', 'Coinfloor', 'Huobi', 'CCCAGG', 'LakeBTC', 'ANXBTC', 'Bit2C', 'Coinsetter', 'CCEX', 'Coinse', 'MonetaGo', 'Gatecoin', 'Gemini', 'CCEDK', 'Cryptopia', 'Exmo', 'Yobit', 'Korbit', 'BitBay', 'BTCMarkets', 'Coincheck', 'QuadrigaCX', 'BitSquare', 'Vaultoro', 'MercadoBitcoin', 'Bitso', 'Unocoin', 'BTCXIndia', 'Paymium', 'TheRockTrading', 'bitFlyer', 'Quoine', 'Luno', 'EtherDelta', 'bitFlyerFX', 'TuxExchange', 'CryptoX', 'Liqui', 'MtGox', 'BitMarket', 'LiveCoin', 'Coinone', 'Tidex', 'Bleutrade', 'EthexIndia', 'Bithumb', 'CHBTC', 'ViaBTC', 'Jubi', 'Zaif', 'Novaexchange', 'WavesDEX', 'Binance', 'Lykke', 'Remitano', 'Coinroom', 'Abucoins', 'BXinth', 'Gateio', 'HuobiPro', 'OKEX']
        self.exchanges = ['Bitfinex','Bitstamp','coinone','Coinbase','CCCAGG']
        #self.exchanges = ['Coinbase']
        self.chunksize = 199  #~~#thread limit
        #self.org_params = json.load(open("config/cti_config.dict"))

    def get_args(self):
        """
        :return:
        """
        parser = argparse.ArgumentParser(usage='alpha_runner.py --run <run> --runfocus_symbols_only <runfocus_symbols_only> --runisprice <runisprice>')
        parser.add_argument('--run', required=True, dest='run', choices=['Y', 'N'], help='want to run this y')
        parser.add_argument('--runfocus_symbols_only', required=True, dest='runfocus_symbols_only', choices=['Y', 'N'], help='runfocus_symbols_only run')
        parser.add_argument('--runisprice', required= False, default= 'N',dest='runisprice', choices=['Y', 'N'], help='runfocus_symbols_only run')
        args = parser.parse_args()
        print '------'+str(args)
        return args

    def alpha_runner(self):
        print 'Chunk size: '+str(self.chunksize)
        if self.run == 'Y':
            print "Begin alpha_runner"
            try:
                try:
                    if self.runfocus_symbols_only == 'N':
                        #get list of coins
                        coin_df = buildcoinlist.GetCoinLists(self.runfocus_symbols_only,self.focus_symbols,self.cwd)
                        gcl_output = coin_df.main()
                        df = p.read_csv(self.cwd+'/data/coinlist_info.csv')
                        ls_has = df["Symbol"].tolist()

                    elif self.runfocus_symbols_only == 'Y':
                        ls_has = self.focus_symbols
                except Exception as e:
                    print(e)
                    print 'error getting symbol_list'

                try:
                    x = len(ls_has)
                    #ls_has = ls_has[:5]
                    #ls_has.append('SMT')
                    print '--------------------------------------------------------------------------'
                    print 'Evaluating: '+str(x)+' Coins'
                    print '--------------------------------------------------------------------------'
                    #helps limit #threads open etc

                    md = miningdata.GetMineData(self.cwd)
                    md.main()
                    #thread1 = #threading.Thread(target=md.main(), args=())

                    print'--------------------------------------------------------------------------'
                    mfp = fetchprice.GetDtlPrice(ls_has, self.exchanges, self.chunksize,self.cwd) #chunk size not used here just broken up into 50 strings due to api list constraint
                    mfp.main()
                    #thread2 = #threading.Thread(target=mfp.main(), args=())
                    print'--------------------------------------------------------------------------'

                    #tp = tradepair.GetTradePair(ls_has,self.cwd)
                    #tp.main()
                    ##thread3 = #threading.Thread(target=tp.main(), args=())
                    print'--------------------------------------------------------------------------'

                    mh = minute_hist.GetMinuteHist(ls_has,self.exchanges,self.chunksize,self.cwd)
                    mh.main()
                    #thread4 = #threading.Thread(target=mh.main(), args=())

                    hh = hour_hist.GetHourHist(ls_has,self.exchanges,self.chunksize,self.cwd)
                    hh.main()
                    #thread5 = #threading.Thread(target=hh.main(), args=())

                    dh = day_hist.GetDayHist(ls_has,self.exchanges,self.chunksize,self.cwd)
                    dh.main()
                    #thread6 = #threading.Thread(target=dh.main(), args=())
                    print'--------------------------------------------------------------------------'

                    #gsd = social.GetSocialData(ls_has,self.cwd)
                    #gsd.main()
                    ##thread7 = #threading.Thread(target=mfp.main(), args=())


                    #thread1.start()
                    #thread2.start()
                    ##thread3.start()
                    #thread4.start()
                    #thread5.start()
                    #thread6.start()

                    #thread1.join()
                    #thread2.join()
                    ##thread3.join()
                    #thread4.join()
                    #thread5.join()
                    #thread6.join()
                    ##thread7.start()

                        # non 0:00:35.364493
                        #multi#thread  0:00:21.039896
                        #full run mutli #thread

                except Exception as e:
                    print(e)
                    print 'error on processing dtl, hist'
                #askcurrentprice from has price/ if focus_symbols passed

            except Exception as e:
                print(e)
                print "ERROR: alpha_runner"

        else:
            print 'invalid args'

    def main(self):
        start_time = dt.datetime.now()
        setup.setup_alpha()
        print '----------------------------BEGIN----------------------------'
        self.alpha_runner()
        print '----------------------------END----------------------------'
        x = dt.datetime.now() - start_time
        print 'Completion time: '+str(x)




if __name__ == '__main__':
    ar = AlphaRunner()

    ar.main()






