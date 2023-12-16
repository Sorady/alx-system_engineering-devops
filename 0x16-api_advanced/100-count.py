#!/usr/bin/python3
"""This module contains the count_words function."""
import requests


def count_words(subreddit, wordlist, after="", count=0, word_count={}):
    """Recursively queries Reddit API, parses all hot posts' titles for a
    given subreddit and prints sorted word frequency of given keywords.
    """

    word_list = [w.lower() for w in wordlist]

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
            "user-agent": "Python:recurse_script:v1.0.0 (bu /u/Peace_Deer4685)"
            }
    payload = {
            "after": after,
            "count": count,
            "limit": 100
            }

    res = requests.get(url, headers=headers, params=payload,
                       allow_redirects=False)

    try:
        if res.status_code == 404:
            raise Exception
        res = res.json()
    except Exception:
        return

    res = res.get("data")
    after = res.get("after")
    count = res.get("count")
    for p in res.get("children"):
        title = p.get("data").get("title").lower().split()
        for w in title:
            if w in word_list:
                c = word_count.get(w, 0)
                word_count[w] = c + 1

    if after is not None:
        count_words(subreddit, wordlist, after, count, word_count)
    elif len(word_count) == 0:
        return
    else:
        word_count = sorted(word_count.items(), key=lambda i: (-i[1], i[0]))

        for key, val in word_count:
            print("{}: {}".format(key, val))
