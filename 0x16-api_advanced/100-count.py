#!/usr/bin/python3
"""
This function queries the Reddit API and  parses the
title of all hot articles, and prints a sorted count
of given keywords (case-insensitive, delimited by spaces.
Javascript should count as javascript, but java should not).
"""
import requests


def count_words(subreddit, word_list, hot_list=[], after=""):
    """
    Returns the sorted count of keywords appearing in
    titles of hot posts in Reddit

    Args:
        subreddit (string): The name of the subreddit
        wordlist (list): The list of keywords to search for
        hot_list (list): List of all posts of a subredit
        after (string): The id of the parameter in url used
                        to query for next page items
    Return:
           word_count (dict): sorted count of given keywords
    """
    if subreddit is None:
        return None

    url = 'https://www.reddit.com/r/{}/hot/.json'.format(subreddit)
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0)\
     AppleWebKit/538.0.0 (KHTML, like Gecko) \
     Chrome/17.0.821.0 Safari/538.0.0'}

    try:
        response = requests.get(url, headers=user_agent,
                                allow_redirects=False,
                                params={'limit': 100,
                                        'after': after})

        if response.status_code == 200:
            results = response.json()
            top_posts = results.get('data').get('children')

            for post in top_posts:
                hot_list.append(post.get('data').get('title'))

            after = results.get('data').get('after')

            if after is None:
                keywords_dict = {}
                for word in word_list:
                    word = word.lower()
                    for post_title in hot_list:
                        count = count_occurence(word, post_title)
                        if count > 0:
                            if keywords_dict.get(word):
                                keywords_dict[word] += count
                            else:
                                keywords_dict[word] = count

                sorted_dict = sorted(keywords_dict.items(),
                                     key=lambda item: (-item[1], item[0]))

                for key, value in sorted_dict:
                    print("{}: {}".format(key, value))
            else:
                return count_words(subreddit, word_list, hot_list, after)
        else:
            return None
    except Exception:
        return None


def count_occurence(key, title):
    """
    Returns the number of occurence of a word in a sentence

    Args:
        key (string): The word to count number of occurence
        title (string): The sentence to count the occurences

    Return:
           count (int): The number of times the word occurs
    """
    words = title.split()
    count = 0
    for word in words:
        if key.lower() == word.lower():
            count += 1
    return count
