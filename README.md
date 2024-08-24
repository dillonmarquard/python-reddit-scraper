# Reddit Data Pipeline

## Setup

python: 3.9.17    
pyyaml: 6.0.2   
praw: 7.7.1    
  
```  
pip install -r requirements.txt
```  

### Authentication  
We will use config.yaml to store our api secret in the following format.   
You can create (private script) app here (https://www.reddit.com/prefs/apps) to obtain credentials.   
  
(config.yaml)
```YAML  
account:  
    username: <username>
    app_name: <app name>
    app_id: <app id>  
    secret: <client secret>  
```

### Example Commands

```PYTHON
# pulls data for the python subreddit since Aug 20th, 2024 and pretty prints the database to the command line.
python app.py -r python -U -p -d 1724137200
```

### Future Considerations
* improve throughput despite api rate-limiting