import requests


def get_posts(user_id=None):
    """
    Retrieve posts from the JSONPlaceholder /posts endpoint.

    If user_id is provided, only posts belonging to that
    user are requested. Otherwise, all posts are returned.
    """

    url = "https://jsonplaceholder.typicode.com/posts"

    params = {}

    if user_id is not None:
        params["userId"] = user_id

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"JSONPlaceholder request failed: {error}")
        return []