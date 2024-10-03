import requests
from bs4 import BeautifulSoup
import time
from dataclasses import dataclass
from typing import List, Dict, Union
import argparse

@dataclass
class RedditPost:
    title: str
    author: str
    num_comments: int
    timestamp: str
    link: str
    score: int


def parse_reddit_posts(html):
    soup = BeautifulSoup(html, 'html.parser')
    posts: List[RedditPost] = []

    article_containers = soup.find_all('article')

    for article in article_containers:
        title = article.get('aria-label', "Title not found")

        shreddit_post_tag = article.find('shreddit-post')

        if shreddit_post_tag:
            score = shreddit_post_tag.get('score', "Score not found")
            comment_count = shreddit_post_tag.get('comment-count', "Comments not found")
            author = shreddit_post_tag.get('author', "Author not found")
            timestamp = shreddit_post_tag.get('created-timestamp', "Timestamp not found")
            link = shreddit_post_tag.get('permalink', "Link not found")
        else:
            score = comment_count = author = timestamp = link = "Data not found"

        posts.append(
            RedditPost(title, author, comment_count, timestamp, link, score)
        )

    cursor_tag = soup.find('shreddit-post', {'more-posts-cursor': True})

    if cursor_tag:
        after_cursor = cursor_tag.get('more-posts-cursor')
    else:
        after_cursor = None

    return {"posts_data": posts, "cursor": after_cursor}


def scrape_subreddit(subreddit_id: str, sort: Union["new", "hot", "old"], max_posts: int):
    base_url = f"https://www.reddit.com/r/{subreddit_id}/"
    response = requests.get(base_url)
    subreddit_data = {"posts": []}
    data = parse_reddit_posts(response.text)
    subreddit_data["posts"].extend(data["posts_data"])
    cursor = data["cursor"]

    def make_pagination_url(cursor_id: str):
        return f"https://www.reddit.com/svc/shreddit/community-more-posts/hot/?after={cursor_id}%3D%3D&t=DAY&name=vim&feedLength=3&sort={sort}"

    while cursor and len(subreddit_data["posts"]) < max_posts:
        url = make_pagination_url(cursor)
        response = requests.get(url)
        data = parse_reddit_posts(response.text)
        cursor = data["cursor"]
        post_data = data["posts_data"]
        subreddit_data["posts"].extend(post_data)

    subreddit_data["posts"] = subreddit_data["posts"][:max_posts]

    return subreddit_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape Reddit posts from a subreddit.')
    parser.add_argument('subreddit', type=str, help='The subreddit to scrape')
    parser.add_argument('sort', type=str, choices=['new', 'hot', 'old'], help='The sorting order of posts')
    parser.add_argument('max_posts', type=int, help='The maximum number of posts to scrape')

    args = parser.parse_args()

    posts = scrape_subreddit(args.subreddit, args.sort, args.max_posts)

    for post in posts["posts"]:
        print(post)
