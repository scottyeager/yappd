import os
from yappd import PDict

DBFILE = "test.db"

class Test:
    pass

def clean():
    for file in DBFILE, DBFILE + "-shm", DBFILE + "-wal":
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

# Storing and retrieving values
def test_basic():
    clean()
    p = PDict(DBFILE)

    p[1] = 1
    assert p[1] == 1

    p = PDict(DBFILE)
    assert p[1] == 1

    clean()

# Update function
def test_update():
    clean()
    p = PDict(DBFILE)
    p.update({1: 1, 2: 2, 3: 3})

    assert p[1] == 1
    assert p[2] == 2
    assert p[3] == 3

    p = PDict(DBFILE)
    assert p[1] == 1
    assert p[2] == 2
    assert p[3] == 3

    clean()

# Deleting values
def test_delete():
    clean()
    p = PDict(DBFILE)
    p[1] = 1
    del p[1]

    assert p._dict == {}

    p = PDict(DBFILE)
    assert p._dict == {}

    clean()

# Storing custom classes and saving mutations
def test_mutation():
    clean()
    p = PDict(DBFILE)

    t = Test()
    t.l = []
    t.i = 0

    p['test'] = t
    assert p['test'] == t

    t.l.append(1)
    t.i = 1

    p.save()

    p = PDict(DBFILE)
    t = p['test']
    assert t.l == [1]
    assert t.i == 1

    t.i = 2
    p.save('test')

    p = PDict(DBFILE)
    t = p['test']
    assert t.i == 2

    clean()