import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from view.base_view import BaseView
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
class ManagerView(BaseView):
    def __init__(self, root, view_model):
        super().__init__(root)
        self.root.title("Панель менеджера")
        self.root.geometry("800x600")
        self.view_model=view_model
        self.notebook=ttk.Notebook(self.container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        bike_frame=tk.Frame(self.notebook)
        self.notebook.add(bike_frame, text="Велосипеди")
        bike_container=tk.Frame(bike_frame)
        bike_container.pack(fill=tk.BOTH, expand=True)
        self.bike_tree=self.create_treeview(bike_container, ("ID", "Model", "Status", "Station"), ("ID", "Модель", "Статус", "Станція"), tree_id="bike_tree")
        bike_form=tk.Frame(bike_frame)
        bike_form.pack(pady=10)
        tk.Label(bike_form, text="Модель:").grid(row=0, column=0, padx=5)
        self.bike_model=tk.Entry(bike_form)
        self.bike_model.grid(row=0, column=1)
        tk.Label(bike_form, text="Статус:").grid(row=1, column=0, padx=5)
        self.bike_status=ttk.Combobox(bike_form, values=["available", "in_repair", "removed"])
        self.bike_status.grid(row=1, column=1)
        tk.Label(bike_form, text="Станція:").grid(row=2, column=0, padx=5)
        self.bike_station=tk.Entry(bike_form)
        self.bike_station.grid(row=2, column=1)
        tk.Button(bike_form, text="Додати", command=self.handle_add_bike).grid(row=3, column=0, pady=10)
        tk.Button(bike_form, text="Оновити", command=self.handle_update_bike).grid(row=3, column=1)
        tk.Button(bike_form, text="Видалити", command=self.handle_delete_bike).grid(row=3, column=2)
        tk.Button(bike_form, text="Експорт XML", command=self.handle_export).grid(row=4, column=0)
        tk.Button(bike_form, text="Імпорт XML", command=self.handle_import).grid(row=4, column=1)
        station_frame=tk.Frame(self.notebook)
        self.notebook.add(station_frame, text="Велостанції")
        station_container=tk.Frame(station_frame)
        station_container.pack(fill=tk.BOTH, expand=True)
        self.station_tree=self.create_treeview(station_container, ("ID", "Address"), ("ID", "Адреса"), tree_id="station_tree")
        station_form=tk.Frame(station_frame)
        station_form.pack(pady=10)
        tk.Label(station_form, text="Адреса:").grid(row=0, column=0, padx=5)
        self.station_address=tk.Entry(station_form)
        self.station_address.grid(row=0, column=1)
        tk.Button(station_form, text="Додати", command=self.handle_add_station).grid(row=1, column=0, pady=10)
        tk.Button(station_form, text="Оновити", command=self.handle_update_station).grid(row=1, column=1)
        tk.Button(station_form, text="Видалити", command=self.handle_delete_station).grid(row=1, column=2)
        report_frame=tk.Frame(self.notebook)
        self.notebook.add(report_frame, text="Звіти")
        report_form=tk.Frame(report_frame)
        report_form.pack(pady=10)
        tk.Label(report_form, text="Початкова дата (РРРР-ММ-ДД):").grid(row=0, column=0, padx=5)
        self.start_date=tk.Entry(report_form)
        self.start_date.grid(row=0, column=1)
        self.start_date.insert(0, "2025-05-01")
        tk.Label(report_form, text="Кінцева дата (РРРР-ММ-ДД):").grid(row=1, column=0, padx=5)
        self.end_date=tk.Entry(report_form)
        self.end_date.grid(row=1, column=1)
        self.end_date.insert(0, "2025-05-23")
        tk.Button(report_form, text="Звіт про доходи", command=self.handle_income_report).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(report_form, text="Прогноз попиту", command=self.handle_demand_report).grid(row=3, column=0, columnspan=2, pady=5)
        self.report_text=tk.Text(report_frame, height=20, width=80)
        self.report_text.pack(pady=10)
        notification_frame=tk.Frame(self.notebook)
        self.notebook.add(notification_frame, text="Сповіщення")
        notification_container=tk.Frame(notification_frame)
        notification_container.pack(fill=tk.BOTH, expand=True)
        self.notification_tree=self.create_treeview(notification_container, ("ID", "Model", "Station"), ("ID", "Модель", "Станція"), tree_id="notification_tree")
        tk.Button(notification_frame, text="Оновити сповіщення", command=self.update_notifications).pack(pady=10)
        tk.Button(self.container, text="Вихід", command=lambda: self.view_model.logout()).pack(pady=10)
        self.update_bicycles()
        self.update_stations()
        self.update_notifications()
        self.root.update()
        self.notebook.update()
    def update_bicycles(self):
        logger.info("Updating bicycles table")
        self.update_treeview(self.bike_tree, self.view_model.get_bicycles(), ["id", "model", "status", "station_id"])
        self.root.update()
    def update_stations(self):
        logger.info("Updating stations table")
        self.update_treeview(self.station_tree, self.view_model.get_stations(), ["id", "address"])
        self.root.update()
    def update_notifications(self):
        logger.info("Updating notifications table")
        self.update_treeview(self.notification_tree, self.view_model.get_repair_notifications(), ["id", "model", "station_id"])
        self.root.update()
    def handle_add_bike(self):
        model, status, station_id=self.bike_model.get(), self.bike_status.get(), self.bike_station.get() or None
        if not (model and status):
            return self.handle_action(lambda: None, None, "Заповніть модель і статус")
        self.handle_action(
            lambda: self.view_model.add_bicycle(model, status, int(station_id) if station_id else None),
            None
        ) and self.update_bicycles()
    def handle_update_bike(self):
        selected=self.bike_tree.selection()
        if not selected:
            return self.handle_action(lambda: None, None, "Виберіть велосипед")
        bike_id=self.bike_tree.item(selected)["values"][0]
        model, status, station_id=self.bike_model.get(), self.bike_status.get(), self.bike_station.get() or None
        if not (model and status):
            return self.handle_action(lambda: None, None, "Заповніть модель і статус")
        self.handle_action(
            lambda: self.view_model.update_bicycle(bike_id, model, status, int(station_id) if station_id else None),
            None
        ) and self.update_bicycles()
    def handle_delete_bike(self):
        selected=self.bike_tree.selection()
        if not selected:
            return self.handle_action(lambda: None, None, "Виберіть велосипед")
        bike_id=self.bike_tree.item(selected)["values"][0]
        self.handle_action(
            lambda: self.view_model.delete_bicycle(bike_id),
            None
        ) and self.update_bicycles()
    def handle_export(self):
        self.handle_action(
            self.view_model.export_xml,
            "Дані експортовано в bicycles.xml"
        )
    def handle_import(self):
        self.handle_action(
            self.view_model.import_xml,
            None
        ) and self.update_bicycles()
    def handle_add_station(self):
        address=self.station_address.get()
        if not address:
            return self.handle_action(lambda: None, None, "Введіть адресу")
        self.handle_action(
            lambda: self.view_model.add_station(address),
            None
        ) and self.update_stations()
    def handle_update_station(self):
        selected=self.station_tree.selection()
        if not selected:
            return self.handle_action(lambda: None, None, "Виберіть станцію")
        station_id=self.station_tree.item(selected)["values"][0]
        address=self.station_address.get()
        if not address:
            return self.handle_action(lambda: None, None, "Введіть адресу")
        self.handle_action(
            lambda: self.view_model.update_station(station_id, address),
            None
        ) and self.update_stations()
    def handle_delete_station(self):
        selected=self.station_tree.selection()
        if not selected:
            return self.handle_action(lambda: None, None, "Виберіть станцію")
        station_id=self.station_tree.item(selected)["values"][0]
        self.handle_action(
            lambda: self.view_model.delete_station(station_id),
            None
        ) and self.update_stations()
    def handle_income_report(self):
        try:
            start_date=datetime.strptime(self.start_date.get(), "%Y-%m-%d")
            end_date=datetime.strptime(self.end_date.get(), "%Y-%m-%d")
            if start_date > end_date:
                self.handle_action(lambda: None, None, "Початкова дата не може бути пізніше кінцевої")
                return
            logger.info(f"Generating income report for {start_date} to {end_date}")
            report_data=self.view_model.get_income_report(start_date, end_date)
            logger.info(f"Raw report data: {report_data}")
            report=self.view_model.get_formatted_income_report(start_date, end_date)
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, report)
        except Exception as e:
            logger.error(f"Income report error: {str(e)}")
            self.handle_action(lambda: None, None, str(e))
    def handle_demand_report(self):
        try:
            report=self.view_model.get_demand_report()
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, report)
        except Exception as e:
            logger.error(f"Demand report error: {str(e)}")
            self.handle_action(lambda: None, None, f"Помилка прогнозу попиту: {str(e)}")