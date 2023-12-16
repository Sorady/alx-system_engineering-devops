#!/usr/bin/python3
"""
100-count
"""
import requests

def count_words(subreddit, word_list, after=None, count={}):
    """
    Recursive function that queries the Reddit API, parses the title of all hot
    articles, and prints a sorted count of given keywords
    """
    # Base case: invalid subreddit or no more pages
    if after is None and count == {}:
        return None
    # Set the headers and parameters for the request
    headers = {'User-Agent': 'python3:100-count:v1.0'}
    params = {'limit': 100, 'after': after}
    # Make the request to the subreddit's hot articles
    response = requests.get('https://www.reddit.com/r/{}/hot.json'.format(subreddit), headers=headers, params=params, allow_redirects=False)
    # Check the status code
    if response.status_code != 200:
        return None
    # Get the data as a dictionary
    data = response.json().get('data')
    # Get the list of hot articles
    articles = data.get('children')
    # Loop through the articles
    for article in articles:
        # Get the title of the article
        title = article.get('data').get('title').lower()
        # Loop through the word list
        for word in word_list:
            # Check if the word is in the title
            if word.lower() in title.split():
                # Increment the count of the word
                count[word.lower()] = count.get(word.lower(), 0) + title.split().count(word.lower())
    # Get the next page
    after = data.get('after')
    # Recursive call with the next page and the current count
    count_words(subreddit, word_list, after, count)
    # Print the results
    if after is None:
        # Sort the count by value and then by key
        sorted_count = sorted(count.items(), key=lambda x: (-x[1], x[0]))
        # Loop through the sorted count
        for key, value in sorted_count:
            # Print the word and the count
            print('{}: {}'.format(key, value))
