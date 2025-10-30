class Bicycle:
    def __init__(self, id, model, status, station_id):
        self.id=id
        self.model=model
        self.status=status
        self.station_id=station_id
    def save(self, db):
        if self.id is None:
            query="INSERT INTO bicycles (model, status, station_id) VALUES (%s, %s, %s)"
            self.id=db.execute_query(query, (self.model, self.status, self.station_id))
        else:
            query="UPDATE bicycles SET model=%s, status=%s, station_id=%s WHERE id=%s"
            db.execute_query(query, (self.model, self.status, self.station_id, self.id))
    def delete(self, db):
        query="DELETE FROM bicycles WHERE id=%s"
        db.execute_query(query, (self.id,))