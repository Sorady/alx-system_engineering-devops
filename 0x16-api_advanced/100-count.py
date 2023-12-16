#!/usr/bin/python3
""" module to get all hot posts on subreddit """
from requests import get


def count_words(subreddit, word_list, obj={}, after=''):
    """ get all hot posts on provided subreddit
        Params:
            subreddit: subreddit provided to search in it
            hot_list: list of titles
        Return:
            list of all title of posts
    """
    if obj == {}:
        for li in word_list:
            obj[li] = 0
    url = f'https://www.reddit.com/r/{subreddit}/hot.json{after}'
    header = {'User-Agent': 'Amgad_fikry_alx_task_3'}
    req = get(url, allow_redirects=False, headers=header)
    if req.status_code == 200:
        data = req.json().get('data')
        posts = data.get('children')
        for post in posts:
            for li in word_list:
                if post.get('data').get('title').find(li) != -1:
                    obj[li] = obj[li] + 1
        if data.get('after') != 'null':
            count_words(subreddit,
                        word_list,
                        obj,
                        f'?after={data.get("after")}')
        print(obj)
        return ''
