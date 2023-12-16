#!/usr/bin/python3
"""
Python script that, using this REST API, for a given subreddit,
returns the 10 hot posts
"""
import requests


def top_ten(subreddit):
    """
    Returns the 10 hot posts for a given subreddit.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for post in data['data']['children']:
            print(post['data']['title'])
    else:
        print(None)
