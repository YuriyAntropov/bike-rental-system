import tkinter as tk
from model.database import Database
from view.login_view import LoginView
from view.manager_view import ManagerView
from view.client_view import ClientView
from viewmodel.login_viewmodel import LoginViewModel
from viewmodel.manager_viewmodel import ManagerViewModel
from viewmodel.client_viewmodel import ClientViewModel
class App:
    def __init__(self, root):
        self.root=root
        self.root.title("Система прокату велосипедів")
        self.root.geometry("500x500")
        self.db=Database()
        self.show_login()
    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginView(self.root, LoginViewModel(self.db, self.navigate))
    def navigate(self, view_class, db, user):
        for widget in self.root.winfo_children():
            widget.destroy()
        if user.role=="manager":
            view_model=ManagerViewModel(db)
            view_class(self.root, view_model)
        else:
            view_model=ClientViewModel(db, user)
            view_class(self.root, view_model)
if __name__=="__main__":
    root=tk.Tk()
    app=App(root)
    root.mainloop()