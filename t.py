#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import re

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import textwrap
from auth import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)
from twython import TwythonStreamer

import time
from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)

font13 = ImageFont.truetype(os.path.join(picdir, 'GnuUnifont.ttf'), 13)

def printToDisplay(string):
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 10), string, font = font13, fill = 0)
    epd.display(epd.getbuffer(image))

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if data['lang'] == 'en':
            username = data['user']['screen_name']
            tweet = data['text']
            tweet = re.sub(r"&amp", "", tweet)
            tweet = textwrap.fill(data['text'], width = 35)
            print(f"@{username}: \n{tweet}")
            printToDisplay(f"{username}: \n{tweet}")
            time.sleep(3)


        def on_error(self, status_code, data):
            print(status_code)



stream = MyStreamer(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

filter = ['San Francisco', '🛸']
stream.statuses.filter(track = filter)
