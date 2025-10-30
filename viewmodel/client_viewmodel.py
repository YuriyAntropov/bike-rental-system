from model.rental import Rental
from datetime import datetime
class ClientViewModel:
    def __init__(self, db, user):
        self.db=db
        self.user=user
    def get_available_bicycles(self):
        return [
            {**bike, "station_id": bike["station_id"] or ""} 
            for bike in self.db.fetch_all("SELECT * FROM bicycles WHERE status='available'")]
    def start_rental(self, bicycle_id, start_time):
        bike=self.db.fetch_one("SELECT * FROM bicycles WHERE id=%s AND status='available'", (bicycle_id,))
        if not bike:
            raise Exception("Велосипед недоступний")
        Rental(None, bicycle_id, self.user.id, start_time).start_rental(self.db)
    def end_rental(self):
        rental_data=self.db.fetch_one(
            "SELECT * FROM rentals WHERE user_id=%s AND end_time IS NULL",
            (self.user.id,))
        if not rental_data:
            raise Exception("Оренда не знайдена або вже завершена")
        Rental(
            rental_data["id"], rental_data["bicycle_id"], rental_data["user_id"],
            rental_data["start_time"], rental_data["end_time"], rental_data["cost"]
        ).end_rental(self.db)
    def get_rentals(self, sort_option="Дата (спадання)"):
        rentals=[
            {**r, "end_time": r["end_time"] or "", "cost": r["cost"] or ""} 
            for r in self.db.get_user_rentals(self.user.id)]
        if sort_option=="Дата (спадання)":
            return sorted(rentals, key=lambda x: x["start_time"], reverse=True)
        elif sort_option=="Дата (зростання)":
            return sorted(rentals, key=lambda x: x["start_time"])
        elif sort_option=="Вартість":
            return sorted(rentals, key=lambda x: float(x["cost"] or 0))
        return rentals
    def logout(self):
        self.user=None