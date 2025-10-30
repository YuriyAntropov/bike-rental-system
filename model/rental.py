from datetime import datetime
from decimal import Decimal
class Rental:
    def __init__(self, id, bicycle_id, user_id, start_time, end_time=None, cost=None):
        self.id=id
        self.bicycle_id=bicycle_id
        self.user_id=user_id
        self.start_time=start_time
        self.end_time=end_time
        self.cost=cost
    def start_rental(self, db):
        query="""
            INSERT INTO rentals (bicycle_id, user_id, start_time)
            VALUES (%s, %s, %s)
        """
        self.id=db.execute_query(query, (self.bicycle_id, self.user_id, self.start_time))
        db.execute_query("UPDATE bicycles SET status='removed' WHERE id=%s", (self.bicycle_id,))
    def end_rental(self, db):
        self.end_time=datetime.now()
        duration=(self.end_time - self.start_time).total_seconds()/60.0
        # вартість: 1 грн\хв, мін вартість 1 грн
        self.cost=Decimal(max(1.0, duration)).quantize(Decimal('0.01'))
        query="""
            UPDATE rentals
            SET end_time=%s, cost=%s
            WHERE id=%s
        """
        db.execute_query(query, (self.end_time, self.cost, self.id))
        db.execute_query("UPDATE bicycles SET status='available' WHERE id=%s", (self.bicycle_id,))