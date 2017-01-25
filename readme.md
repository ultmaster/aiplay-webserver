# AI Playground Webserver

## Preparation (obscure)
### ROOT
`su` before running everything
### Important: install judger
```
cd include/judger && ./runtest.sh
```
**Done!**

Note: it is ok if you fail in 1-2 tests.
### Requirements
```
pip install -r requirements.txt
sudo apt-get install redis-server
```
```
# not using yet
sudo groupadd compiler
sudo useradd -g compiler compiler
```
### Do this before you run things
```
redis-server (working backstage if you prefer)
celery worker -A config.celery --loglevel=info
```
### Future plans
There is also directories needed to create. I included them in `setup.py`. In the future, I hope
`sudo python3 setup.py`
will all do.


## JSON
#### Request of main test
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
  "pretest_judge": {
    "id":-1,
    "lang":"ncmp"
  },
  "config": {
    "problem_id":1001,
    "max_time":1000,
    "max_sum_time":10000,
    "max_memory":256
  }
}
```
Note that pretest judge is optional. We will use judge for default.
#### Request of pretest
```json
{
    "submission":{
        "id":104,
        "lang":"c",
        "code":"..."
    },
    "judge": {
        "id":200,
        "lang":"c",
        "code":"..."
    },
    "config": {
        "problem_id":1001,
        "max_time":1000,
        "max_sum_time":10000,
        "max_memory":256
    }
}
```
## Judge working structure
```
judge_server
|- submission
|- round
|- data
|- pretest
```

## About Judge
We give exactly two more command line arguments, no matter you are using it or not.

1. the original input path

2. the answer path

3. the new input path (rewrite)

4. `pretest` for pretests; `main` for opposite cases

Recall that when you are using C++ or Python, the command arguments start from 1. But
when using Java, command arguments start form 0.

Note that you can only read the output from `stdin` and write the conclusion to `stdout`.

Now let's talk about the protocol Judge should follow when writing conclusions.

### Judge Protocols
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

### Pretest
If you want programs to run some pretests before running on the main tests, in order to prevent ILE(?), you 
then need to upload some pretest data.

### Data directory format:
Input file should contain 'input' or use suffix name '.in'. Output file should contain 'output', 'answer' or use
suffix name '.out' or '.ans'. Bound input and output files should be exactly same except the differences mentioned
above. You should definitely not use name like 'input' for an output file to prevent potential errors.

I really hate IGNORE_CASE problem. Sometimes it does; sometimes it does not. Leave me alone...

### Weight on each test case
It means that each test case can have a weight when summing up. The default value is 10, meaning that
participants will get a score on the scale of 0 to 10 in this test case. This value can be customized,
by adding `data.conf` into following into data directory:
```json
{
  "input1.txt": 20,
  "input2.txt": 30,
  "input3.txt": 50
}
```
