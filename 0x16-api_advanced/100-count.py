#!/usr/bin/python3
"""
Python script that, using this REST API, for a given subreddit,
returns all its hot posts for a given subreddit.
"""
import requests


def count_words(subreddit, word_list, after=None, count_dict=None):
    if count_dict is None:
        count_dict = {}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'after': after} if after else {}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        after = data['data']['after']
        for post in posts:
            title = post['data']['title'].lower()
            for word in word_list:
                if word.lower() in title:
                    index = title.index(word.lower())
                    if (index == 0 or not title[
                        index-1].isalpha()) and (index+len(word) == len(
                            title) or not title[index+len(word)].isalpha()):
                        if word.lower() in count_dict:
                            count_dict[word.lower()] += 1
                        else:
                            count_dict[word.lower()] = 1
        if after:
            return count_words(subreddit, word_list, after, count_dict)
        else:
            sorted_counts = sorted(
                count_dict.items(), key=lambda x: (-x[1], x[0]))
            for count in sorted_counts:
                print(f"{count[0]}: {count[1]}")
    else:
        print(None)
