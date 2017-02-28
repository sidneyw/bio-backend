# NLP Backend

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

To setup spacy:
```
python -m spacy.en.download all
```

### Usage

```
source .env
flask run
```

### Test
```
flask test
```

### Curl Testing APIs
```
curl -X POST -H "Content-Type: audio/wav" --data-binary @/Users/jasonfeng/Downloads/emilia_clark_trim.wav localhost:5000/voice/tone
```


### Deployment for heroku servers
```
gunicorn manage:app
```
