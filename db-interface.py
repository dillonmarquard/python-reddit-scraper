import sqlite3

class SqLiteDB:
    """A sqlite3 interface to save subreddit post and comment data"""
    
    def __init__(self):
        self._con = sqlite3.connect("reddit-of02j.db") # pull from secrets.yaml
        self.cur = con.cursor()

    def insert_update_post() -> None:
        """update + insert data about a post on a subreddit"""
        pass

    def insert_update_comment() -> None:
        """update + insert data about a comment for a post"""
        pass