#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "secrets/client_secrets.json"
DEVELOPER_SECRETS_FILE = "secrets/youtube-v3-discoverydocument.json"
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# # # # # # # # #
# AUTHORIZATION #
# # # # # # # # #

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message="Invalid client secrets file.")

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  with open(DEVELOPER_SECRETS_FILE, "r") as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))


# # # # # # #
# ALGORITHM #
# # # # # # #

NUM_COMMENTS_PER_PAGE = 100
NUM_COMMENT_PAGES = 10
WEIRD_INDICATORS = [["weird", "part", "of"], ["that's", "enough", "internet"], ["enough", "for", "today"], ["how", "did", "i", "get", "here"], 
["what", "did", "i", "just", "watch"], ["the", "fuck", "did", "i"],["i'm", "in", "hell"], ["im", "in", "hell"], ["why", "am", "i", "watching"], ]


def setup_args():
  argparser.add_argument("--videoid",
    help="Required; ID for video.")
  args = argparser.parse_args()
  if not args.videoid:
    exit("Please specify videoid using the --videoid= parameter.")
  return args


def is_weird(comment):
  lowercase_comment = comment.lower()
  for indicator_list in WEIRD_INDICATORS:
    if all(token in lowercase_comment for token in indicator_list):
      return True
  return False


def is_video_weird(youtube, video_id):
  next_page_token = None
  for i in range(0, NUM_COMMENT_PAGES):
    results = youtube.commentThreads().list(
      part="snippet",
      videoId=video_id,
      textFormat="plainText",
      maxResults=NUM_COMMENTS_PER_PAGE,
      pageToken=next_page_token
    ).execute()

    if "nextPageToken" in results:
      next_page_token = results["nextPageToken"]
    else:
      return False

    for item in results["items"]:
      comment = item["snippet"]["topLevelComment"]
      author = comment["snippet"]["authorDisplayName"]
      text = comment["snippet"]["textDisplay"]
      if is_weird(text):
        return True

  return False


def get_video_title(youtube, video_id):
  video_response = youtube.videos().list(
    part='snippet',
    id=video_id
  ).execute()
  video = video_response.get("items", [])[0]
  return str(video["snippet"]["title"])


def check_weirdness(youtube, video_id):
  if is_video_weird(youtube, args.videoid):
    print("Yep, " + get_video_title(youtube, args.videoid) + " (http://www.youtube.com/watch?v=" + args.videoid + ") is in the weird part of YouTube.")
  else:
    print("Nope, " + get_video_title(youtube, args.videoid) + " (http://www.youtube.com/watch?v=" + args.videoid + ") is NOT in the weird part of YouTube.")


if __name__ == "__main__":
  args = setup_args()
  youtube = get_authenticated_service(args)
  try:
    check_weirdness(youtube, args.videoid)
  except HttpError,e:
    print("An HTTP error " + str(e.resp.status) + " occurred:\n" + str(e.content))
