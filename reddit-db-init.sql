CREATE TABLE IF NOT EXISTS Thread (
    thread_id TEXT PRIMARY KEY,
    subreddit_id TEXT,
    original_post TEXT,
    username TEXT,
    upvotes INTEGER,
    post_date REAL,
    url TEXT
);

CREATE TABLE IF NOT EXISTS Comment (
    comment_id TEXT PRIMARY KEY,
    thread_id TEXT,
    parent_id TEXT,
    username TEXT,
    upvotes INTEGER,
    post_date REAL,
    comment TEXT
);

CREATE TABLE IF NOT EXISTS Subreddit (
    subreddit_id TEXT PRIMARY KEY,
    subreddit_name TEXT
);