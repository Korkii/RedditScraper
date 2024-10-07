# Reddit Scraper

This project is a Reddit scraper that retrieves posts from a given subreddit. The retrieved data includes key details like the post title, author, number of comments, and timestamp.

## Features

- Scrapes posts from a specified subreddit.
- Retrieves key details such as title, author, number of comments, timestamp, link, and score.
- Uses direct HTTP requests without relying on browser automation tools or the official Reddit API.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Korkii/RedditScraper
    cd reddit-scraper
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the script with the desired arguments:
    ```sh
    python src/main.py <subreddit> <sort> <max_posts>
    ```
    - `<subreddit>`: The subreddit to scrape (e.g., `python`)
    - `<sort>`: The sorting order of posts (`new`, `hot`, or `old`)
    - `<max_posts>`: The maximum number of posts to scrape (e.g., `100`)

    Example:
    ```sh
    python src/main.py vim hot 100
    ```

## Demo

![Demo](https://imgur.com/WyJYaQH.png)

## Notes

- This scraper uses direct HTTP requests to fetch the HTML content of the subreddit pages.
- The `BeautifulSoup` library is used to parse the HTML and extract the required data.
- The script handles pagination to retrieve the specified number of posts from the subreddit.
