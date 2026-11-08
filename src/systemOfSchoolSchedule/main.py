from src.systemOfSchoolSchedule.repositories.roleUserRepository import getRoleById
from src.systemOfSchoolSchedule.dbConfig.connection import initDb
from src.systemOfSchoolSchedule.services.authService import createDefaultAdmin
from src.systemOfSchoolSchedule.auth import login
from src.systemOfSchoolSchedule.menu import adminMenu, studentMenu, teacherMenu, classTeacherMenu

def main():
    initDb()
    createDefaultAdmin()

    while True:
        user = login()
        if not user:
            continue

        userRole = getRoleById(user.userId).roleName
        if userRole == "admin":
            adminMenu(user)
        elif userRole == "manager":
            adminMenu(user)

        elif userRole == "classTeacher":
            classTeacherMenu(user)

        elif userRole == "teacher":
            teacherMenu(user)

        elif userRole == "student":
            studentMenu(user)
        else:
            print("Нет такой роли")

if __name__ == "__main__":
    main()
