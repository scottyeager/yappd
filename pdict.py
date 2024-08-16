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
        self.con.execute("INSERT OR REPLACE INTO data VALUES(?, ?, ?)", (self.dictname, jsonpickle.dumps(item), jsonpickle.dumps(value)))
        self.con.commit()
        self.dict[item] = value

    def __delitem__(self, item):
        self.con.execute("DELETE FROM data WHERE dict=? AND key=?", (self.dictname, jsonpickle.dumps(item)))
        self.con.commit()
        del self.dict[item]

    def __repr__(self):
        return self.dict.__repr__()
    
    def update(self, input_dict):
        for key, value in input_dict.items():
            if key not in self.dict or self.dict[key] != value:
                self[key] = value