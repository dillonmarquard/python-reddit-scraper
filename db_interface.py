import sqlite3
from dataclasses import dataclass

from reddit_interface import Subreddit, Thread, Comment

@dataclass
class CommentForest: # children of top-level comments
    comment: Comment
    children: list[Comment]

@dataclass
class ThreadComments:
    thread: Thread
    comments: list[CommentForest] # list of top-level comments

@dataclass
class SubredditThreads:
    subreddit: Subreddit
    threads: list[ThreadComments]

def rec_forest(p, comment_list):
    children = []
    for c in filter(lambda t: t.parent_id[3:] == p.comment_id, comment_list):
        tmp = rec_forest(c, comment_list)
        children.append(tmp)
    return CommentForest(p, children)

def gen_comment_forest(thread, comment_list): # for a specific thread
    thread_comments = list(filter(lambda c: c.thread_id[3:] == thread.thread_id, comment_list))
    cf = [rec_forest(tlc, thread_comments) for tlc in filter(lambda t: t.parent_id[0:3] == 't3_', thread_comments)]
    return ThreadComments(thread, cf)

def rec_display_comments(tc, depth=1, max_depth=0) -> None:
    print('\t'*depth,'|', tc.comment.comment_id, tc.comment.username, len(tc.comment.comment))
    if max_depth and depth > max_depth: # 0 implies no depth limit
        return
    for comment in tc.children:
        rec_display_comments(comment, depth + 1, max_depth)

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

    def insert_update_post(self, data: list[Thread]) -> None:
        """update + insert data about a post on a subreddit"""
        sql = f"""
            INSERT OR REPLACE INTO Thread (thread_id, subreddit_id, original_post, username, upvotes, post_date, url) values (?, ?, ?, ?, ?, ?, ?);
        """
        res = [(thread.thread_id, thread.subreddit_id, thread.original_post, thread.username, thread.upvotes, thread.post_date, thread.url) for thread in data]
        self._cur.executemany(sql, res)
        self._con.commit()

    def insert_update_comment(self, data: list[Comment]) -> None:
        """update + insert data about a comment for a post"""
        sql = f"""
            INSERT OR REPLACE INTO Comment (comment_id, thread_id, parent_id, username, upvotes, post_date, comment) values (?, ?, ?, ?, ?, ?, ?);
        """
        res = [(comment.comment_id, comment.thread_id, comment.parent_id, comment.username, comment.upvotes, comment.post_date, comment.comment) for comment in data]
        self._cur.executemany(sql, res)
        self._con.commit()

    def insert_update_subreddit(self) -> None:
        pass

    def get_comments(self) -> list[Comment]:
        sql = """
            SELECT * FROM Comment;
        """
        return [Comment(res[0], res[1], res[2], res[3], res[4], res[5], res[6]) for res in self._cur.execute(sql).fetchall()]

    def get_threads(self) -> list[Thread]:
        sql = """
            SELECT * FROM Thread;
        """
        return [Thread(res[0], res[1], res[2], res[3], res[4], res[5], res[6]) for res in self._cur.execute(sql).fetchall()]

    def get_thread_comments(self, thread_list, comment_list) -> list[ThreadComments]:
        tcl = []
        for thread in thread_list:
            cfl = gen_comment_forest(thread, comment_list)
            tcl.append(cfl)
        return tcl

    def get_subreddit_threads(self) -> dict:
        thread_list = self.get_threads()
        comment_list = self.get_comments()
        d = {thread.subreddit_id : [] for thread in thread_list}
        tcl = self.get_thread_comments(thread_list, comment_list)
        for tc in tcl:
            d[tc.thread.subreddit_id].append(tc)
        
        return d

    def display_db(self, max_depth=0) -> None: 
        # 0 implies no max depth limit
        subreddit_dict = self.get_subreddit_threads()
        for subreddit in subreddit_dict:
            print('\t',subreddit, len(subreddit_dict[subreddit]))
            for tc in subreddit_dict[subreddit]:
                for comment in tc.comments: # for each top-level comment
                    rec_display_comments(comment, 1, max_depth)
                print('\t','|', tc.thread.thread_id, len(tc.comments))