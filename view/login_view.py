import tkinter as tk
from view.base_view import BaseView
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
class LoginView(BaseView):
    def __init__(self, root, view_model):
        super().__init__(root)
        self.root.title("Вхід у систему")
        self.root.geometry("500x500")
        self.view_model=view_model
        tk.Label(self.container, text="Логін:").pack(pady=10)
        self.username=tk.Entry(self.container)
        self.username.pack()
        tk.Label(self.container, text="Пароль:").pack(pady=10)
        self.password=tk.Entry(self.container, show="*")
        self.password.pack()
        tk.Button(self.container, text="Увійти", command=self.submit).pack(pady=10)
        tk.Button(self.container, text="Зареєструватися", command=self.show_register).pack(pady=5)
        tk.Button(self.container, text="Вихід", command=self.root.quit).pack(pady=5)
    def submit(self):
        username=self.username.get()
        password=self.password.get()
        logger.info(f"Attempting login for user: {username}")
        # Перевіряємо логін
        login_success=self.handle_action(
            lambda: self.view_model.login(username, password),
            None,
            "Неправильний логін або пароль"
        )
        # Якщо логін успішний, викликаємо навігацію
        if login_success:
            logger.info("Login successful, navigating to user panel")
            try:
                self.view_model.navigate()
            except Exception as e:
                logger.error(f"Navigation error: {str(e)}")
                self.handle_action(
                    lambda: None,
                    None,
                    f"Помилка переходу до панелі: {str(e)}"
                )
    def show_register(self):
        top=tk.Toplevel(self.root)
        top.title("Реєстрація")
        top.geometry("300x250")
        container=tk.Frame(top)
        container.pack(pady=20)
        tk.Label(container, text="Логін:").pack(pady=10)
        username=tk.Entry(container)
        username.pack()
        tk.Label(container, text="Пароль:").pack(pady=10)
        password=tk.Entry(container, show="*")
        password.pack()
        tk.Label(container, text="Повторіть пароль:").pack(pady=10)
        confirm_password=tk.Entry(container, show="*")
        confirm_password.pack()
        def submit_register():
            if not (username.get() and password.get()):
                return self.handle_action(lambda: None, None, "Заповніть усі поля")
            if password.get() != confirm_password.get():
                return self.handle_action(lambda: None, None, "Паролі не збігаються")
            user, error=self.view_model.register(username.get(), password.get())
            self.handle_action(
                lambda: user or (_ for _ in ()).throw(Exception(error)),
                "Реєстрація успішна" if user else None,
                error or "Помилка реєстрації"
            ) and top.destroy()
        tk.Button(container, text="Зареєструвати", command=submit_register).pack(pady=10)
        tk.Button(container, text="Закрити", command=top.destroy).pack(pady=5)