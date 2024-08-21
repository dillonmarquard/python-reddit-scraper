# Reddit Data Pipeline

## Setup

### Authentication
We will use secrets.yaml to store our api secret in the following format.
You can create an app here (https://www.reddit.com/prefs/apps).

``` (secrets.yaml)
accounts:  
    <username>:  
        client: <client id>  
        secret: <client secret>  
```