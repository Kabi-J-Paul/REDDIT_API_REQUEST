"""Query a subreddit with Reddit's JSON API and show its key details."""

import sys

import requests

DEFAULT_SUBREDDIT = "learnpython"
USER_AGENT = "python:subreddit-info:v1.0 (by /u/Kabi-Jean-Paul)"
TIMEOUT = 20


def get_json(base, path, **params):
    response = requests.get(
        base + path,
        headers={"User-Agent": USER_AGENT},
        params=params,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def main():
    subreddit = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SUBREDDIT
    subreddit = subreddit.removeprefix("r/").strip("/")
    base = f"https://www.reddit.com/r/{subreddit}"

    about = get_json(base, "/about.json")["data"]
    rules = get_json(base, "/about/rules.json")["rules"]
    posts = get_json(base, "/top.json", limit=10, t="all")["data"]["children"]
    posts = sorted(posts, key=lambda post: post["data"].get("score", 0), reverse=True)

    print(f"Subreddit:   {about.get('display_name_prefixed', 'r/' + subreddit)}")
    print(f"Subscribers: {about.get('subscribers', 0):,}")
    print(f"Description: {about.get('public_description') or about.get('description') or 'N/A'}")
    print("\nRules:")
    for number, rule in enumerate(rules, 1):
        print(f"{number}. {rule.get('short_name', 'Rule')}")
    print("\nTop 10 posts by upvotes:")
    for number, post in enumerate(posts[:10], 1):
        data = post["data"]
        print(
            f"{number}. {data.get('title', 'Untitled')} - "
            f"u/{data.get('author', '[deleted]')} ({data.get('score', 0)} upvotes)"
        )


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, KeyError, ValueError) as error:
        print(f"Reddit API request failed: {error}")
        print("Reddit now requires API approval under its Responsible Builder Policy.")
        sys.exit(1)
