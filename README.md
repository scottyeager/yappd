# yappd

This is a persistent dictionary like object in Python based on `jsonpickle` and `sqlite3`. You store values in it like a normal `dict` and they are written to disk automatically. When you load it up again later, everything is like you left it.

## Why?

Pickling objects in Python has some major downsides. With `jsonpickle` we get human readable output that can always be loaded, even if the original classes aren't around in the current scope.

But why not just store the resulting JSON to disk in a text file? Well, it turns out that reliably updating files on disk in an atomic way is not so easy. SQLite has this covered and is a no brainer choice for storing app data on disk.

That said, if you don't need SQL features, then adopting a database brings a lot of extra hassle (even with an ORM). The implementation of yappd means we can just shove arbitrary objects into the disk and get them back later. There's no need to perform a database migration if you decide later that every `Pet` object should have a `favorite_food` field.

## How to use it?

No package yet. For now you can just drop (or symlink) the file from this repo into your project and make sure to install `jsonpickle`:

```
pip install jsonpickle
```

Then import and use PDict:

```python
from pdict import PDict
p = PDict('mydata')
p['hello'] = 'world'
```

Each PDict needs a file to write its data into, and the path to the file is the first argument to the constructor. An optional second argument is the dictionary name, which allows multiple dictionaries to be stored in the same file. By default the name `default` used:

```python
p1 = PDict('mydata', 'default') # Equivalent to example above
p2 = PDict('mydata', 'p2') # This one uses p2 as the name so there's no conflict
```
