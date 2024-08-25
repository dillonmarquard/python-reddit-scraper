import yaml
import datetime
import argparse
import re

# from itertools import chain

# import praw

import reddit_interface
import db_interface            

import logging

def main():

    # handler = logging.StreamHandler()
    # handler.setLevel(logging.DEBUG)
    # for logger_name in ("praw", "prawcore"):
    #     logger = logging.getLogger(logger_name)
    #     logger.setLevel(logging.DEBUG)
    #     logger.addHandler(handler)

    # a further improvement would be using vault to run the script and collect any secrets within a firewall.
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    parser = argparse.ArgumentParser(prog="Reddit Scraper")
    parser.add_argument("-r", "--subreddit", help = "Choose a subreddit by name or url (eg. python or https://www.reddit.com/r/python/)", required=True)
    parser.add_argument("-U", "--Update", help = "Update the database for the selected subreddit", action='count', default=0)
    parser.add_argument("-p", "--print", help = "Print the database", action='count', default=0)
    parser.add_argument("-d", "--Date", help="Specify the unixtime to pull subreddit data until", default="1704067200.0")
    args = parser.parse_args()

    # we can extract the subreddit the user wants to update here
    subreddit = args.subreddit.lower()
    if 'https://www.reddit.com/r/' in subreddit:
        subreddit = re.findall('https://www.reddit.com/r/(.+)/',subreddit)[0]

    # create the database if it doesnt exist, and connect to it
    db = db_interface.SqLiteDB()

    if args.Update:
        user = config['account']
        # use the api key to access the reddit api
        api = reddit_interface.RedditAPI(user['username'], user['app_name'], user['app_id'], user['secret'])

        # get a list of threads and comments from the reddit api for the specified subreddit
        thread_list, comment_list = api.get_subreddit_data(subreddit, start_date=datetime.datetime.fromtimestamp(float(args.Date)))

        # update the database with the fresh subreddit data 
        db.insert_update_post(thread_list)
        db.insert_update_comment(comment_list)

    if args.print:
        # print the entirety of the database 
        # subreddit
        #   thread list
        #       comment tree
        db.display_db(max_depth=0) # specify the comment tree depth to print (eg. 0 is the entire tree, 1 would print 1 sub-comment)

main()