# AI Playground Webserver

## Preparation (obscure)

```
pip install -r requirements.txt
sudo apt-get install redis-server
redis-server
```
```
celery worker -A config.celery --loglevel=info
```
```
sudo groupadd compiler
sudo useradd -g compiler compiler
```
There is also directories needed to create. I included them in `setup.py`. In the future, I hope
`sudo python3 setup.py`
will all do.

## ROOT
`su` before running everything
## JSON

request json, result is written to file
```json
{
  "total_submissions":2,
  "submissions":[
    {
      "id":100,
      "lang":"c",
      "code":"int main(){}"
    },
    {
      "id":101,
      "lang":"p",
      "code":"print('!')"
    }
  ],
  "judge": {
    "id":200,
    "language":"j",
    "code":"class Main { public static void main() { } }"
  },
  "problem_id":1001,
  "max_time":1000,
  "max_sum_time":10000,
  "max_memory":256,
  "round_id":1
}
```
## Root structure:
```
aipWebserver
|- submission
|- round
|- data
|- compile
```
## About the compiler
When the compiler is called, the client needs to fill in the 
blanks of "compile config", "src_path" and "submission_id".
And after the compiler is called, at most 3 files will be generated. Namely,
"{id}" for the program, "{id}.out" for the error message, "{id}.log" for whatever.
