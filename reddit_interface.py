import requests
import datetime
from dataclasses import dataclass


@dataclass
class Thread:
    original_post: str
    username: str
    upvotes: int
    post_date: datetime.date
    url: str

@dataclass
class Comment:
    username: str
    upvotes: int
    post_date: datetime.date
    comment: str
    

class RedditAPI:
    """Reddit API wrapper for pulling subreddit and (sub-)comment data"""

    def __init__(self, username: str, app: str, client: str, secret: str):
        
        self._client = client
        self._secret = secret
        self._auth = requests.auth.HTTPBasicAuth(client, secret)
        self._user_agent = f"{app} by u/{username}"

    def get_threads(self, subreddit: str, start_date: datetime.date = datetime.date(2024,1,1), end_date: datetime.date=datetime.date.today()) -> list[Thread]:
        pass

    def get_comments(self, post: str) -> list[Comment]:
        pass