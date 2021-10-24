from typing import Iterable
import re
import random
import sys
from time import sleep

import pandas as pd
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import tqdm

# api_hash from https://my.telegram.org, under API Development.
# Enter your phone number, verify with the sent code and
# go to the API Development Tools page.
# There create an app and copy API ID and API HASH.
api_id: int = None
api_hash: str = None

# name of the session. After running file will created with such name, don't delete
session_name = 'links2ids_process'


def wait(n_sec: int = None):
    n_sec = n_sec or random.random() * 2
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


def links2ids(links: Iterable[str]) -> list:
    """
    params:
        links - list of links to channel in @link format
    """
    with TelegramClient(session_name, api_id, api_hash) as client:
        ids = []
        for link in tqdm.tqdm(links):
            cur_id = get_channel_id(client, link)
            ids.append(cur_id)
            wait()

    return ids


def main():
    df = pd.read_csv("data/tg_channels.csv", index_col=0)
    links = df["link"].values[:100]

    ids = links2ids(links)
    print(ids)


main()
