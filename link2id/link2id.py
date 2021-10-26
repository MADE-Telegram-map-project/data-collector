"""Convert Telegram link to channel id"""

from typing import Iterable, List, Optional
import random
import sys
from time import sleep
import csv
import os
import argparse
import threading
import queue

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import tqdm

# api_hash from https://my.telegram.org, under API Development.
# Enter your phone number, verify with the sent code and
# go to the API Development Tools page.
# There create an app and copy API ID and API HASH.
api_id: int = os.environ["API_ID"]
api_hash: str = os.environ["API_HASH"]

# name of the session. After running file will created with such name, don't delete
session_name = 'links2ids_process'

CHANNEL_KEY = "channel_id"
LINK_KEY = "link"


def wait(n_sec: int = None):
    n_sec = n_sec or random.random() * 1
    sleep(n_sec)


def get_channel_id(client, channel_link: str) -> int:
    """ get id of @channel_link """
    try:
        assert isinstance(channel_link, str)
        full = client(GetFullChannelRequest(channel=channel_link))
        idx = full.full_chat.id
    except Exception as e:
        # some channels in csv are not exist or renamed already
        print(e, file=sys.stderr)
        idx = None
    return idx


def link2id(client, link: str) -> Optional[int]:
    """
    params:
        links - list of links to channel in @link format
    """
    return get_channel_id(client, link)


def main(args):
    csv_reader = csv.DictReader(args.data)
    header = csv_reader.fieldnames
    already_parsed = set()

    if os.path.isfile(args.out):
        with open(args.out, "r", encoding="utf-8", newline="") as link_file:
            reader = csv.DictReader(link_file)
            reader.fieldnames

            for row in reader:
                already_parsed.add(row[LINK_KEY])

    links = []

    for row in csv_reader:
        if row[LINK_KEY] in already_parsed:
            continue
        links.append(row[LINK_KEY])

    args.data.close()

    write_header = True
    if os.path.isfile(args.out):
        write_header = False
    with TelegramClient(session_name, api_id, api_hash) as client, \
        open(args.out, "a", encoding="utf-8", newline="") as processed_file:
        writer = csv.DictWriter(processed_file, fieldnames=[CHANNEL_KEY, LINK_KEY])

        if write_header:
            writer.writeheader()

        for link in tqdm.tqdm(links):
            chanenl_id = link2id(client, link)
            if chanenl_id is not None:
                writer.writerow({LINK_KEY: link, CHANNEL_KEY: str(chanenl_id)})
            wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=argparse.FileType("r", encoding="utf-8"), required=True)
    parser.add_argument("--out", required=True, type=str)

    args = parser.parse_args()
    main(args)
