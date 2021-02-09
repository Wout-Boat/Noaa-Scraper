"""
Program works to download all of the sequential images of a specificed
animation loop from NOAA's weather satalite image page at
https://www.star.nesdis.noaa.gov/goes/index.php
"""

# Imports
import requests
import shutil
import os
import cv2

# Change this line only
noaa_url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/nr/GEOCOLOR/20210390641_GOES16-ABI-nr-GEOCOLOR-2400x2400.jpg"

# This witchcraft uses Python's insane list splitting tools to select the
# filename in the URL and set it to start_file_name
url_split = noaa_url.split("/")
start_file_name = url_split[-1]

# Creates the string to be used for the rest of the url base
url_rest = ""

# This adds the rest of the URL excluding the filename into one string under
# url_rest. Selecting from url_split list with [:-1] to exclude filename.
for part in url_split[:-1]:
    url_rest += part + "/"

# Splits the filename around the _ right after the number code
file_name_split = start_file_name.split("_")

# number_code is equal to the first index of the split.
number_code = int(file_name_split[0])

# ints used for the main downloading loop
images = 0
skips = 0

# Gets the running directory for the script
cwd = os.getcwd()
# Adds /img/ to the end of the running directory
img_path = cwd + '/img/'

# Creates the /img/ directory if it doesn't exist
if not os.path.exists(img_path):
    os.makedirs(img_path)

# Main downloading loop start
# TODO: need to make the loop not go off of
#  images but to go just based off of skips.
while images < 250:

    # creates the download url for this current loop with the current
    # number code
    working_url = url_rest + str(number_code) + "_" + file_name_split[1]

    # The request to the url
    r = requests.get(working_url, stream=True)

    # If file is found
    if r.status_code == 200:
        # Reset skips
        skips = 0

        r.raw.decode_content = True

        # Saves image to path
        # zfill(5) adds leading zeros to the numbers, this prevents opencv from
        # ordering the images incorrectly.
        with open(img_path + str(images).zfill(5) + ".jpg", 'a+b') as f:
            #
            shutil.copyfileobj(r.raw, f)
        print("Downloaded number " + str(images))
        images += 1

    # If file is not found
    if r.status_code != 200:

        # Add one to skips
        skips += 1

        # If we skip an image too many times kill the loop
        if skips > 15:
            images += 1000

    # The images are only saved in increments of 5?
    # This skips to the next image in sequence.
    number_code += 5

# TODO: - Need to add coments to the following portion.
#   - Also need to add a loop here that changes the size of the frames
#   so that they are 1920x1080
print("Done downloading files")

video_name = "output.avi"
imgs = [img for img in os.listdir(img_path) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(img_path, imgs[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 10, (width, height))

for image in imgs:
    video.write(cv2.imread(os.path.join(img_path, image)))

cv2.destroyAllWindows()
video.release()