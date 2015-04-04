Data storage
============

I really liked the talk [Turning the database inside out](http://blog.confluent.io/2015/03/04/turning-the-database-inside-out-with-apache-samza/) and the ideas discussed in there. But to get a better understanding I feel I need to get some hands on experimentation with the concepts.

To start out I want something simple that will represent the datasource, a text file. To get some data there I have a writer.

```python
import datetime
import random

users = ['Anna', 'Panna', 'Dregen', 'Apa', 'Lapa', 'Dapa', 'Dijon']
messages = ['hungry', 'content', 'happy', 'sad', 'glad', 'mad', 'drunk', 'skunker', 'sleepy', 'derpy', 'catter',
            'hatter']


def certainty():
    return str(random.randint(1, 100))


def message():
    return random.choice(messages)


def writer(handle, lines):
    for i in range(lines):
        log_text = "%s\t%s\t%s\t%s\n" % (datetime.datetime.now(), random.choice(users), certainty(), message())
        handle.write(log_text)
```

For initial searching of the data, that would be a select, I just read all the lines and look for lines matching my search term.

```python
def reader(source, search):
	for l in source.readlines():
		if search in l:
			print(l.strip())
```

```
$ ./reader.py commit_log Dijon
->
...
2015-03-25 19:58:04.874321 Dijon 90 sleepy
2015-03-25 19:58:04.874853 Dijon 55 sleepy
2015-03-25 19:58:04.875239 Dijon 98 sad
2015-03-25 19:58:04.875425 Dijon 9 sad
2015-03-25 19:58:04.875741 Dijon 97 sad
```

Simple enough even though I get the full log of all changes that have happened, current and old. Assuming that we would represent a regular database and all the writes to an existing row would be an update we are only interested in the last match.

```python
def reader(source, search):
    match = ""
    for l in source.readlines():
        if search in l:
            match = l
    print match.strip()
```

```
$ ./reader2.py commit_log Dijon
->
2015-03-25 19:58:04.875741 Dijon 97 sad
```

The expectation would be that for even this simple implementation that as the log grows, the time to find the right row increases. In a way this is a bit unfair at the moment since we are actually not updating in place but just growing the commit log for every update. But I imagine this being similar to adding a lot of new users.

Or after growing the log a bit that does not really affect the timing that much. So let's scratch that for now.

What we do know though is that there's been tons of updates to Dijons message and we only see the last one. So if we want to see how all the messages changes over time we would still need to store all of them.

Our data is now growing rapidly so we want to add an index to our log. The indexer takes one of the columns as in data, rearranges the data and then store it as a python object. When updating an existing index we would probably just take the latest changes, read up the index and update with the new data.

```python
import pickle
from collections import defaultdict

valid_indices = {'date': 0, 'name': 1, 'certainty': 2, 'message': 3}
idx = defaultdict(list)


def get_key(col_nbr, line):
    cols = line.split('\t')
    index_key = cols[col_nbr]
    return index_key


def indexer(source, index_key):
    if index_key in valid_indices:
        index_file = "%s_%s.idx" % (index_key, 'index')
        col_nbr = valid_indices[index_key]
        with open(index_file, 'wb') as i:
            for line in source.readlines():
                line = line.strip()
                index_key = get_key(col_nbr, line)
                idx[index_key].append(line)
            pickle.dump(idx, i)
            print("The pickling has been done")
    else:
        print("Invalid index key given")
```

When reading the data we now use the index file as a source and just look up the data based on the key. Unpickling data is really slow though so this is for now a lot slower than the previous version. But this experiment isn't about speed so it doesn't really matter. It's just really noticible when trying it. We can see though that the search for our data is much simpler, we don't have to go through it all. Instead we go directly to the collection of data that interest us.

```python
def index_reader(source, search):
    data = pickle.load(source)
    if search in data:
        print data.get(search)[-1]
    else:
        print ''
```

Even though speed doesn't really matter it becomes slightly annoying using pickle with bigger files. So let's run quick tests with other methods.

Popular storing methods are dumping the dict as a string and reading it with `ast.literal_eval`, and using `json.dump` with `json.loads`

For reference, the size of the test file used is:
```
29M commit_log
```

Just doing a dump of the dictionary as a string increases the size slightly. Below are the timings when using ast.literal_eval.
```
33M message_evalindex.idx

./eval_indexer.py commit_log message  2,76s user 0,40s system 99% cpu 3,163 total

./evalindex_reader.py message_evalindex.idx glad  6,32s user 1,00s system 99% cpu 7,326 total
```

As we can see the json is the same size as the string dump.

```
33M message_jsonindex.idx

./json_indexer.py commit_log message  4,45s user 0,26s system 99% cpu 4,705 total

./json_reader.py message_jsonindex.idx glad  2,67s user 0,19s system 99% cpu 2,855 total
```

So even though it's slightly slower to create the index with json it's faster to read it. And since we are likely to search more than index I'll switch to json.

The changes to the indexer and reader are.
```diff
2d1
< import pickle
4a4
> import json
25,26c24,25
<             pickle.dump(idx, i)
---
>             json.dump(dict(idx), i)
```

```diff
2d1
< import pickle
4c3
<
---
> import json
7c6
<     data = pickle.load(source)
---
>     data = json.loads(source.read())
```

