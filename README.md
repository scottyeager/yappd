# Yappd

Yappd is a persistent dictionary like object in Python based on [`jsonpickle`](https://github.com/jsonpickle/jsonpickle) and `sqlite3`. You store values in it like a normal `dict` and they are written to disk automatically. When you load it up again later, everything is like you left it.

It can store any object that's supported by `jsonpickle` ("almost any Python object"), including nested structures.

Since Yappd maintains a regular Python `dict` under the hood, it's only suitable for data sets that can be kept in RAM (whatever you'd normally use a `dict` for).

## How to use it?

Just install with `pip` (into a venv of course):

```
pip install yappd
```

Then import and use PDict:

```python
from yappd import PDict
p = PDict('mydata')
p['hello'] = 'world'

p = PDict('mydata') # Load it from disk again
p['hello'] == 'world' # True
```

Each PDict needs a file to write its data into, and the path to the file is the first argument to the constructor. An optional second argument is the dictionary name, which allows multiple dictionaries to be stored in the same file. By default the name `default` used:

```python
p1 = PDict('mydata', 'default') # Equivalent to example above
p2 = PDict('mydata', 'p2') # This one uses p2 as the name so there's no conflict
```

Most `dict` functions are implemented and are usually just proxies to the underlying `dict` object.

## Caveat, data mutation

There's a major caveat to keep in mind, which is mutable data types. Take this usage for example:

```python
p = PDict('mydata')

p['mylist'] = []
p['mylist'].append(1)
p['mylist'] == [1] # True

p = PDict('mydata') # Reload the dict from disk
['mylist'] == [] # True. Change not stored to disk
```

At this point the value stored on disk for `mylist` is an empty list, but the value stored in the program memory is `[1]`. Since yappd can't detect if stored values are mutated, you must explicitly store any mutated values again to update them on disk.

The `save` function is provided for this purpose:

```python
p = PDict('mydata')

p['mylist'] = []
p['mylist'].append(1)
p.save('mylist')
p['mylist'] == [1] # True

p = PDict('mydata') # Reload the dict from disk
p['mylist'] == [1] # True. This time it's okay
```

You can also call `save` with no arguments to save all values. It's more efficient though to specify which values to save.

## Why?

Pickling objects in Python has some major downsides. With `jsonpickle` we get human readable output that can always be loaded, even if the original classes aren't around in the current scope.

But why not just store the resulting JSON to disk in a text file? Well, it turns out that reliably updating files on disk in an atomic way is not so easy. SQLite has this covered and is a no brainer choice for storing app data on disk.

That said, if you don't need SQL features, then adopting a database brings a lot of extra hassle (even with an ORM). The implementation of yappd means we can just shove arbitrary objects into the disk and get them back later. There's no need to perform a database migration if you decide later that every `Pet` object should have a `favorite_food` field.