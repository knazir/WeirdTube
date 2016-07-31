#!/usr/bin/python
# Usage: python videoCheck.py --videoid=<video_id>

import httplib2
import math
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from Queue import Queue


# # # # # # # # #
# AUTHORIZATION #
# # # # # # # # #

CLIENT_SECRETS_FILE = "secrets/client_secrets.json"
DEVELOPER_SECRETS_FILE = "secrets/youtube-v3-discoverydocument.json"
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


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

# Constants
ENCODING = "utf-8"
NUM_RELATED_VIDEOS = 10
NUM_COMMENTS_PER_PAGE = 100
NUM_COMMENT_PAGES = 10
WEIRD_INDICATORS = [
                    ["weird", "part", "of"], ["wierd", "part", "of"], ["that's enough internet"], ["enough for today"],
                    ["how", "did i get here"], ["what", "did", "i just watch"], ["the fuck did i", "watch"],
                    ["i'm in hell"], ["im in hell"], ["am i watching"], ["side of the internet"], ["side of YouTube"]
                   ]


def setup_args():
    argparser.add_argument("--videoid", help="Required; ID for video.")
    argparser.add_argument("--debug", help="Prints all video comments read.", action="store_true")
    argparser.add_argument("--showreason", help="Prints comment that classifies video as weird.", action="store_true")
    args = argparser.parse_args()
    if not args.videoid:
        exit("Please specify videoid using the --videoid= parameter.")
    return args


def define_globals():
    global REASON
    REASON = None


def get_video_title(youtube, args):
    video_response = youtube.videos().list(
        part='snippet',
        id=args.videoid
    ).execute()
    video = video_response.get("items", [])[0]
    return str(video["snippet"]["title"].encode(ENCODING))


def get_first_video(youtube, args):
    return {"videoid": args.videoid, "title": get_video_title(youtube, args), "previd": None, "clicks":0}


def is_weird(author, comment):
    lowercase_comment = comment.lower()
    for indicator_list in WEIRD_INDICATORS:
        if all(token in lowercase_comment for token in indicator_list):
            globals()["REASON"] = 'Comment by "' + author.encode(ENCODING) + '": "' + comment.encode(ENCODING) + \
                                  '" had a derivation of: ' + str(indicator_list)[1:-1]
            return True
    return False


def is_video_weird(youtube, video):
    next_page_token = None
    for i in range(0, NUM_COMMENT_PAGES):
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video["videoid"],
            textFormat="plainText",
            maxResults=NUM_COMMENTS_PER_PAGE,
            pageToken=next_page_token
        ).execute()

        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            if is_weird(author, text):
                return True

        if "nextPageToken" in results:
            next_page_token = results["nextPageToken"]
        else:
            break
    return False


def get_related_videos(youtube, prev_video):
    search_response = youtube.search().list(
        part="snippet",
        type="video",
        maxResults=NUM_RELATED_VIDEOS,
        relatedToVideoId=prev_video["videoid"]
    ).execute()

    related_videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            related_videos.append({
                "videoid": search_result["id"]["videoId"],
                "title": search_result["snippet"]["title"],
                "previd": prev_video["videoid"],
                "clicks": prev_video["clicks"] + 1
            })
    return related_videos


def check_weirdness(youtube, video):
    if is_video_weird(youtube, video):
        return None
    else:
        return get_related_videos(youtube, video)


def reconstruct_path(video, visited_videos):
    path = [video]
    previd = video["previd"]
    while previd is not None:
        next_video = visited_videos[previd]
        path.append(next_video)
        previd = next_video["previd"]

    reconstructed_path = ""
    index = 1
    for video in reversed(path):
        reconstructed_path += str(index) + ". " + video["title"].encode(ENCODING) + \
                              " (http://www.youtube.com/watch?v=" + video["videoid"].encode(ENCODING) + ") ->\n"
        index += 1
    return reconstructed_path[:-4]


def main():
    # Setup
    define_globals()
    args = setup_args()
    youtube = get_authenticated_service(args)

    # Visible metadata
    queue = Queue()
    visited_videos = {}
    highest_clicks = 0

    if args.debug:
        print("DEBUG: Arguments: " + str(args))

    print("================")
    print("BEGINNING SEARCH")
    print("================")
    video = get_first_video(youtube, args)
    print("Checking initial video...")

    # Wrap requests
    try:
        queue.put(video)
        visited_videos[video["videoid"]] = video

        while not queue.empty():
            # Get next video in queue
            video = queue.get()

            if args.debug:
                print("DEBUG: Trying " + video["title"] + " (http://www.youtube.com/watch?v=" +
                      video["videoid"] + ") " + str(video["clicks"]) + " click(s) away.")

            if video["clicks"] > highest_clicks:
                highest_clicks = video["clicks"]
                print("Checking " + str(int(math.pow(NUM_RELATED_VIDEOS, highest_clicks))) + " videos "
                      + str(highest_clicks) + " click(s) away...")

            # Get related videos
            related_videos = check_weirdness(youtube, video)
            if related_videos is None:
                break
            for related_video in related_videos:
                prev_queue_size = queue.qsize()
                if related_video["videoid"] not in visited_videos:
                    visited_videos[related_video["videoid"]] = related_video
                    queue.put(related_video)

    except HttpError, e:
        print("An HTTP error " + str(e.resp.status) + " occurred: " + str(e))
        return

    # Process and print results
    print
    print("=======")
    print("RESULTS")
    print("=======")
    print("Reached the weird part of YouTube: " + video["title"] + " in " + str(video["clicks"]) + " click(s) after " +
          "examining " + str(len(visited_videos.keys())) + " videos.")
    if args.showreason:
        print("REASON: " + str(REASON))

    # Process and print path
    path = reconstruct_path(video, visited_videos)
    print
    print("====")
    print("PATH")
    print("====")
    print(path)


if __name__ == "__main__":
    main()
