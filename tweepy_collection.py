import micro_influencer_utilities as miu
import tweepy
import os
import time
import sys
from pathlib import Path
from datetime import datetime
import json
import re

pathToTwitterAuthData = "twitterAccess.txt"
pathToDevKeyAndSecret = "consumer_api_keys.txt"

api = miu.authentication(pathToDevKeyAndSecret, pathToTwitterAuthData)