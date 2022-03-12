#!/usr/bin/env python3

''' This script gets instructions for a list of Lego sets.  Provide the script a
file of set numbers, one per line, and an API key (see below).

Hitting the main instructions link runs a bunch of scripts so hitting something
like https://www.lego.com/en-us/service/buildinginstructions/10232 directly with
requests does not get what you want.  The scripts hit an API.

This script hits that same API.  You'll need an API key to hit it.  To get the
x-api-key:

- Go to https://www.lego.com/en-us/service/buildinginstructions/10232 in a
  browser while inspecting the tab for Network traffic
- Find the POST request to
  https://services.slingshot.lego.com/api/v4/lego_historic_product_read/_search
- Get the x-api-key value from the Request Headers
- Provide it to the script

The script will create a directoy per Lego set and pull every manual from the
latest version, like:

    3221/3221-1.pdf
    10232/10232-1.pdf
    10232/10232-2.pdf
    10232/10232-3.pdf

It also downloads an image of the set.
'''

import os
import requests
import sys

if len(sys.argv) != 3:
    print('usage: python3 get_instructions.py <sets> <api_key>\n'
          '    sets - A filename including set numbers, one per line\n'
          '    api_key - The API key from a packet, per the heredoc instructions')
    sys.exit()

sets_file = sys.argv[1]
api_key = sys.argv[2]

url = "https://services.slingshot.lego.com/api/v4/lego_historic_product_read/_search"

payload = '{{\"_source\":[\"product_number\",\"locale.en-us\",\"locale.en-us\",\"market.us.skus.item_id\",\"market.us.skus.item_id\",\"availability\",\"themes\",\"product_versions\",\"assets\"],\"from\":0,\"size\":1,\"query\":{{\"bool\":{{\"must\":[{{\"term\":{{\"product_number\":\"{set_num}\"}}}}],\"should\":[],\"filter\":[]}}}}}}'

headers = {
              'Accept': 'application/json, text/plain, */*',
              'Content-Type': 'application/json;charset=utf-8',
              'x-api-key': f'{api_key}'
          }

with open(sets_file, 'r') as infile:
    for set_num in infile:
        set_num = set_num.strip()
        # Get full JSON for product
        response = requests.request("POST",
                                    url,
                                    headers=headers,
                                    data=payload.format(set_num=set_num))
        text = response.json()

        # If there are instruction manuals, loop through them
        try:
            for i, j in enumerate(text['hits']['hits'][0]['_source']['product_versions'][-1]['building_instructions'], 1):
                if not os.path.isdir(set_num):
                    # If we're here, there are instructions
                    # If target directory does not exist, create it.
                    os.mkdir(set_num)

                if i == 1:
                    # This is the first manual.  There might be more.  On the
                    # first one, download the product picture
                    pic_url = text['hits']['hits'][0]['_source']['assets'][0]['assetFiles'][0]['url']
                    pic_name = text['hits']['hits'][0]['_source']['assets'][0]['assetFiles'][0]['fileName']
                    pic_response = requests.get(pic_url)
                    with open(f'{set_num}/{pic_name}', 'wb') as outfile:
                         outfile.write(pic_response.content)

                # Get the manual
                book_url = j['file']['url']
                book_response = requests.get(book_url)
                with open(f'{set_num}/{set_num}-{i}.pdf', 'wb') as outfile:
                     outfile.write(book_response.content)
        except:
            # No fanfare, just make the caller aware something is weird about
            # this set
            print(f'Not getting manual(s) for {set_num}')
            continue
