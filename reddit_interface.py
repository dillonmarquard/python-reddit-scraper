import praw
import platform
import datetime
from itertools import chain

from dataclasses import dataclass
import warnings



@dataclass
class Comment:
    comment_id: str
    thread_id: str
    username: str
    upvotes: int
    post_date: float
    comment: str

@dataclass
class Thread:
    thread_id: str
    original_post: str
    username: str
    upvotes: int
    post_date: float
    url: str
    comments: list[Comment]
    
class RedditAPI:
    """Reddit API wrapper for pulling subreddit and (sub-)comment data"""

    def __init__(self, username: str, app: str, client: str, secret: str):
        self._client = client
        self._secret = secret
        self._user_agent = f"{platform.system()}:{app}:v0.1.0 (by u/{username})"
        # this will be a read-only interface
        self._reddit = praw.Reddit(
            client_id = self._client,
            client_secret = self._secret,
            user_agent = self._user_agent,
            ratelimit_seconds = 300,
        )

    def __str__(self) -> str:
        return self._user_agent

    def get_threads(self, subreddit: str, start_date: datetime.datetime = datetime.datetime(2024,1,1), end_date: datetime.datetime = datetime.datetime.today()):
        threads = self._reddit.subreddit(subreddit).new(limit=25)
        thread_list = [Thread(thread.id, thread.selftext, thread.author.name, thread.score, thread.created_utc, thread.permalink, [Comment(comment.id, comment.link_id, comment.author.name, comment.score, comment.created_utc, comment.body) for comment in thread.comments.list()]) for thread in threads if thread.created_utc >= start_date.timestamp()]
        comment_list = list(chain.from_iterable([thread.comments for thread in thread_list]))
        if thread_list[-1].post_date > (start_date + datetime.timedelta(hours=24)).timestamp():
            # we will display this warning when the last post returned is more than 24 hours after the requested start_date.
            warnings.warn("Reddits API only returns the last 1000 posts, which may not include posts up to the requested date.")
        return thread_list, comment_list