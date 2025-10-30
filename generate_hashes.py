import bcrypt
def generate_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
passwords=["manager123", "client123"]
for pwd in passwords:
    hashed=generate_hash(pwd)
    print(f"Пароль: {pwd}, Хеш: {hashed}")