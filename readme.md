# AI Playground Webserver

Webserver for AI Playground.

**Current Version:** webserver: v1; server_base: v1

## What can it do?

1. Upload test data to it

2. Send pretest request to it

3. Send judge request to it

## Tutorial of installation
The installation is very simple. (under good web condition of course)

**Step 1:** clone the repository, and install [Docker](https://www.docker.com/).

**Step 2:** create `local_config.py` to change the token by adding `TOKEN = '<your token>'` (**IMPORTANT!!!**)

**Step 3:** run `sudo ./install_dependencies.sh`. (very slow, if you have run this in current version, skip this step)

**Step 4:** have a cup of tea or coffee...

**Step 5:** run `sudo ./install.sh`

**Step 6:** `sudo docker run -it -p 4999:4999 aiplay/webserver:v1`

And if nothing ridiculous pops out, done!

**Tips:** You can use `Ctrl + P + Q` to have your terminal back. For advanced usage,
learning a tutorial about docker is strongly recommended. :)


## The first thing you probably want to know
### ROOT
`su` before running everything!

Don't worry that root permission will blow your system. 
Everything which is possible to be dangerous will be carefully controlled.
And since the whole system is running on docker......

### Fail in Judger unittests
It is ok if you fail in 1-2 tests.

### What is pretest?
This is a question you should ask [Codeforces](http://codeforces.com/). "Sort of like that".


## How to use it

### Check server status (token NOT required)
The following is returned when GET `<hostname>/info` page.
* status (ok/failure)
* error (empty if none)
* system version
* cpu info
* memory info
* g++ version
* java version
* python3 version
* whether redis and celery are running (if not, status is failure)

### Tokens

Remember I told you to modify `setup.py`? This is where the token comes up. Every requests sent to webserver
should have an authorization in its header. With Python, this is very easy:
```python
import requests
requests.post(url, data=something, auth=('token', TOKEN)).json()
requests.post(url, json=something, auth=('token', TOKEN)).json()
```

### Responses

I chose to write responses before requests because, believe it or not, I feel this is more important.

Responses will all be in json. The first thing you should check, is `status`. If it is 'received', then okay.
Otherwise, sadly, something is wrong. You should check your token or whether you are sending data in a correct method.

You can check `code` if you are sending a judge or pretest request. The `code` standard can be found in `config.py`.
But for convenience, I copied it here.
```python
ERROR_CODE = {
    -100: 'Finished',
    -3: 'Correct',
    -2: 'OK',
    -1: 'Wrong Answer',
    0: 'Pretest Passed',
    1: 'Time Limit Exceeded',
    2: 'Time Limit Exceeded',
    3: 'Memory Limit Exceeded',
    4: 'Runtime Error',
    5: 'System Error',
    6: 'Compile Error',
    7: 'Idleness Limit Exceeded',
    8: 'Pretest Failed',
    9: 'Sum Time Limit Exceeded'
}
```
The `message` field, which can be very long, shows a 'brief' report of what happened. It's in markdown, and polished
for human reading. It's recommended that this can be shown in the final webpage.

The `score` field, if exists, is simply a record of how everyone has performed in the past contest.

### Requests

#### Request of main test (post, json)
Sent to `<hostname>/judge`.

Main tests run rounds on each input data for these selected programs. The finally score is summed by partial score
multiplied by numbers predefined in `data.conf`. If it is a OI/ACM problem, it is actually a simplified (solo) version
of that.

Language can be 'cpp' for C++11, 'java' for Java 7, 'python' for Python 3, 'builtin' for built-in programs.

To know more about built-in programs, see below.
```json
{
  "submissions":[
    {
      "id":100,
      "lang":"cpp",
      "code":"int main(){}"
    },
    {
      "id":101,
      "lang":"python",
      "code":"print('!')"
    }
  ],
  "judge": {
    "id":200,
    "lang":"java",
    "code":"class Main { public static void main() { } }"
  },
  "pretest_judge": {
    "lang":"builtin",
    "code":"testlib/checker/int_ocmp.py"
  },
  "config": {
    "problem_id":1001,
    "max_time":1000,
    "max_sum_time":10000,
    "max_memory":256
  }
}
```
Actually many parts of this json is optional. But we don't recommend you to be lazy, because it will be
extremely confusing and error-leading.

#### Request of pretest (post, json)
Sent to `<hostname>/test`.

It is roughly the same. Note that 'submission' is not 'submissions', 'judge' is not 'pretest_judge'.
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

#### Request of updating data (post, data)

Write the zip file **directly** in the data. Additional information is hidden in url.

##### URL
* `<hostname>/upload/data/1002` means it is the data of problem 1002
* `<hostname>/upload/pretest/1003` means it is the pretest data of problem 1003

##### Data
A zip file in which there is nothing but data files. It will look like:
```
- input1.txt
- input2.txt
- output1.txt
- output2.txt
- data.conf
```
Since Python has a weird `zipfile`, generate such a zip can be not so easy. Here is my solution.
```python
import zipfile, os

def add_dir_to_file(source_dir, target_path):
    f = zipfile.ZipFile(target_path, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(source_dir):
        for filename in file_names:
            real_path = os.path.join(dir_path, filename)
            f.write(real_path, arcname=os.path.relpath(real_path, source_dir))
    f.close()
```

## Tools to prepare problems and contests

### Write a judge (or checker if you prefer)
We give exactly two more command line arguments, no matter you are using it or not.

1. the original input path

2. the answer path

3. the new input path (rewrite)

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
3. ok / yes / right / correct (meaning score 100 percent)
4. no / wrong (meaning score 0 percent)
5. points / scored / scores / score <integer> (from 0 to 100 percent)
6. idleness limit exceeded (score 0 and stop)
```
Rule #6 basically means that the program does nothing or does something weird that Judge cannot understand. :)

Note that all the things you write as quotes (`'...'`) are ignored.

Now consider a rare case in which you write:
```
Your idea is correct, but you did something wrong. So you scored 50.
```
In which case we will match **bottom-up**. Note that the sentence match Rule #5, so it has already scored 50.
No matter it is 'correct' or 'wrong', it will be 50.

If there were to be some terrible accident that makes Judge unhappy and even angry,
don't worry, we will take care of that. Even if you don't write anything, it will still
seems to be functioning properly. But participants may not be happy to see their programs score 0.

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

### Powerful tools: testlib in Python

In the include dir, there is a testlib included. This testlib is not the famous one written by Russian.
I have to admit that the original one is powerful and classical, but it is too long and I am too stupid to use it.
Therefore I use Python to write a similar testlib with no more than 500 lines of code. :)

I'm going to use something once said in the original testlib: `The best way to use it is to read it.` Classes like
`Inputstream` and `Compare` would save you much time when writing Judge. But at the same time, if you can being lazy,
you can just use the checkers **built-in**.

Now it is time that we talk about built-in programs.

### Built-in programs

We have few built-in programs nowadays, mostly checkers. But in the future, I hope that more and more programs, about
different functions, can be included. INCLUDE_DIR is already included in `CPLUS_INCLUDE_PATH` and `PYTHON_PATH`, so it
is easy for you to include them in your own work. For Java, well, it is a little tricky, still working on that...

The coolest thing is that you can even pass a built-in program directly to judge, without writing any code.
`'id'` can be empty if you like, `'lang'` should be 'builtin', `'code'` is the relative path in INCLUDE_DIR. Done!


## More Components

### Judger
A Python 3 improved version of QDUOJ Judger. Special thanks to them. And see README in Judger for detail.

Java memory is N/A after the improvement for C++ and Python. I was hoping that someone can write a new Judger.

### Unittest
Running unittest is both a good way of checking and seeing what's going on. I hope code in unittest
may help you write the code in client-server.

Tips to run test: add local_config.py to your directory contain the following:
```python
URL = '<your url>'
TOKEN = '<your token>'
```

### Redis and Celery
A stupid way to run async tasks. You can safely ignore it.

### Docker
It might be convenient to build a image of installed version of webserver. I guess that is a future plan?
