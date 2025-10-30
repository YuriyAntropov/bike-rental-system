import bcrypt
from model.database import Database
from model.user import User
def test_authentication(username, password, expected_hash):
    print(f"\nТестування для {username} з паролем {password}")
    print(f"Очікуваний хеш: {expected_hash}")
    try:
        if bcrypt.checkpw(password.encode('utf-8'), expected_hash.encode('utf-8')):
            print("Пряма перевірка хеша: УСПІХ")
        else:
            print("Пряма перевірка хеша: НЕВДАЧА")
    except Exception as e:
        print(f"Помилка прямої перевірки: {str(e)}")
    try:
        db=Database()
        user=User.authenticate(db, username, password)
        if user:
            print(f"Аутентифікація через базу: УСПІХ (ID: {user.id}, Роль: {user.role})")
        else:
            print("Аутентифікація через базу: НЕВДАЧА")
    except Exception as e:
        print(f"Помилка перевірки через базу: {str(e)}")
if __name__=="__main__":
    test_authentication(
        "manager1",
        "manager123",
        "$2b$12$hUsNDQNJoTCReXx2Yo40M.G0kd2.XV9hwiaSh.c5CAT5QJy77IomK")
    test_authentication(
        "client1",
        "client123",
        "$2b$12$ul7NFSz.UE4qCmrfW30ciOm18uqzTsYkn.9KpeI2NJYC25efO.V2q")