from src.systemOfSchoolSchedule.services.authService import authenticate

def login():
    print("\nЛичный кабинет")

    loginValue = input("Логин: ")
    passwordValue = input("Пароль: ")

    user = authenticate(loginValue, passwordValue)

    if not user:
        print("\nНеверный логин или пароль")
        return None

    print(f"\nДобро пожаловать, {user.fullName}")
    return user


