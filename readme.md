```
pip install -r requirements.txt
sudo apt-get install redis-server
redis-server
```
```
celery worker -A aipWebserver.celery --loglevel=info
```
```
sudo groupadd compiler
sudo useradd -g compiler compiler
```
request json, response is written to sql directly
```json
{
  "total_submissions":2,
  "submission":[
    {
      "language":2,
      "code":"int main(){}"
    },
    {
      "language":3,
      "code":"print(!)"
    }
  ],
  "problem_id":1001,
  "max_time":1000,
  "max_sum_time":10000,
  "max_memory":256,
  "round_id":1
}
```