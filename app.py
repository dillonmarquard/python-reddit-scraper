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

    thread_list, comment_list = api.get_threads("python", start_date=datetime.datetime(2024,8,18))
    print(thread_list[1])
    print(comment_list[1])

    db = db_interface.SqLiteDB()
    db.insert_update_post(thread_list)
    db.insert_update_comment(comment_list)

main()