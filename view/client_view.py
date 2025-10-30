import tkinter as tk
from tkinter import ttk
from datetime import datetime
from view.base_view import BaseView
class ClientView(BaseView):
    def __init__(self, root, view_model):
        super().__init__(root)
        self.root.title("Панель клієнта")
        self.root.geometry("600x400")
        self.view_model=view_model
        self.tree=self.create_treeview(("ID", "Model", "Station"), ("ID", "Модель", "Станція"))
        button_frame=tk.Frame(self.container)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Орендувати", command=self.handle_rental).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Завершити оренду", command=self.handle_end_rental).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Історія оренд", command=self.show_rentals).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Вихід", command=lambda: self.view_model.logout()).pack(side=tk.LEFT, padx=5)
        self.update_bicycles()
    def update_bicycles(self):
        self.update_treeview(self.tree, self.view_model.get_available_bicycles(), ["id", "model", "station_id"])
    def handle_rental(self):
        selected=self.tree.selection()
        if not selected:
            return self.handle_action(lambda: None, None, "Виберіть велосипед")
        bike_id=self.tree.item(selected)["values"][0]
        self.handle_action(
            lambda: self.view_model.start_rental(bike_id, datetime.now()),
            "Велосипед орендовано",
            "Не вдалося орендувати велосипед"
        ) and self.update_bicycles()
    def handle_end_rental(self):
        self.handle_action(
            self.view_model.end_rental,
            "Оренду завершено",
            "Не вдалося завершити оренду"
        ) and self.update_bicycles()
    def show_rentals(self):
        top=tk.Toplevel(self.root)
        top.title("Історія оренд")
        top.geometry("600x300")
        container=tk.Frame(top)
        container.pack(fill=tk.BOTH, expand=True, pady=10)
        sort_frame=tk.Frame(container)
        sort_frame.pack(pady=5)
        tk.Label(sort_frame, text="Сортувати за:").pack(side=tk.LEFT, padx=5)
        self.sort_combobox=ttk.Combobox(sort_frame, values=["Дата (спадання)", "Дата (зростання)", "Вартість"])
        self.sort_combobox.pack(side=tk.LEFT, padx=5)
        tk.Button(sort_frame, text="Сортувати", command=lambda: self.update_rentals()).pack(side=tk.LEFT, padx=5)
        self.rental_tree=self.create_treeview(("ID", "Model", "Start", "End", "Cost"), ("ID", "Модель", "Початок", "Кінець", "Вартість"))
        tk.Button(container, text="Закрити", command=top.destroy).pack(pady=10)
        self.update_rentals()
    def update_rentals(self):
        self.update_treeview(self.rental_tree, self.view_model.get_rentals(self.sort_combobox.get()), 
                            ["id", "model", "start_time", "end_time", "cost"])