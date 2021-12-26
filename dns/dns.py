"""DNS prototype."""

class Record:
    """Single DNS record."""

    def __init__(self, name, addr):
        self.__name = name
        self.__addr = addr

    def get_name(self):
        return self.__name

    def get_addr(self):
        return self.__addr

class DnsDb:
    """DNS database."""

    def __init__(self):
        self.__records = {}
        self.__addrs = {}

    def num_records(self):
        """Return number of records."""
        return len(self.__records)

    def add_record(self, record):
        """Add record."""
        self.__check_record(record)
        self.__records[record.get_name()] = record

    def resolve(self, name):
        """Return IP address by name."""
        try:
            return self.__records[name].get_addr()
        except KeyError:
            return None

    def __check_record(self, record):
        if record.get_addr() in self.__addrs:
            raise ValueError("Duplicated address")
        self.__addrs[record.get_addr()] = True
