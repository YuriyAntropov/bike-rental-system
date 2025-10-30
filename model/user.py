import bcrypt
import re
class User:
    def __init__(self, id, role, username, password):
        self.id=id
        self.role=role
        self.username=username
        self.password=password  # Хеш
    @staticmethod
    def authenticate(db, username, password):
        """
        Аутентифікує користувача за логіном і паролем.
        Повертає об'єкт User, якщо аутентифікація успішна, інакше None.
        """
        try:
            query="SELECT id, role, username, password FROM users WHERE username=%s"
            user=db.fetch_one(query, (username,))
            if not user:
                print(f"Користувача з логіном {username} не знайдено")
                return None
            if not isinstance(user, dict):
                print(f"Некоректний формат даних для {username}: {user}")
                return None
            stored_hash=user.get('password', '').strip()
            print(f"Зчитаний хеш із бази для {username}: {stored_hash}")
            print(f"Довжина хеша: {len(stored_hash)}")
            if not re.match(r'^\$2[aby]\$\d{2}\$[./0-9A-Za-z]{53}$', stored_hash):
                print(f"Некоректний формат хеша для {username}: {stored_hash}")
                return None
            try:
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    print(f"Аутентифікація успішна для {username}")
                    return User(user['id'], user['role'], user['username'], user['password'])
                else:
                    print(f"Неправильний пароль для {username}")
                    return None
            except ValueError as ve:
                print(f"Помилка перевірки пароля для {username}: {str(ve)}")
                return None
        except Exception as e:
            print(f"Помилка аутентифікації для {username}: {str(e)}")
            return None
    @staticmethod
    def register(db, username, password, role="client"):
        """
        Реєструє нового користувача.
        Повертає (об'єкт User, None) у разі успіху, або (None, error_message) у разі помилки.
        """
        try:
            query="SELECT id FROM users WHERE username=%s"
            if db.fetch_one(query, (username,)):
                return None, f"Користувач із логіном {username} уже існує"
            if len(password)<6:
                return None, "Пароль повинен містити щонайменше 6 символів"
            if len(username)<3:
                return None, "Логін повинен містити щонайменше 3 символи"
            salt=bcrypt.gensalt()
            hashed=bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            query="INSERT INTO users (role, username, password) VALUES (%s, %s, %s)"
            user_id=db.execute_query(query, (role, username, hashed))
            print(f"Користувач {username} успішно зареєстрований")
            return User(user_id, role, username, hashed), None
        except Exception as e:
            print(f"Помилка реєстрації: {str(e)}")
            return None, f"Помилка реєстрації: {str(e)}"