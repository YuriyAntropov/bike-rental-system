from datetime import datetime
class ConsoleView:
    def __init__(self, login_viewmodel, manager_viewmodel, client_viewmodel):
        self.login_viewmodel=login_viewmodel
        self.manager_viewmodel=manager_viewmodel
        self.client_viewmodel=client_viewmodel
        self.user=None
    def run(self):
        while True:
            if not self.user:
                self.show_login()
            elif self.user.role=="manager":
                self.show_manager_menu()
            else:
                self.show_client_menu()
    def show_login(self):
        print("\n=== Вхід у систему ===")
        username=input("Логін: ")
        password=input("Пароль: ")
        self.user=self.login_viewmodel.login(username, password)
        print("Неправильний логін або пароль" if not self.user else f"Вітаємо, {self.user.username} ({self.user.role})!")
    def show_manager_menu(self):
        while True:
            print("\n=== Меню менеджера ===\n1. Велосипеди\n2. Додати велосипед\n3. Оновити велосипед\n4. Видалити велосипед\n5. Велостанції\n6. Додати велостанцію\n7. Оновити велостанцію\n8. Видалити велостанцію\n9. Вийти")
            choice=input("Виберіть опцію (1-9): ")
            try:
                if choice=="1":
                    for bike in self.manager_viewmodel.get_bicycles():
                        print(f"ID: {bike['id']}, Модель: {bike['model']}, Статус: {bike['status']}, Станція: {bike['station_id'] or 'Немає'}")
                elif choice=="2":
                    model=input("Модель: ")
                    status=input("Статус (available/in_repair/removed): ")
                    station_id=input("ID станції (Enter для None): ") or None
                    self.manager_viewmodel.add_bicycle(model, status, int(station_id) if station_id else None)
                    print("Велосипед додано")
                elif choice=="3":
                    bike_id=input("ID велосипеда: ")
                    model=input("Нова модель: ")
                    status=input("Новий статус: ")
                    station_id=input("Новий ID станції (Enter для None): ") or None
                    self.manager_viewmodel.update_bicycle(int(bike_id), model, status, int(station_id) if station_id else None)
                    print("Велосипед оновлено")
                elif choice=="4":
                    self.manager_viewmodel.delete_bicycle(int(input("ID велосипеда: ")))
                    print("Велосипед видалено")
                elif choice=="5":
                    for station in self.manager_viewmodel.get_stations():
                        print(f"ID: {station['id']}, Адреса: {station['address']}")
                elif choice=="6":
                    self.manager_viewmodel.add_station(input("Адреса: "))
                    print("Велостанцію додано")
                elif choice=="7":
                    self.manager_viewmodel.update_station(int(input("ID велостанції: ")), input("Нова адреса: "))
                    print("Велостанцію оновлено")
                elif choice=="8":
                    self.manager_viewmodel.delete_station(int(input("ID велостанції: ")))
                    print("Велостанцію видалено")
                elif choice=="9":
                    self.user=None
                    break
                else:
                    print("Невірний вибір")
            except Exception as e:
                print(f"Помилка: {e}")
    def show_client_menu(self):
        while True:
            print("\n=== Меню клієнта ===\n1. Доступні велосипеди\n2. Орендувати\n3. Завершити оренду\n4. Історія оренд\n5. Вийти")
            choice=input("Виберіть опцію (1-5): ")
            try:
                if choice=="1":
                    for bike in self.client_viewmodel.get_available_bicycles():
                        print(f"ID: {bike['id']}, Модель: {bike['model']}, Станція: {bike['station_id'] or 'Немає'}")
                elif choice=="2":
                    self.client_viewmodel.start_rental(int(input("ID велосипеда: ")), datetime.now())
                    print("Велосипед орендовано")
                elif choice=="3":
                    self.client_viewmodel.end_rental()
                    print("Оренду завершено")
                elif choice=="4":
                    for rental in self.client_viewmodel.get_rentals():
                        print(f"ID: {rental['id']}, Велосипед: {rental['model']}, Початок: {rental['start_time']}, Кінець: {rental['end_time'] or 'Активна'}, Вартість: {rental['cost'] or 'Не розраховано'}")
                elif choice=="5":
                    self.user=None
                    break
                else:
                    print("Невірний вибір")
            except Exception as e:
                print(f"Помилка: {e}")