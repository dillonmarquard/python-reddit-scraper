# Reddit Data Pipeline

## Setup

python: 3.9.17
pyyaml: 6.0.2

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