from model.bicycle import Bicycle
from model.station import Station
from model.demand_predictor import DemandPredictor
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
class ManagerViewModel:
    def __init__(self, db):
        self.db=db
    def add_bicycle(self, model, status, station_id):
        if station_id and not self.db.fetch_one("SELECT 1 FROM stations WHERE id=%s", (station_id,)):
            logger.error(f"Station {station_id} does not exist")
            raise Exception("Станція не існує")
        Bicycle(None, model, status, station_id).save(self.db)
        logger.info(f"Added bicycle: {model}, status: {status}, station_id: {station_id}")
    def update_bicycle(self, bicycle_id, model, status, station_id):
        if station_id and not self.db.fetch_one("SELECT 1 FROM stations WHERE id=%s", (station_id,)):
            logger.error(f"Station {station_id} does not exist")
            raise Exception("Станція не існує")
        Bicycle(bicycle_id, model, status, station_id).save(self.db)
        logger.info(f"Updated bicycle ID {bicycle_id}: {model}, status: {status}, station_id: {station_id}")
    def delete_bicycle(self, bicycle_id):
        Bicycle(bicycle_id, None, None, None).delete(self.db)
        logger.info(f"Deleted bicycle ID {bicycle_id}")
    def get_bicycles(self):
        bicycles=self.db.fetch_all("SELECT * FROM bicycles")
        result=[{**b, "station_id": str(b["station_id"] or "")} for b in bicycles]
        logger.info(f"Fetched {len(result)} bicycles")
        return result
    def export_xml(self):
        self.db.export_bicycles()
        logger.info("Exported bicycles to XML")
    def import_xml(self):
        self.db.import_bicycles()
        logger.info("Imported bicycles from XML")
    def add_station(self, address):
        Station(None, address).save(self.db)
        logger.info(f"Added station: {address}")
    def update_station(self, station_id, address):
        Station(station_id, address).save(self.db)
        logger.info(f"Updated station ID {station_id}: {address}")
    def delete_station(self, station_id):
        if self.db.fetch_one("SELECT 1 FROM bicycles WHERE station_id=%s", (station_id,)):
            logger.error(f"Cannot delete station {station_id}: bicycles are present")
            raise Exception("Cannot delete station with bicycles")
        Station(station_id, None).delete(self.db)
        logger.info(f"Deleted station ID {station_id}")
    def get_stations(self):
        stations=self.db.fetch_all("SELECT * FROM stations")
        logger.info(f"Fetched {len(stations)} stations")
        return stations
    def get_income_report(self, start_date, end_date):
        result=self.db.get_income_report(start_date, end_date)
        logger.info(f"Income report: {result}")
        return result
    def get_formatted_income_report(self, start_date, end_date):
        report_data=self.get_income_report(start_date, end_date)
        formatted="Звіт про доходи:\n" + "\n".join(
            f"{entry['date']}: {entry['total_income']:.2f} грн"
            for entry in report_data
        )
        logger.info(f"Formatted income report: {formatted}")
        return formatted
    def get_demand_report(self):
        report=DemandPredictor(self.db).get_station_demand_report()
        logger.info(f"Demand report: {report}")
        return f"Прогноз попиту:\n{report}"
    def get_repair_notifications(self):
        notifications=self.db.get_repair_notifications()
        result=[{**b, "station_id": str(b["station_id"] or "")} for b in notifications]
        logger.info(f"Fetched {len(result)} repair notifications")
        return result
    def logout(self):
        logger.info("Manager logged out")
        pass