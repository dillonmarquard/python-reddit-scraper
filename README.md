# Reddit Data Pipeline

## Setup

python: 3.9.17  
pyyaml: 6.0.2  
sqlite3: 3.41.2  
praw: 7.7.1  

### Authentication
We will use config.yaml to store our api secret in the following format.  
You can create an app here (https://www.reddit.com/prefs/apps).  
  
config.yaml
```YAML  
account:  
    username: <username>
    app_name: <app name>
    app_id: <app id>  
    secret: <client secret>  
```

### To-do
* output tables to cli
* unit test
* use postgres (in a docker container)