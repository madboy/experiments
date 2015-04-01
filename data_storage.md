Data storage
============

I really liked the talk [Turning the database inside out](http://blog.confluent.io/2015/03/04/turning-the-database-inside-out-with-apache-samza/) and the ideas discussed in there. But to get a better understanding I feel I need to get some hands on experimentation with the concepts.

To start out I want something simple that will represent the datasource, a text file. To get some data there I have a writer.

```python
import datetime
import random

users = ['Anna', 'Panna', 'Dregen', 'Apa', 'Lapa', 'Dapa', 'Dijon']
messages = ['hungry', 'content', 'happy', 'sad', 'glad', 'mad', 'drunk', 'skunker', 'sleepy', 'derpy', 'catter', 'hatter']

def certainty():
	return str(random.randint(1, 100))

def message():
	return random.choice(messages)

def writer(handle, lines):
    for i in range(lines):
        log_text = "%s %s %s %s\n" % (datetime.datetime.now(), random.choice(users), certainty(), message())
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

Simple enough even though I get the full log of all changes that have happened, current and old. Assuming that we would represent a regular database and all the writes to an existing row would be an update we're only interested in the last match.

```python
def reader(source, search):
	s = open(source, 'r')
    match = ""
	for l in s.readlines():
		if search in l:
			match = l
	print match
```

```
$ ./reader commit_log Dijon
->
2015-03-25 19:58:04.875741 Dijon 97 sad
```

The expectation would be that for even this simple implementation that as the log grows, the time to find the right row increases. In a way this is a bit unfair at the moment since we are actually not updating in place but just growing the commit log for every update. But I imagine this being similar to adding a lot of new users.

Or after growing the log a bit that does not really affect the timing that much. So let's scratch that for now.

What we do know though is that there's been tons of updates to Djons message and we only see the last one. So if we want to see how all the messages changes over time we would still need to store all of them.

Our data is now growing rapidly so we want to add an index to our log. The indexer takes one of the columns as indata, rearranges the data and then store it as a python object. When updating an existing index we would probably just take the latest changes, read up the index and update with the new data.

```python
valid_indices = ['date', 'name', 'certainty', 'message']

def indexer(filename, index):
	if valid_indices.count(index):
		f = open(filename, 'r')
		index_file = "%s_%s.idx" % (index, 'index')
		i = open(index_file, 'wb')
		idx = {}
		for line in f.readlines():
			cols = line.split(' ')
			row = {'date': ' '.join(cols[0:2]),
				'name': cols[2],
				'certainty': cols[3],
				'message': cols[4].rstrip()}
			index_key = row[index]
			if idx.get(index_key):
				idx[index_key].append(line.strip())
			else:
				idx[index_key] = [line.strip()]
		pickle.dump(idx, i)
		i.close()
		print("The pickling has been done")
	else:
		print("Invalid index key given")
```

When reading the data we now use the index file as a source and just look up the data based on the key. Unpickling data is really slow though so this is for now a lot slower than the previous version. But this experiment isn't about speed so it doesn't really matter. It's just really noticible when trying it. We can see though that the search for our data is much simpler, we don't have to go through it all. Instead we go directly to the collection of data that interest us.

```python
def index_reader(source, search):
	import pickle
	s = open(source, 'rb')
	data = pickle.load(s)
	print data[search][-1]
```
