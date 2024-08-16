import sqlite3
import jsonpickle

class PDict:
    def __init__(self, dbfile, dictname="default"):
        self.dbfile = dbfile
        self.dictname = dictname

        self.dict = {}
        self.con = sqlite3.connect(dbfile)
        self.con.execute("PRAGMA journal_mode=wal")
        self.con.execute("CREATE TABLE IF NOT EXISTS data(dict, key, value)")
        self.con.execute("CREATE UNIQUE INDEX IF NOT EXISTS dict_key ON data (dict, key)")

        results = self.con.execute("SELECT key, value FROM data WHERE dict=?", (dictname,)).fetchall()
        for key, value in results:
            self.dict[jsonpickle.loads(key)] = jsonpickle.loads(value)            

    def __getitem__(self, item):
        return self.dict[item]
    
    def __setitem__(self, item, value):
        self._write(item, value)
        self.dict[item] = value

    def __delitem__(self, item):
        self.con.execute("DELETE FROM data WHERE dict=? AND key=?", (self.dictname, jsonpickle.dumps(item)))
        self.con.commit()
        del self.dict[item]

    def __repr__(self):
        return self.dict.__repr__()
    
    def _write(self, key, value):
        self.con.execute("INSERT OR REPLACE INTO data VALUES(?, ?, ?)", (self.dictname, jsonpickle.dumps(key), jsonpickle.dumps(value)))
        self.con.commit()
    
    def update(self, input_dict):
        for key, value in input_dict.items():
            if key not in self.dict or self.dict[key] != value:
                self[key] = value

    def save(self, *args):
        """Updates the state stored on disk to match the in memory dict. This is only intended to be used to synchronize any mutations of stored objects. It's not intended that users modify the internal dict directly.

        If args are given, they are the keys to be saved. With no args, save all keys.
        """
        if len(args) > 0:
            for arg in args:
                self._write(arg, self.dict[arg])
        else:
            for key, value in self.dict.items():
                self._write(key, value)