import requests
import pandas as p
import datetime as dt
import os
import threading
from tqdm import tqdm
from time import sleep
import boto3
from os.path import basename
import json
import csv
import gzip
import shutil
import socket

class RunGlue:
    def __init__(self,my_file):
        self.client = boto3.client('glue')
        self.my_file = my_file.replace('/gzip_files','')

        self.basename = basename(my_file)
        self.filename, self.file_extension = os.path.splitext(self.basename)
        self.my_file = self.my_file.replace(self.file_extension,'')

        self.cron = 'cron(15 12 * * ? *)'
        cwd_split = self.my_file.split('/')[:-1]


        target_ibdex = cwd_split.index('alpha') # project name
        self.s3_path = 's3://litcrypto/'+'/'.join(cwd_split[target_ibdex:])+'/'
        #print(self.s3_path)

        self.crawler_name = ''.join(cwd_split[target_ibdex+2:])
        #print(self.crawler_name)


    def create_crawler(self):

        print('Creating: '+self.crawler_name)

        response = self.client.create_crawler(
            Name=self.crawler_name,
            Role='service-role/AWSGlueServiceRole-lit_crypto',
            DatabaseName='litcrypto',
            Description='autogenerated via managedatastorepy',
            Targets={
                'S3Targets': [
                    {
                        'Path': self.s3_path,
                        'Exclusions': []
                    },
                ],
                'JdbcTargets': []
            },
            Schedule=self.cron,
            Classifiers=[],
            TablePrefix='',
            SchemaChangePolicy={
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'DELETE_FROM_DATABASE'
            },
            Configuration=''
        )

    def run_crawler(self):
        try:
            response = self.client.start_crawler(Name=self.crawler_name)
        except Exception as e:
            print(e)

    def validate_create_crawler(self):

        try:
            response = self.client.get_crawler(Name=self.crawler_name)
            #print(response)

        except Exception as e:
            #print(e)
            try:
                rg = RunGlue(self.my_file)
                rg.create_crawler()
            except Exception as e:
                pass
                #print(e)


    def main(self):
        try:
            rg = RunGlue(self.my_file)
            rg.validate_create_crawler()
            rg.run_crawler()

        except Exception as e:
            pass
            #print(e)




if __name__ == '__main__':
    my_file = '/Users/jckail13/lit_crypto_data/alpha/data/social/reddit/reddit.json'#.gz
    cwd = my_file
    #rg = RunGlue(my_file)
    rg = RunGlue()
    rg.main()



    #below model for creating crawler:
    """
 
        response = self.client.create_crawler(
            Name=self.crawler_name,
            Role='service-role/AWSGlueServiceRole-lit_crypto',
            DatabaseName='litcrypto',
            Description='autogenerated via managedatastorepy',
            Targets={
                'S3Targets': [
                    {
                        'Path': self.s3_path,
                        'Exclusions': []
                    },
                ],
                'JdbcTargets': [
                    {
                        'ConnectionName': 'string',
                        'Path': 'string',
                        'Exclusions': [
                            'string',
                        ]
                    },
                ]
            },
            Schedule='string',
            Classifiers=[
                'string',
            ],
            TablePrefix='string',
            SchemaChangePolicy={
                'UpdateBehavior': 'LOG'|'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'LOG'|'DELETE_FROM_DATABASE'|'DEPRECATE_IN_DATABASE'
            },
            Configuration='string'
        )

    
    
    """