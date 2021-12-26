"""Record in database."""


class Record:
    """Record in database."""
    def __init__(self, record_id):
        self.__id = record_id

    def get_id(self):
        """Return record ID."""
        return self.__id
