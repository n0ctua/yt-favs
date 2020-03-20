#
# Download your latest Youtube favorites
#
# usage:
# $ source env/bin/activate
# $ python yt-favs.py
#

import httplib2
import os
import sys
import json
import subprocess

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"


# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    # Trusted testers can download this discovery document from the developers page
    # and it should be in the same directory with the code.
    return build(API_SERVICE_NAME, API_VERSION,
                 http=credentials.authorize(httplib2.Http()))


args = argparser.parse_args()
service = get_authenticated_service(args)

# ---------- END BOILERPLATE CODE ----------

success_count = 0
fail_count = 0

# Load previous video list from json-file
try:
    with open("data.json", "r") as file:
        video_dict = json.load(file)
except FileNotFoundError:
    print("No previous video data found. Creating a new list.")
    video_dict = {}  # {video_id: (downloaded, title), }

# Retrieve the contentDetails part of the channel resource for the
# authenticated user's channel.
channels_response = service.channels().list(
    mine=True,
    part="contentDetails"
).execute()

# From the API response, extract the playlist ID that identifies the list
# of videos uploaded to the authenticated user's channel.
uploads_list_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["favorites"]

# Retrieve the list of videos uploaded to the authenticated user's channel.
playlistitems_list_request = service.playlistItems().list(
    playlistId=uploads_list_id,
    part="snippet",
    maxResults=50
)

# Put information about each video in the dictionary
while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()

    for playlist_item in playlistitems_list_response["items"]:
        title = playlist_item["snippet"]["title"]
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        if video_id not in video_dict:
            video_dict[video_id] = [False, title]  # list instead of tuple, because json naturally doesn't support it
            print("Added this video to your collection: %s" % title)

    playlistitems_list_request = service.playlistItems().list_next(
        playlistitems_list_request, playlistitems_list_response)

# Download videos, which were not already downloaded
print("\nDownloading...")
for key, value in video_dict.items():
    if not value[0]:
        process = subprocess.run(["youtube-dl", key, "-o", "~/Videos/%(title)s-%(id)s.%(ext)s"],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        if process.returncode:
            print("%s\t(%s)\t\033[1;31mFAILED\033[1;m" % (value[1], key))
            fail_count += 1
        else:
            print("%s\t(%s)\t\033[1;32mSUCCESS\033[1;m" % (value[1], key))
            video_dict[key][0] = True  # mark video as downloaded
            success_count += 1

# Print Stats
print(
    "\nYou have %d Youtube favorites\nYou successfully downloaded %d new videos\n%d Downloads failed"
    % (len(video_dict), success_count, fail_count)
)

# Write current favorites to json-file
with open("data.json", "w") as file:
    json.dump(video_dict, file, indent=4, separators=(",", ": "))
