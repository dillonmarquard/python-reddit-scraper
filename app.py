import yaml
import datetime

import reddit_interface

def main():

    with open("config.yaml", 'r') as stream:
        data = yaml.safe_load(stream)

    user = data['account']

    # pull from cli
    dt = datetime.date.fromisoformat("2024-01-01")
    print(dt)

    api = reddit_interface.RedditAPI(user['username'], user['app_name'], user['app_id'], user['secret'])

main()