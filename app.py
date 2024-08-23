import yaml
import datetime
import argparse
import re

import reddit_interface
import db_interface

def main():

    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--Subreddit", help = "Choose a Subreddit by name (eg. python)", required=True)

    args = parser.parse_args()

    subreddit = args.Subreddit.lower()

    print(subreddit)

    user = config['account']

    api = reddit_interface.RedditAPI(user['username'], user['app_name'], user['app_id'], user['secret'])
    print(api)

    thread_list, comment_list = api.get_subreddit_data(subreddit, start_date=datetime.datetime(2024,8,18))
    print(thread_list)
    print(comment_list)

    db = db_interface.SqLiteDB()
    db.insert_update_post(thread_list)
    db.insert_update_comment(comment_list)

main()