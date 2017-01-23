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
    "lang":"j",
    "code":"class Main { public static void main() { } }"
  },
  "config": {
    "problem_id":1001,
    "max_time":1000,
    "max_sum_time":10000,
    "max_memory":256,
    "round_id":1
  }
}
```
## Root structure:
```
judge_server
|- submission
|- round
|- data
```

## About Judge
We give exactly two more command line arguments, no matter you are using it or not.
1. the original input path
2. the answer path
3. the new input path (rewrite)

Recall that when you are using C++ or Python, the command arguments start from 1. But
when using Java, command arguments start form 0.

Note that you can only read the output from `stdin` and write the conclusion to `stdout`.

Now let's talk about the protocol Judge should follow when writing conclusions.

#### Judge Protocols
Judge should write exactly one line to `stdout`. As the sentence would be revealed to
user, you probably don't want your sentence to be obscure...

When we are reading the conclusion Judge is trying to tell, we break the sentence into
tokens, ignoring all blanks, commas, and periods. And then, we catch keywords. It means that when Judge writes 'continue',
no matter where it is, the game will continue.

Currently the following phrases are supported (we don't care about upper-lower cases)
```
1. continue
2. stop
3. ok / yes / right / correct (meaning score 100)
4. no / wrong (meaning score 0)
5. scored / scores / score <integer> (from 0 to 100)
6. idleness limit exceeded (score 0 and stop)
```
Rule #6 basically means that the program does nothing or does something weird that Judge cannot understand. :)

Now consider a rare case in which you write:
```
Your idea is correct, but you did something wrong. So you scored 50.
```
In which case we will match **bottom-up**. Note that the sentence match Rule #5, so it has already scored 50.
No matter it is 'correct' or 'wrong', it will be 50.

If there were to be some terrible accident that makes Judge unhappy and even angry,
don't worry, we will take care of that. Even if you don't write anything, it will still
seems to be functioning properly. But we will post a notice about the accident
and you have to do something about that.