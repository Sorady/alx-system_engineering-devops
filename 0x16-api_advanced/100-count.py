#!/usr/bin/python3
'''Get ALL hot posts'''
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {}

    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"

    headers = {
        'User-Agent': 'Unix:0-subs:v1'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']

        for post in posts:
            title = post['data']['title'].lower()
            for word in word_list:
                word = word.lower()
                if f" {word} " in f" {title} ":
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1

        after = data['data']['after']

        if after is not None:
            count_words(subreddit, word_list, after, counts)
        else:
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

            for word, count in sorted_counts:
                print(f"{word}: {count}")
