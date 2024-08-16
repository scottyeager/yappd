from pdict import PDict

# Storing and retrieving values
p = PDict("test.db")

p[1] = 1
assert p[1] == 1

p = PDict("test.db")
assert p[1] == 1

# Update function
p.update({2: 2, 3: 3})

assert p[2] == 2
assert p[3] == 3

p = PDict("test.db")
assert p[1] == 1
assert p[2] == 2
assert p[3] == 3

# Deleting values
del p[1]
del p[2]
del p[3]

assert p._dict == {}

p = PDict("test.db")
assert p._dict == {}

# Storing custom classes

class Test:
    pass

t = Test()
t.l = []
t.i = 0

p['test'] = t
assert p['test'] == t

# Saving mutations

t.l.append(1)
t.i = 1

p.save()

p = PDict("test.db")
t = p['test']
assert t.l == [1]
assert t.i == 1

t.i = 2
p.save('test')

p = PDict("test.db")
t = p['test']
assert t.i == 2