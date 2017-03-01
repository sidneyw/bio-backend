# Bio Backend

See [Bio Client](https://github.com/kyledotterrer/bio-client) as well
### Installation

This microservice is based off of Python 3. If you don't have it:
```
brew install python3
```
Now python3 will be an alias to the default python command.

Make sure that you are always running this inside virtualenv

```
pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Usage

```
source .env
flask run
```

### Deployment for heroku servers
```
gunicorn manage:app
```
