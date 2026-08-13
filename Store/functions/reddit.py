import requests


def get_reddit_posts(subreddit="django", limit=10):
    """
    Retrieve recent posts from a chosen subreddit.

    The function sends an HTTP GET request to Reddit and
    attempts to convert the returned JSON into a simplified
    list of post dictionaries.

    A user-friendly error message is returned if the external
    service cannot provide the requested data.
    """

    # Construct the external API URL dynamically so that
    # different subreddits can be requested when required.
    url = f"https://www.reddit.com/r/{subreddit}/new.json"

    # Identify the application making the HTTP request.
    headers = {
        "User-Agent": (
            "Django-eCommerce-HyperionBootcamp by W Santos"
        )
    }

    # Restrict the amount of external data requested.
    params = {
        "limit": limit
    }

    try:
        # Send an HTTP GET request to the external service.
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10,
        )

        # Convert unsuccessful HTTP responses into exceptions
        # that can be handled safely below.
        response.raise_for_status()

        # Convert the JSON response into Python data.
        data = response.json()

        posts = []

        # Reddit listing responses contain posts inside
        # the data -> children structure.
        for item in data["data"]["children"]:
            post = item["data"]

            posts.append({
                "title": post.get("title", "Untitled post"),
                "author": post.get("author", "Unknown"),
                "score": post.get("score", 0),
                "comments": post.get("num_comments", 0),
                "permalink": post.get("permalink", ""),
            })

        return posts, None

    except requests.HTTPError as error:
        # Handle responses such as 403, 404 and 500 without
        # allowing the external service to crash Django.
        return [], (
            "The external service rejected the request. "
            f"HTTP error: {error.response.status_code}."
        )

    except requests.RequestException:
        # Handle connection errors, timeouts and other
        # network-related failures.
        return [], (
            "The external service could not be reached."
        )

    except (ValueError, KeyError):
        # Handle invalid or unexpected JSON response structures.
        return [], (
            "The external service returned data in an "
            "unexpected format."
        )