import os

try:
    token = os.environ['CF_API_TOKEN']
    email = os.environ['CF_API_EMAIL']
    account_id = os.environ['CF_API_ACCOUNT_ID']
except KeyError:
    print('CF_API_TOKEN, CF_API_EMAIL or CF_API_ACCOUNT_ID environment variable not set')

import CloudFlare
import requests
from delete import *
from create import *

def GetBlockList(block_list_url):
    block_list = requests.get(block_list_url).text.splitlines()
    return block_list

def main():
    CF = CloudFlare.CloudFlare(email=email, token=token)

    block_list = GetBlockList(input("Enter the URL of the block list you want to use: "))
    print("Block list has {} domains".format(len(block_list)))

    DeleteAll(CF)
    CreateAll(CF, block_list)

if __name__ == '__main__':
    main()
