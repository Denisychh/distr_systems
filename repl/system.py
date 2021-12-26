"""System with replication."""
from db import Database
from record import Record

class System:
    """System with replication."""
    def __init__(self, repls_num=1):
        if repls_num < 1:
            raise ValueError("repls_num must be positive")

        self.__main = Database()
        self.__repls = []
        for _ in range(repls_num):
            self.__repls.append(Database())

        self.__stats = {
            'main': 0,
            'repl': [],
        }
        for _ in range(repls_num):
            self.__stats['repl'].append(0)

        self.__ind = 0

    def get_main(self):
        """Return main DB."""
        return self.__main

    def get_repl(self, ind=0):
        """Return replicated DB."""
        return self.__repls[ind]

    def sync(self):
        """Synchronize system."""
        for repl in self.__repls:
            _sync(self.__main, repl)

    def add_record(self, rec):
        """Add record to database."""
        return self.__main.add_record(rec)

    def get_record(self, record_id):
        """Get record by ID."""
        rec = self.__repls[self.__ind].get_record(record_id)
        self.__stats['repl'][self.__ind] += 1
        self.__update_ind()
        if rec:
            return rec
        return self.__main.get_record(record_id)

    def get_all(self):
        """Return all records."""
        res = self.__repls[self.__ind].get_all()
        self.__stats['repl'][self.__ind] += 1
        self.__update_ind()
        return res

    def stats(self):
        """Return statistics of readings."""
        return self.__stats

    def __update_ind(self):
        self.__ind = (self.__ind + 1) % len(self.__repls)


def _sync(src, dst):
    records = src.get_all()
    for rec_id, rec in records.items():
        if not dst.get_record(rec_id):
            dst.add_record(rec)
if __name__ == '__main__':
    system = System(4)
    system.add_record(Record(1))
    system.add_record(Record(2))
    system.add_record(Record(3))
    system.sync()
    system.get_record(1)
    system.get_record(1)
    system.get_record(1)
    system.get_record(1)
    stats = system.stats()
    print (stats['main'], stats['repl'])
    
