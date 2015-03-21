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
