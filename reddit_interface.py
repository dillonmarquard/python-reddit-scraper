import praw
import platform
import datetime
from itertools import chain, tee

from dataclasses import dataclass
import warnings

@dataclass
class Comment:
    comment_id: str
    thread_id: str
    parent_id: str
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

    def reddit_submission_to_thread(self, submission) -> Thread:
        return Thread(submission.id, submission.selftext, submission.author.name, submission.score, submission.created_utc, submission.permalink)

    def reddit_submission_to_comments(self, submission) -> list[Comment]:
        return [Comment(comment.id, comment.link_id, comment.parent_id, comment.author.name, comment.score, comment.created_utc, comment.body) for comment in submission.comments.list() if comment.author != None]

    def get_subreddit_data(self, subreddit: str, start_date: datetime.datetime = datetime.datetime(2024,1,1), end_date: datetime.datetime = datetime.datetime.today()):
        within_period = lambda thread: thread.created_utc >= start_date.timestamp()
        min_post_date = lambda thread: thread.post_date

        submissions = self._reddit.subreddit(subreddit).new(limit=25)
        valid_submissions1, valid_submissions2 = tee(filter(within_period, submissions))

        thread_list = list(map(self.reddit_submission_to_thread, valid_submissions1))
        comment_list = list(chain.from_iterable(map(self.reddit_submission_to_comments, valid_submissions2)))

        if min(thread_list, key=min_post_date).post_date > (start_date + datetime.timedelta(hours=24)).timestamp():
            # we will display this warning when the last post returned is more than 24 hours after the requested start_date.
            warnings.warn("Reddit's API only returns up to the last 1000 posts, which may not include posts up to the requested date.")

        return thread_list, comment_list