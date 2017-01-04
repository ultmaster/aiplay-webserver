```
pip install -r requirements.txt
sudo apt-get install redis-server
redis-server
```
```
celery worker -A aipWebserver.celery --loglevel=info
```