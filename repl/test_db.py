import unittest
from record import Record
from db import Database


class TestDatabase(unittest.TestCase):
    def test_empty(self):
        db = Database()
        self.assertEqual(db.records_num(), 0)

    def test_add_records(self):
        db = Database()
        db.add_record(Record(1))
        self.assertEqual(db.records_num(), 1)

    def test_add_same_record_twice(self):
        db = Database()
        db.add_record(Record(1))
        with self.assertRaises(ValueError):
            db.add_record(Record(1))

    def test_get_record_exists(self):
        db = Database()
        db.add_record(Record(1))
        self.assertIsNotNone(db.get_record(1))

    def test_get_record_not_exists(self):
        db = Database()
        db.add_record(Record(1))
        self.assertIsNone(db.get_record(2))

    def test_get_all(self):
        db = Database()
        db.add_record(Record(1))
        db.add_record(Record(2))
        db.add_record(Record(3))
        db.add_record(Record(4))
        self.assertEqual(len(db.get_all()), 4)
if __name__ == '__main__':
    unittest.main()
