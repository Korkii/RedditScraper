# Reddit Scraper

This project is a Reddit scraper that retrieves 100 posts from a given subreddit. The retrieved data includes key details like the post title, author, number of comments, and timestamp.

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

1. Open the `src/main.py` file and modify the `subreddit` variable to the desired subreddit:
    ```python
    if __name__ == '__main__':
        subreddit = "ubisoft"  # Change this to your desired subreddit
        posts = scrape_subreddit(subreddit, "hot", 100)

        for post in posts["posts"]:
            print(post)
    ```

2. Run the script:
    ```sh
    python src/main.py
    ```

## Notes

- This scraper uses direct HTTP requests to fetch the HTML content of the subreddit pages.
- The `BeautifulSoup` library is used to parse the HTML and extract the required data.
- The script handles pagination to retrieve up to 100 posts from the subreddit.
