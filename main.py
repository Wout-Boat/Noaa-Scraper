"""
Program works to download all of the sequential images
"""

import requests
import shutil
import os

# Change this line only
noaa_url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/nr/GEOCOLOR/20210211901_GOES16-ABI-nr-GEOCOLOR-2400x2400.jpg"

# Get num code out of URL
url_split = noaa_url.split("/")
start_file_name = url_split[-1]
url_rest = ""

#
for part in url_split[:-1]:
    url_rest += part + "/"

file_name_split = start_file_name.split("_")
number_code = int(file_name_split[0])

images = 0
skips = 0

cwd = os.getcwd()
path = cwd + '/img/'

if not os.path.exists(path):
    os.makedirs(path)

while images < 250:

    working_url = url_rest + str(number_code) + "_" + file_name_split[1]

    r = requests.get(noaa_url, stream=True)

    if r.status_code == 200:
        skips = 0
        r.raw.decode_content = True
        with open(path + str(images) + ".jpg", 'a+b') as f:
            shutil.copyfileobj(r.raw, f)
        print("Downloaded number " + str(images))
        images += 1

    if r.status_code != 200:
        print("Skipping " + noaa_url)
        skips += 1
        if skips > 15:
            images += 1000

    number_code += 5

print("Done downloading files")
