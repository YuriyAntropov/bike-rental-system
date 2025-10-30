from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
class DemandPredictor:
    def __init__(self, db):
        self.db=db
    def get_station_demand_report(self):
        query="""
            SELECT s.id, s.address, COUNT(r.id) as rental_count, DAYNAME(r.start_time) as day
            FROM stations s
            LEFT JOIN bicycles b ON b.station_id=s.id
            LEFT JOIN rentals r ON r.bicycle_id=b.id
            WHERE r.start_time IS NOT NULL
            GROUP BY s.id, s.address, DAYNAME(r.start_time)
        """
        data=self.db.fetch_all(query)
        logger.info(f"Demand report data: {data}")
        if not data:
            return "Немає даних для прогнозу попиту"
        report="Прогноз попиту по станціях:\n"
        for entry in data:
            report+=f"Станція {entry['id']} ({entry['address']}): {entry['rental_count']} оренд у {entry['day']}\n"
        return report