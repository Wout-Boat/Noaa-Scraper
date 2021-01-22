"""
Program works to download all of the sequential images
"""

import requests
import shutil

# Change this line only
noaa_url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/nr/GEOCOLOR" \
       "/20210200611_GOES16-ABI-nr-GEOCOLOR-2400x2400.jpg"

# Get num code out of URL
url_split = noaa_url.split("/")
start_file_name = url_split[-1]
url_rest = ""

#
for part in url_split[:-1]:
    url_rest += part + "/"


file_name_split = start_file_name.split("_")
number_code = int(file_name_split[0])

file_name = str(number_code) + "_" + file_name_split[1]
print(url_rest)
print(number_code)
print(file_name)
# Need to write some code that then re-creates the url given the components
# and the the number_code that was pulled from the url.
images = 0
skips = 0
while images < 250:

    # The part where the code doesn't work
    r = requests.get(noaa_url, stream=True)
    # End part where the code doesn't work

    if r.status_code == 200:
        skips = 0
        r.raw.decode_content = True
        with open(str(images) + ".jpg", 'a+b') as f:
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