#!/usr/bin/python3
"""
100-count
"""
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursive function to query the Reddit API and count occurrences of specified keywords.

    Args:
        subreddit (str): The subreddit to query.
        word_list (list): List of keywords to count occurrences.
        after (str): Token for pagination.
        counts (dict): Dictionary to store keyword counts.

    Returns:
        None
    """
    if counts is None:
        counts = {}

    headers = {'User-agent': 'Mozilla/5.0'}
    url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    params = {'limit': 100, 'after': after}

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get('data', {})
    children = data.get('children', [])

    for child in children:
        title = child.get('data', {}).get('title', '').lower()
        for word in word_list:
            word = word.lower()
            if word in title:
                counts[word] = counts.get(word, 0) + 1

    after = data.get('after')
    if after:
        count_words(subreddit, word_list, after, counts)
    else:
        print_results(counts)

def print_results(counts):
    """
    Print the results in descending order by count and alphabetically by keyword.

    Args:
        counts (dict): Dictionary containing keyword counts.

    Returns:
        None
    """
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    for word, count in sorted_counts:
        print(f'{word}: {count}')

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], [x for x in sys.argv[2].split()])

