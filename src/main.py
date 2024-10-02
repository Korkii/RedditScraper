from typing import List
import requests
from bs4 import BeautifulSoup
import time
from dataclasses import dataclass
from typing import List, Dict, Union


@dataclass
class RedditPost:
    title: str
    author: str
    num_comments: int
    timestamp: str
    link: str
    score: int


def get_subreddit_page(subreddit, after=None):
    base_url = f"https://www.reddit.com/r/{subreddit}/"
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "intl_splash=false"
    }

    url = base_url + ("?after=" + after if after else "")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Unable to fetch page (status code {response.status_code})")
        return None


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


def scrape_subreddit(subreddit_id: str, sort: Union["new", "hot", "old"], max_pages: int = None):
    base_url = f"https://www.reddit.com/r/{subreddit_id}/"
    response = requests.get(base_url)
    subreddit_data = {"posts": []}
    data = parse_reddit_posts(response.text)
    subreddit_data["posts"].extend(data["posts_data"])
    cursor = data["cursor"]

    def make_pagination_url(cursor_id: str):
        return f"https://www.reddit.com/svc/shreddit/community-more-posts/hot/?after={cursor_id}%3D%3D&t=DAY&name=vim&feedLength=3&sort={sort}"

    while cursor and (max_pages is None or max_pages > 0):
        url = make_pagination_url(cursor)
        response = requests.get(url)
        data = parse_reddit_posts(response.text)
        cursor = data["cursor"]
        post_data = data["posts_data"]
        subreddit_data["posts"].extend(post_data)
        if max_pages is not None:
            max_pages -= 1
        print(f"Scraped {len(post_data)} posts, total: {len(subreddit_data['posts'])}")

    return subreddit_data


if __name__ == '__main__':
    subreddit = "vim"
    posts = scrape_subreddit(subreddit, "hot", 3)

    for post in posts["posts"]:
        print(post)
