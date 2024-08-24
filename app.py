import yaml
import datetime
import argparse
import re

import reddit_interface
import db_interface            

import logging

def main():

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    for logger_name in ("praw", "prawcore"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    parser = argparse.ArgumentParser(prog="Reddit Scraper")
    parser.add_argument("-r", "--subreddit", help = "Choose a subreddit by name or url (eg. python or https://www.reddit.com/r/python/)", required=True)
    parser.add_argument("-U", "--Update", help = "Update the database for the selected subreddit", action='count', default=0)
    parser.add_argument("-p", "--print", help = "Print the database", action='count', default=0)
    parser.add_argument("-d", "--Date", help="Specify the unixtime to pull subreddit data until", default="1704067200.0")
    args = parser.parse_args()

    subreddit = args.subreddit.lower()
    if 'https://www.reddit.com/r/' in subreddit:
        subreddit = re.findall('https://www.reddit.com/r/(.+)/',subreddit)[0]

    
    db = db_interface.SqLiteDB()

    if args.Update:
        user = config['account']
        api = reddit_interface.RedditAPI(user['username'], user['app_name'], user['app_id'], user['secret'])

        thread_list, comment_list = api.get_subreddit_data(subreddit, start_date=datetime.datetime.fromtimestamp(float(args.Date)))
        db.insert_update_post(thread_list)
        db.insert_update_comment(comment_list)

    if args.print:
        db.display_db(max_depth=0)

    

main()