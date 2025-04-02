import requests

BASE_URL = "https://dummyjson.com"

BASE_LOGIN_ENDPOINT = "/auth/login"

BASE_AUTH_ENDPOINT = "/auth/me"

BASE_POSTS_ENDPOINT = "/posts"

BASE_COMMENTS_ENDPOINT = "/posts/{id}/comments"

BASE_AUTH_TAG = "Bearer"

BASE_AUTH_HEADER = "Authorization"

BASE_POSTS_LIMIT = 60

BASE_POST_ID_KEY = "id"

BASE_COMMENTS_KEY = "comments"

VALID_CODE = 200


TOKEN_KEYS = ["token", "accessToken"]


def extract_auth_token(reply):
    for key in TOKEN_KEYS:
        if key in reply:
            return reply[key]
    return None



def login(username, password):
        url = f"{BASE_URL}{BASE_LOGIN_ENDPOINT}"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)

        if response.status_code == VALID_CODE:
            reply = response.json()
            token = extract_auth_token(reply)
            if token:
                return token
            else:
                print("Login succeeded, but no token found in response due to: ")
                print(reply)
                return None
        else:
            print("Login Failed due to: ")
            print(response.json())
            return None


def get_user_info(token):
    url = f"{BASE_URL}{BASE_AUTH_ENDPOINT}"

    headers = {
        BASE_AUTH_HEADER: f"{BASE_AUTH_TAG} {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == VALID_CODE:
        return response.json()
    else:
        print("Failed to get user info due to: ")
        print(response.json())
        return None

def get_posts():

    url = f"{BASE_URL}{BASE_POSTS_ENDPOINT}"
    parameters = {"limit": BASE_POSTS_LIMIT}

    response = requests.get(url, params=parameters)

    if response.status_code == VALID_CODE:
        reply = response.json()
        return reply.get("posts", [])
    else:
        print("Failed to fetch posts due to: ")
        print(response.json())
        return []


def get_comments_for_posts(posts):
    for post in posts:
        post_id = post.get(BASE_POST_ID_KEY)
        endpoint = BASE_COMMENTS_ENDPOINT.replace("{id}", str(post_id))
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url)

        if response.status_code == VALID_CODE:
            reply = response.json()
            post[BASE_COMMENTS_KEY] = reply.get(BASE_COMMENTS_KEY, [])

        else:
            print(f"Failed to get comments for post {post_id} due to: ")
            print(response.json())
            post["comments"] = []

    return posts








