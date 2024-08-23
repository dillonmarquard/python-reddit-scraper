import sqlite3

from reddit_interface import Thread, Comment

class SqLiteDB:
    """A sqlite3 interface to save subreddit post and comment data"""
    
    def __init__(self):
        self._url = "reddit.db"
        self._con = sqlite3.connect(self._url)
        self._cur = self._con.cursor()
        with open("reddit-db-init.sql") as f:
            self._cur.executescript(f.read())
            self._con.commit()

    def __str__(self) -> str:
        return self._url

    def insert_update_post(self, data: list[Thread]) -> str:
        """update + insert data about a post on a subreddit"""
        sql = f"""
            INSERT OR REPLACE INTO Thread (thread_id, original_post, username, upvotes, post_date, url) values (?, ?, ?, ?, ?, ?);
        """
        res = [(thread.thread_id, thread.original_post, thread.username, thread.upvotes, thread.post_date, thread.url) for thread in data]
        self._cur.executemany(sql, res)
        self._con.commit()

        return sql

    def insert_update_comment(self, data: list[Comment]) -> None:
        """update + insert data about a comment for a post"""
        sql = f"""
            INSERT OR REPLACE INTO Comment (comment_id, thread_id, parent_id, username, upvotes, post_date, comment) values (?, ?, ?, ?, ?, ?, ?);
        """
        res = [(comment.comment_id, comment.thread_id, comment.parent_id, comment.username, comment.upvotes, comment.post_date, comment.comment) for comment in data]
        self._cur.executemany(sql, res)
        self._con.commit()
        
        return sql

    def get_comments(self) -> list[Comment]:
        sql = """
            SELECT * FROM Comment;
        """
        return self._cur.execute(sql).fetchall()

    def get_threads(self) -> list[Thread]:
        sql = """
            SELECT * FROM Thread;
        """
        return self._cur.execute(sql).fetchall()