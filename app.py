import yaml
import datetime

import reddit_interface
import db_interface

def main():

    with open("config.yaml", 'r') as stream:
        data = yaml.safe_load(stream)

    user = data['account']

    api = reddit_interface.RedditAPI(user['username'], user['app_name'], user['app_id'], user['secret'])
    print(api)

    thread_list, comment_list = api.get_subreddit_data("python", start_date=datetime.datetime(2024,8,18))
    print(thread_list)
    print(comment_list)

    db = db_interface.SqLiteDB()
    db.insert_update_post(thread_list)
    db.insert_update_comment(comment_list)

main()