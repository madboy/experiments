Lua coroutines
==============
#### Introduction

Reading chapter 9 from [Programming in Lua](http://www.amazon.com/exec/obidos/ASIN/859037985X/lua-pilindex-20)
#### Life of a coroutine

I create a coroutine which starts out in a suspended state. The first time I resume it runs the function body which in this case is just to print the words "I will soon be dead" after that is done the coroutine has nothing more to do, and will switch state over to dead. So when we try to resume again the coroutine will let us know that it's dead and nothing more will happen.

```lua
co = coroutine.create(function () 
	print("I will soon be dead") 
end)
```

```lua
print(coroutine.status(co))
-> suspended

coroutine.resume(co)
-> I will soon be dead

print(coroutine.status(co))
-> dead
```

#### Yield

Using yield we can have a coroutine that lives a litte longer. The coroutine will run until the first yield and then stop in it's track. Successive resumes will continue after that yield until the next yield.

```lua
co = coroutine.create(function ()
	coroutine.yield("This will be yielded first")
	coroutine.yield("This will be yielded on the second resume")
end)
```

```lua
print(coroutine.resume(co))
-> This will be yielded first

print(coroutine.resume(co))
-> This will be yielded on the second resume
```

#### Producer and consumer

The next part is a minimally modified Listing 9.1 from the chapter.

Let's say we have something spitting out a sequence of numbers, the `producer`. The producer is a coroutine so that each time we call it we'd get the next number. We then have a `consumer` that can use any type of producer, all it expects is that the producer is a coroutine so that `receive` can do a `coroutine.resume` to get the next number. The consumer will then take some action on the received value, in this case just printing it.

This setup aslo allows us to introduce a `filter` in the chain, as long as it follows the expectation of a producer. So the filter need to be a coroutine.

```lua
function receive (prod)
	local status, value = coroutine.resume(prod)
	return  value
end

function producer ()
	return coroutine.create(function ()
		for i = 1, math.huge do
			coroutine.yield(i*i)
		end
	end)
end

function filter (prod)
	return coroutine.create(function ()
		for line = 1, math.huge do
			local val = receive(prod)
			val = string.format("%d: %s", line, val)
			coroutine.yield(val)
		end
	end)
end

function consumer (prod)
	for i = 1, 5 do
		local val = receive(prod)
		print(val)
	end
end
```

```lua
consumer(producer())
-> 1
-> 4
-> 9
-> 16
-> 25
```

```lua
consumer(filter(producer()))
-> 1: 1
-> 2: 4
-> 3: 9
-> 4: 16
-> 5: 25
```

Using the producer for a stop criteria requires that you have a snapshot in time.

```lua
function receive (it)
	local status, value = coroutine.resume(it)
	return value
end

function producer ()
	return coroutine.create(function ()
		for i = 1, 3 do
			coroutine.yield(i)
		end
	end)
end
```

So the below will give three apa since we will call the same coroutine until it gives nil.

```lua
local p = producer()

while receive(p) do
	print("apa")
end
```

While this will give an infinite loop since we are just getting 1 over and over again since we
are calling a new coroutine for each iteration.

```lua
while receive(producer()) do
	print("apa")
end
```

The small change of making `receive` return a function allows you to use it as an iterator

```lua
function receive (it)
	return function ()
		local status, value = coroutine.resume(it)
		return value
	end
end

for p in receive(producer()) do
	print(p)
end

-> 1
-> 2
-> 3
```

Can this be used for anything more exiting?

Let's say we want an iterator that will give us the next fibonacci number up to a given number. We first write the `fib` function so that we can get the numbers. Then all we need to do is create a receiver/iterator producer pair around that function.

```lua
function fib (n)
	if n <= 0 then
		return 0
	elseif n == 1 then
		return 1
	else
		return fib(n - 1) + fib(n - 2)
	end
end

function fibonacci (n)
	-- producer
	local co = coroutine.create(function ()
		for i = 0, n do
			coroutine.yield(fib(i))
		end
	end)
	-- receiver/iterator
	return function ()
		local status, value = coroutine.resume(co)
		return value
	end
end

for f in fibonacci(20) do
	print(f)
end

-> 0
-> 1
-> 1
-> ...
-> 4181
-> 6765
```

Or even more compact using `coroutine.wrap`.

```lua
function fibonacci (n)
    return coroutine.wrap(function ()
        for i = 0, n do
            coroutine.yield(fib(i))
        end
    end)
end
```

#### Dispatch

The example of downloading files (Listing 9.4) introduces a bit too many parts for my taste. I would prefer to only focus on the dispatcher it self. So I switch getting a file to be a simple number-spitter-outer, and a name so that we can see which coroutine is currently giving us data.

The `generator` sets up a coroutine that will last for n number of resumes, but instead of returning a function that resumes we insert the coroutine into a table.

The `dispatcher` will use that table to go through our coroutines in turn until all of them run out. We first check if we have reached the end of the queued coroutines and if so switch back to the first one. If the first one would prove empty as well we are done and should break out of the loop. We then resume the current coroutine, and check the status afterwards. If we get false that coroutine is done and we can remove it from the queue. `table.remove` reorders the items in the table so we'll have no gaps. Last we just updatde the position in the queue to look at next.

```lua
threads = {}

function generator (name, n)
    local co = coroutine.create(function ()
        for i = 1, n do
            coroutine.yield(print(name, ":", i))
        end
    end)
    table.insert(threads, co)
end

function dispatcher ()
    local i = 1
    while true do
        if threads[i] == nil then
            if threads[1] == nil then break end
            i = 1
        end
        local status, res = coroutine.resume(threads[i])
        if status == false then
            table.remove(threads, i)
        end
        i = i + 1
    end
end

generator("eskil", 2)
generator("kjell", 4)
generator("io", 3)

dispatcher()
```

```
-> eskil   :   1
-> kjell   :   1
-> io  :   1
-> eskil   :   2
-> kjell   :   2
-> io  :   2
-> kjell   :   3
-> io  :   3
-> kjell   :   4
```

#### Tail

```lua
function read_to_end (file)
	io.input(file)
    io.read("*a")
end

function read_line(file, filename)
    io.input(file)
    local line = io.read("*l")
    if line then
        if print_name then
            print("--------", filename, "---------")
        end
        print(line)
    end
end

files = {}

print_name = false
if #arg > 1 then print_name = true end

for i = 1,#arg do
    local f = {name=arg[i]}
    f.file = io.open(f.name)
    table.insert(files, f)
end

for k,f in pairs(files) do
    read_to_end(f.file)
end

while true do
    for k,f in pairs(files) do
        read_line(f.file, f.name)
    end
end
```

```
--------        slask   ---------
slask: 2015-03-22 17:34:05
--------        slask   ---------
slask: 2015-03-22 17:34:06
--------        slosk   ---------
slosk: 2015-03-22 17:34:06
```

```lua
function generator (file, filename)
	local co = coroutine.create(function ()
		while true do
			io.input(file)
			local line = io.read("*l")
			if line then
				if print_name then
					print("--------", filename, "---------")
				end
				coroutine.yield(line)
			else
				coroutine.yield()
			end
		end
	end)
	table.insert(threads, co)
end

function dispatcher ()
	while true do
		for k, t in pairs(threads) do
			local s, l = coroutine.resume(t)
			if s and l then
				print(l)
			end
		end
	end
end

threads = {}

for k,f in pairs(files) do
	generator(f.file, f.name)
end

dispatcher()
```
