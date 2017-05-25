# Bio Backend

See [Bio Client](https://github.com/kyledotterrer/bio-client) as well

### Installation

This microservice is based off of Python 3. If you don't have it:
```
brew install python3
```
Now python3 will be an alias to the default python command.

In the top level directory, create a file called `.env` with the following in it:
```
export FLASK_APP="$(pwd)/app/autoapp.py"
export FLASK_DEBUG=1
```

Install and configure virtualenv:

```
pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Usage

Make sure that you are always running inside virtualenv:
```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Run locally:
```
source .env
flask run
```

### Deployment for heroku servers
```
gunicorn manage:app
```

### Relevant Documentation
1. [Flask](http://flask.pocoo.org/docs/0.12/)
1. [Pymongo](https://api.mongodb.com/python/current/index.html)
1. [Mongothon](https://github.com/gamechanger/mongothon)
1. [Kegg Parser](https://pythonhosted.org/bioservices/references.html#bioservices.kegg.KEGGParser)
	- [Tutorial](https://pythonhosted.org/bioservices/kegg_tutorial.html)
1. [Flask starter](https://github.com/jason-feng/flask-api-starter-app) 
