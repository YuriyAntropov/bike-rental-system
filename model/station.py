class Station:
    def __init__(self, id, address):
        self.id=id
        self.address=address
    def save(self, db):
        if self.id is None:
            query="INSERT INTO stations (address) VALUES (%s)"
            self.id=db.execute_query(query, (self.address,))
        else:
            query="UPDATE stations SET address=%s WHERE id=%s"
            db.execute_query(query, (self.address, self.id))
    def delete(self, db):
        query="DELETE FROM stations WHERE id=%s"
        db.execute_query(query, (self.id,))