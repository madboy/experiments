Lua coroutines
==============

I create a coroutine which starts out in a suspended state . The first time I resume it runs the function body which in this case is just to print the words "I will soon be dead" after that is done the coroutine has nothing more to do, and will switch state over to dead. So when we try to resume again the coroutine will let us know that it's dead and nothing more will happen.

```
co = coroutine.create(function () 
	print("I will soon be dead") 
end)
```
