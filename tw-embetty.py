#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
from requests.exceptions import HTTPError
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_tweet(tweetid):
  response = requests.get('https://cdn.syndication.twimg.com/tweet-result?id='+tweetid)
  response.raise_for_status()
  # access json content
  jsonResponse = response.json()
  #print(jsonResponse)

  embetty = {
    "data": {
      "created_at": jsonResponse["created_at"],
      "lang": jsonResponse["lang"],
      "edit_history_tweet_ids": jsonResponse["edit_control"]["edit_tweet_ids"],
      "text": jsonResponse["text"],
      "author_id": jsonResponse["user"]["id_str"]
    },
    "includes": {
      "users": [
        {
          "profile_image_url": jsonResponse["user"]["profile_image_url_https"],
          "id": jsonResponse["user"]["id_str"],
          "name": jsonResponse["user"]["name"],
          "username": jsonResponse["user"]["screen_name"]
        },
      ],
    },
  }

  return embetty


def get_profile_image(tweetid):
  response = requests.get('https://cdn.syndication.twimg.com/tweet-result?id='+tweetid)
  response.raise_for_status()
  # access json content
  jsonResponse = response.json()
  #print(jsonResponse)
  imgreq = requests.get(jsonResponse["user"]["profile_image_url_https"])
  return imgreq.content



#http calls


@app.route('/<tweetid>',  methods = ['GET'])
def embetty_get_tweet(tweetid):
    return jsonify(get_tweet(int(tweetid)))

@app.route('/<tweetid>/profile-image',  methods = ['GET'])
def embetty_get_tweet_img(tweetid):
    return get_profile_image(int(tweetid))



if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=5000)
