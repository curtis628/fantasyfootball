#!/usr/bin/env python

"""
This script helps upload custom images stored on disk to a public location on imgur.com, and
generates a helpful template to use for the basis of an ESPN fantasy football league note.
"""

import argparse
import base64
import json
import logging
import os

from datetime import datetime
from collections import namedtuple

import requests


logger = logging.getLogger(__name__)

# container to hold values that are passed between methods
Config = namedtuple(
    "Config",
    [
        "access_token",
        "client_id",
        "upload_folder",
        "description",
    ])


def _get_response_json(response):
    """Helper method that ensures response is successful, and returns JSON dict"""
    logger.debug("%s resulted in [status=%s]:\nbody:%s",
                 response.url, response.status_code, response.text)
    if not response.ok:
        logger.error("%s failed with [status=%s]\nbody: %s",
                     response.url, response.status_code, response.text)
    response.raise_for_status() # raise exception if API call failed for some reason
    return response.json()      # return JSON dict of the response


def _get_access_token(args):
    """Generates a new Imgur access token to use for interacting with the Imgur API"""
    url = "https://api.imgur.com/oauth2/token"
    data = dict(
            refresh_token=args.refresh_token,
            client_id=args.client_id,
            client_secret=args.client_secret,
            grant_type="refresh_token")
    headers = {"content-type": "application/json"}
    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    response_dict = _get_response_json(response)
    logger.info("Retrieved access token for [username=%s]", response_dict["account_username"])
    return response_dict["access_token"]

def _create_album(config):
    """Creates a new BandOfBrothers Imgur album based on today's date"""
    album_name = "BandOfBrothers-{:%Y-%m-%d}".format(datetime.now())
    logger.debug("Creating [album=%s]", album_name)
    
    url = "https://api.imgur.com/3/album"
    data = dict(
            title=album_name,
            description=config.description)
    headers = {
            "content-type": "application/json",
            "Authorization": "Bearer " + config.access_token
            }
    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    response_dict = _get_response_json(response)
    album_id = response_dict["data"]["id"]
    logger.info("Successfully created album [name=%s] with [id=%s]", album_name, album_id)
    return album_id


def _upload_images(config, album_id):
    """Uploads files from upload_folder to Imgur (and associate with album_id). Returns links."""
    logger.info("Uploading files in %s using [album_id=%s]", args.upload_folder, album_id)
    url = "https://api.imgur.com/3/image"
    headers = {
            "content-type": "application/json",
            "Authorization": "Bearer " + config.access_token
            }

    # We want to upload the files in the same order as their filename. This List Comprehension:
    #  * list all files in upload_folder
    #  * sorts them by filename
    #  * stores the full path of each file in sorted_filenames
    sorted_filenames = [
            os.path.join(config.upload_folder, f) for f in sorted(os.listdir(config.upload_folder))
    ]
    imgur_links = [] # Stores (in sorted order) the public URL for each image uploaded to Imgur
    for path in sorted_filenames:
        with open(path, "rb") as f:  # open image in read-only + binary mode
            image_data = f.read()    # read in our image file and then base64 encode it
            b64_image = base64.standard_b64encode(image_data)
            filename = os.path.basename(path)
            data = {
                    "image": b64_image.decode("UTF-8"),
                    "title": filename,
                    "name": filename,
                    "album": album_id}
            response = requests.request("POST", url, data=json.dumps(data), headers=headers)
            response_dict = _get_response_json(response)
            link = response_dict["data"]["link"]
            logger.info("Successfully uploaded %s to Imgur: %s", path, link)
            imgur_links.append(link)

    logger.info("Successfully uploaded %s files: %s", len(imgur_links), imgur_links)
    return imgur_links

def _print_template(config, imgur_links):
    """Generates initial ESPN league note template based on imgur_links"""
    logging.info("Use the ESPN league note template below as a starting place...")
    if config.description:
        print(config.description + "\n")
    for ndx in range(len(imgur_links)):
        print("%s. " % (ndx+1)) # NOTE: Ordering 1-N; could change 'range` to be descending if needed
        print("[center][image]%s[/image]" % imgur_links[ndx]) # Use ESPN markup to center public image
        print("[/center]")
        print("\n")

def _main(config):
    album_id = _create_album(config)
    imgur_links = _upload_images(config, album_id)
    _print_template(config, imgur_links)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facilitates image upload and formatting for league notes")
    parser.add_argument("client_id", help="The Client Id to use for Imgur's API calls")
    parser.add_argument("client_secret", help="The Client Secret to use for Imgur's API calls")
    parser.add_argument("refresh_token", help="The refresh token to use for Imgur's API calls")
    parser.add_argument("upload_folder", help="The path to the folder containing images to upload")
    parser.add_argument("--description", help="Optional description for the album/template")
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    access_token = _get_access_token(args)
    config = Config(
        access_token=access_token,
        client_id=args.client_id,
        upload_folder=args.upload_folder,
        description=args.description)
    _main(config)
