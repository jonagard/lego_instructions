# lego_instructions

This script gets instructions for a list of Lego sets.  Provide the script a
file of set numbers, one per line, and an API key (see below).

## Why This Script

Hitting the main instructions link runs a bunch of scripts so hitting something
like https://www.lego.com/en-us/service/buildinginstructions/10232 directly with
Python requests does not get what you want.  The scripts at that site hit an
API.

This script hits that same API.

## API Key

You'll need an API key to hit it.  To get the x-api-key:

- Go to https://www.lego.com/en-us/service/buildinginstructions/10232 in a
  browser while inspecting the tab for Network traffic
- Find the POST request to
  https://services.slingshot.lego.com/api/v4/lego_historic_product_read/_search
- Get the x-api-key value from the Request Headers
- Provide it to the script

## Calling

Usage:

`python3 get_instructions.py <sets> <api_key>`

where

- sets
  - A filename including set numbers, one per line
- api_key
  - The API key from a packet, per the above instructions

Example call:

```
$ head sets
3065
3221
3816
3939
5560
5882
7111
7913
7914
8046
```

`python3 get_instructions.py sets ABCDEFG`

## Output

The script will create a directoy per Lego set and pull every manual from the
latest version, like:

    3221/3221-1.pdf
    10232/10232-1.pdf
    10232/10232-2.pdf
    10232/10232-3.pdf

It also downloads an image of the set in the directory.
