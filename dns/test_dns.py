import unittest
from lib import *
from dns import DnsDb, Record

class TestDnsDb(unittest.TestCase):
    def test_empty(self):
        db = DnsDb()
        self.assertEqual(DnsDb().num_records(), 0)

    def test_add_record(self):
        db = DnsDb()
        db.add_record(Record("narfu.ru", "1.2.3.4"))
        self.assertEqual(db.num_records(), 1)

    def test_get_addr_known(self):
        db = DnsDb()
        db.add_record(Record("narfu.ru", "1.2.3.4"))
        db.add_record(Record("urfu.ru", "2.3.4.5"))
        self.assertEqual(db.resolve("narfu.ru"), "1.2.3.4")
        self.assertEqual(db.resolve("urfu.ru"), "2.3.4.5")

    def test_get_addr_unknown(self):
        db = DnsDb()
        db.add_record(Record("narfu.ru", "2.3.4.5"))
        db.add_record(Record("29.ru", "3.4.5.6"))
        self.assertEqual(db.resolve("narfu.com"), None)

    def test_same_addresses_differ_names(self):
        db = DnsDb()
        db.add_record(Record("narfu.ru", "2.3.4.5"))

        raised = False
        try:
            db.add_record(Record("29.ru", "2.3.4.5"))
        except ValueError:
            raised = True
            
        self.assertTrue(raised)


class TestDns(unittest.TestCase):
    def test_no_local_dns_db(self):
        comp = Comp()
        ans = comp.resolve("narfu.ru")
        self.assertEqual(ans, None)

    def test_no_anwser_in_local_dv(self):
        comp = Comp()
        db = DnsDb()
        db.add_record(Record("narfu.ru", "1.2.3.4"))
        comp.set_dns_db(db)
        self.assertIsNone(comp.resolve("narfu.com"))

    def test_answer_in_local_db(self):
        comp = Comp()
        db = DnsDb()
        db.add_record(Record("narfu.ru", "1.2.3.4"))
        comp.set_dns_db(db)
        ans = comp.resolve("narfu.ru")
        self.assertEqual(ans, "1.2.3.4")

    def test_answer_from_dns_server(self):
        comp = Comp()
        local_db = DnsDb()
        local_db.add_record(Record("narfu.ru", "1.2.3.4"))
        comp.set_dns_db(local_db)
        comp.iface().set_dns_server("10.20.30.40")

        server = Comp()
        server_db = DnsDb()
        server_db.add_record(Record("ya.ru", "2.3.4.5"))
        server.set_dns_db(server_db)

        net = Network()
        net.add_host(comp, "11.12.13.14")
        net.add_host(server, "10.20.30.40")

        ans = comp.resolve("ya.ru")
        self.assertEqual(ans, "2.3.4.5")

    def test_wrong_addr_of_dns_server(self):
        comp = Comp()
        comp.set_dns_db(DnsDb())
        comp.iface().set_dns_server("10.20.30.45")

        net = Network()
        net.add_host(comp, "11.12.13.14")

        ans = comp.resolve("ya.ru")
        self.assertIsNone(ans, None)

    def test_resolve_unknown_name(self):
        comp = Comp()
        local_db = DnsDb()
        local_db.add_record(Record("narfu.ru", "1.2.3.4"))
        comp.set_dns_db(local_db)
        comp.iface().set_dns_server("10.20.30.40")

        server = Comp()
        server_db = DnsDb()
        server_db.add_record(Record("ya.ru", "2.3.4.5"))
        server.set_dns_db(server_db)

        net = Network()
        net.add_host(comp, "11.12.13.14")
        net.add_host(server, "10.20.30.40")

        ans = comp.resolve("ya.com")
        self.assertEqual(ans, None)

if __name__ == '__main__':
    unittest.main()
