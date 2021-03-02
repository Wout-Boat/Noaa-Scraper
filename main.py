"""
Program works to download all of the sequential images of a specificed
animation loop from NOAA's weather satalite image page at
https://www.star.nesdis.noaa.gov/goes/index.php
"""

# Imports
import os
import shutil

import cv2
import ffmpeg

import requests

# Change this line only
noaa_url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/nr/GEOCOLOR/20210400126_GOES16-ABI-nr-GEOCOLOR-2400x2400.jpg"

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
img_path = cwd + '\\img\\'

# Creates the /img/ directory if it doesn't exist
if not os.path.exists(img_path):
    os.makedirs(img_path)

# Main downloading loop start
# TODO: need to make the loop not go off of
#  images but to go just based off of skips.
while True:

    # creates the download url for this current loop with the current
    # number code
    working_url = url_rest + str(number_code) + "_" + file_name_split[1]

    # The request to the url
    r = requests.get(working_url, stream=True)

    # If file is found
    if r.status_code == 200:

        # Reset skips
        skips = 0

        # Required to function but use to me is unknown.
        r.raw.decode_content = True

        # Saves image to path
        # zfill(5) adds leading zeros to the numbers, this prevents opencv from
        # ordering the images incorrectly.
        with open(img_path + str(images).zfill(5) + ".jpg", 'a+b') as f:
            # save the image data
            shutil.copyfileobj(r.raw, f)
        # Notify user of status
        if (images % 5 == 0):
            print("Downloading... (" + str(images) + "/~210)")
        # Increment images
        images += 1

    # If file is not found
    if r.status_code != 200:

        # Add one to skips
        skips += 1

        # If we skip an image too many times kill the loop
        if skips > 15:
            break

    # The images are only saved in increments of 5?
    # This skips to the next image in sequence.
    number_code += 5

# TODO: Need to add a loop here that changes the size of the frames
#   so that they are 1920x1080
print("Done downloading files")

print("Putting video in the oven...")
# Location of the temporary avi video file
# Following code shamelessly stolen from stack exchange
video_name = "tmp_output.avi"
# Makes an list of all the images in /img/
imgs = [img for img in os.listdir(img_path) if img.endswith(".jpg")]

# Gets the first frame from the list
frame = cv2.imread(os.path.join(img_path, imgs[0]))
# Make some nice variables from the frame size
height, width, layers = frame.shape

# Make the VideoWriter object
video = cv2.VideoWriter(video_name, 0, 10, (width, height))

# Add all the frames to the video
for image in imgs:
    video.write(cv2.imread(os.path.join(img_path, image)))

# Bake that bad boy
cv2.destroyAllWindows()
video.release()

print("It's out of the oven, watch out it's hot!")

# Convert video
# TODO: Add comments to following section

print("Cleaning up after myself...")
os.remove(img_path)

print("All done!")
print("Your video is in " + cwd + ". As output.avi!")