import unittest
import os
import sys
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.database import Database
from model.user import User
from model.rental import Rental
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db=Database()
        self.db.execute_query("DELETE FROM rentals; DELETE FROM bicycles; DELETE FROM stations; DELETE FROM users")
        self.station_id=self.db.execute_query("INSERT INTO stations (address) VALUES (%s)", ("Test Station",))
        self.bike_id=self.db.execute_query("INSERT INTO bicycles (model, status, station_id) VALUES (%s, %s, %s)", 
                                            ("Trek 820", "available", self.station_id))
        self.user_id=User.register(self.db, "testuser", "test123")[0].id
    def test_add_bicycle(self):
        bike_id=self.db.execute_query("INSERT INTO bicycles (model, status, station_id) VALUES (%s, %s, %s)", 
                                      ("Giant Escape", "available", self.station_id))
        bike=self.db.fetch_one("SELECT * FROM bicycles WHERE id=%s", (bike_id,))
        self.assertEqual(bike, {"id": bike_id, "model": "Giant Escape", "status": "available", "station_id": self.station_id})
    def test_update_bicycle(self):
        bike_id=self.db.execute_query("INSERT INTO bicycles (model, status, station_id) VALUES (%s, %s, %s)", 
                                      ("Giant Escape", "available", self.station_id))
        self.db.execute_query("UPDATE bicycles SET model=%s, status=%s, station_id=%s WHERE id=%s", 
                            ("Giant Escape 2", "in_repair", self.station_id, bike_id))
        bike=self.db.fetch_one("SELECT * FROM bicycles WHERE id=%s", (bike_id,))
        self.assertEqual(bike, {"id": bike_id, "model": "Giant Escape 2", "status": "in_repair", "station_id": self.station_id})
    def test_delete_bicycle(self):
        bike_id=self.db.execute_query("INSERT INTO bicycles (model, status, station_id) VALUES (%s, %s, %s)", 
                                      ("Trek 820", "available", self.station_id))
        self.db.execute_query("DELETE FROM bicycles WHERE id=%s", (bike_id,))
        self.assertIsNone(self.db.fetch_one("SELECT * FROM bicycles WHERE id=%s", (bike_id,)))
    def test_export_import_xml(self):
        self.db.execute_query("INSERT INTO bicycles (model, status, station_id) VALUES (%s, %s, %s)", 
                            ("Trek 820", "available", self.station_id))
        self.db.export_bicycles_to_xml("test.xml")
        self.db.execute_query("DELETE FROM bicycles")
        self.db.import_bicycles_from_xml("test.xml")
        bikes=self.db.fetch_all("SELECT * FROM bicycles")
        self.assertGreater(len(bikes), 0)
        self.assertEqual(bikes[0]["model"], "Trek 820")
    def test_register_user(self):
        user, error=User.register(self.db, "newuser", "newpass123")
        self.assertIsNotNone(user)
        self.assertIsNone(error)
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.role, "client")
        self.assertIsNotNone(User.authenticate(self.db, "newuser", "newpass123"))
    def test_start_end_rental(self):
        start_time=datetime.now()
        rental=Rental(None, self.bike_id, self.user_id, start_time)
        rental.start_rental(self.db)
        self.assertEqual(self.db.fetch_one("SELECT status FROM bicycles WHERE id=%s", (self.bike_id,))["status"], "removed")
        rental.end_time=start_time + timedelta(minutes=2)
        rental.end_rental(self.db)
        self.assertEqual(self.db.fetch_one("SELECT status FROM bicycles WHERE id=%s", (self.bike_id,))["status"], "available")
        rental_data=self.db.fetch_one("SELECT * FROM rentals WHERE id=%s", (rental.id,))
        self.assertIsNotNone(rental_data["end_time"])
        self.assertGreater(rental_data["cost"], 0)
    def test_income_report(self):
        start_time=datetime.now() - timedelta(days=1)
        rental=Rental(None, self.bike_id, self.user_id, start_time)
        rental.start_rental(self.db)
        rental.end_time=start_time + timedelta(minutes=2)
        rental.end_rental(self.db)
        report=self.db.get_income_report(start_time - timedelta(days=1), start_time + timedelta(days=1))
        self.assertGreater(len(report), 0)
        self.assertGreater(report[0]["total_income"], 0)
if __name__=="__main__":
    unittest.main()