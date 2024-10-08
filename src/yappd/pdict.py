import sqlite3
import jsonpickle

class PDict:
    def __init__(self, dbfile, name="default"):
        self.dbfile = dbfile
        self.name = name

        self._dict = {}
        self.con = sqlite3.connect(dbfile)
        self.con.execute("PRAGMA journal_mode=wal")
        self.con.execute("CREATE TABLE IF NOT EXISTS data(dict, key, value)")
        self.con.execute("CREATE UNIQUE INDEX IF NOT EXISTS dict_key ON data (dict, key)")

        results = self.con.execute("SELECT key, value FROM data WHERE dict=?", (name,)).fetchall()
        for key, value in results:
            self._dict[self._decode(key)] = jsonpickle.loads(value)            

    def __delitem__(self, key):
        self.con.execute("DELETE FROM data WHERE dict=? AND key=?", (self.name, self._encode(key)))
        self.con.commit()
        del self._dict[key]

    def __iter__(self):
        return self._dict.__iter__()
    
    def __len__(self):
        return len(self._dict)

    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, value):
        self._write(key, value)
        self._dict[key] = value

    def __repr__(self):
        return self._dict.__repr__()
    
    def _encode(self, value):
        return jsonpickle.encode(value, keys=True)
    
    def _decode(self, value):
        return jsonpickle.decode(value, keys=True)
    
    def _write(self, key, value):
        self.con.execute("INSERT OR REPLACE INTO data VALUES(?, ?, ?)", (self.name, self._encode(key), self._encode(value)))
        self.con.commit()

    def items(self):
        return self._dict.items()
    
    def keys(self):
        return self._dict.keys()

    def save(self, *args):
        """Updates the state stored on disk to match the in memory dict. This is only intended to be used to synchronize any mutations of stored objects. It's not intended that users modify the internal dict directly.

        If args are given, they are the keys to be saved. With no args, save all keys.
        """
        if len(args) > 0:
            for arg in args:
                self._write(arg, self._dict[arg])
        else:
            for key, value in self._dict.items():
                self._write(key, value)

    def update(self, input_dict):
        # We set all values, even if the same value is already stored at the same key, in order to also support preserving mutated objects this way
        for key, value in input_dict.items():
            self[key] = value

    def values(self):
        return self._dict.values()