from src.systemOfSchoolSchedule.services.scheduleService import interactiveScheduleViewer, interactiveScheduleViewerForTeacher
from src.systemOfSchoolSchedule.repositories.schoolClassRepository import getIdClassByName, createClass, deleteClass
from src.systemOfSchoolSchedule.repositories.userRepostiory import getIdUserByName, createUser, deleteUserById, getUserClassIdById
from src.systemOfSchoolSchedule.repositories.roleUserRepository import getRoleById
from src.systemOfSchoolSchedule.repositories.scheduleRepository import createChangeInSchedule, createStandardScheduleLesson, updateStandardScheduleLesson
from src.systemOfSchoolSchedule.repositories.subjectRepository import createSubject, deleteSubject
from src.systemOfSchoolSchedule.services.schoolClassService import displayClassStudents

def adminMenu(user):

    while True:

        print(f"""\nАдминистратор ({user.login}) 
1.Посмотреть расписание класса
2.Посмотреть расписание учителя
3.Добавить пользователя
4.Удалить пользователя
5.Добавить класс
6.Удалить класс
7.Изменить расписание единично
8.Создать школьное расписание для класса
9.Изменить расписание у определенного класса
10.Добавить предмет
11.Удалить предмет
0.Выход
""")
        choice = input("Выберите действие: ")

        if choice == "1": #Просмотр расписания класса
            classId = getIdClassByName(input("Введите класс, расписание которого хотите посмотреть: "))
            if not classId:
                print("Нет такого класса")
                continue
            interactiveScheduleViewer(classId)


        elif choice == "2": #Просмотр расписания учителя
            teacherId = getIdUserByName(input("Введите ФИО вашего учителя: "))

            if not teacherId:
                print("Нет такого учителя")
                continue

            userRole = getRoleById(teacherId).roleName

            if userRole not in ["teacher", "classTeacher"]:
                print("Пользователь не является учителем")
                continue

            interactiveScheduleViewerForTeacher(teacherId)

            teacherId = None
            userRole = None

        elif choice == "3": #Создание пользователя
            login = input("Введите логин пользователя: ")
            passwordHash = input("Введите пароль: ")
            fullName = input("Введите ФИО: ")
            roleName = input("Введите роль, которую получит пользователь: ")
            className = input("Введите класс пользователя, если его нет - NONE")
            if not className:
                classId = None
            else:
                try:
                    classId = getIdClassByName(className)
                except Exception as e:
                    print("Нет такого класса")
                    continue
            if roleName not in ["admin", "manager", "classTeacher", "teacher", "student"]:
                print("Нет такой роли")
                continue

            userTest = createUser(login, passwordHash, fullName, classId, roleName)

            if not userTest:
                print("Этот пользователь не может быть классным руководителем этого класса")
                continue

            login = None
            passwordHash = None
            fullName = None
            roleName = None
            classId = None
            className = None
            roleName = None
            userTes = None

        elif choice == "4": #удаление пользователя
            id = getIdUserByName(input("Введите ФИО пользователя, которого хотите удалить"))
            if not id:
                print("Нет такого пользователя")
                continue
            deleteUserById(id)
            id = None

        elif choice == "5":  #Создание класса
            className = input("Введите название класса, который вы хотите создать")
            classLeaderId = getIdUserByName(input("Введите ФИО вашего учителя"))
            if not classLeaderId:
                print("Такого учителя нет")
                continue
            userRole = getRoleById(classLeaderId).roleName

            if userRole not in ["teacher", "classTeacher"]:
                print("Этот пользователь не является учителем")
                continue
            userClassId = getUserClassIdById(classLeaderId)

            if userClassId is not None:
                print("Учитель уже является классным руководителем другого класса")
                continue

            createClass(className, classLeaderId)
            className = None
            classLeaderId = None
            userRole = None
            userClassId = None

        elif choice == "6": #удаление класса
            className = input("Введите название класса, который вы хотите удалить")
            deleted = bool(deleteClass(className))
            if not deleted:
                print(f"Класса {className} не существует")
                continue

            print(f"Класс {className} успешно удален!")
            className = None
            deleted = None


        elif choice == "7": #изменение расписания единоразово
            changeDate = input("Введите вашу дату в формате YYYY-MM-DD: ")
            lessonNumber = int(input("Введите номер урока, который надо заменить"))
            className = input("Введите класс, у которого должна быть замена")
            teacherName= input("Введите ФИО преподавателя: ")
            subjectName = input("Введите название предмета:")
            changeType = int(input("Введи тип изменения [0,1,2]"))

            createChangeInSchedule(changeDate, lessonNumber, className, teacherName, subjectName, changeType)
            changeDate = None
            lessonNumber = None
            className = None
            teacherName = None
            subjectName = None
            changeType = None


        elif choice == "8": #изменение расписания в целом
            dayOfWeek = int(input("введите день недели в числовом формате, где 0 - ПН, 6-ВС: "))
            lessonNumber = int(input("Введите номер урока, который хотите добавить: "))
            className = input("Введите класс, у которого должна быть замена: ")
            teacherName = input("Введите ФИО преподавателя: ")
            subjectName = input("Введите название предмета: ")
            createStandardScheduleLesson(dayOfWeek,lessonNumber,className,teacherName,subjectName)
            dayOfWeek = None
            lessonNumber = None
            className = None
            teacherName = None
            subjectName = None

        elif choice == "9": #Изменение школьного расписания
            dayOfWeek = int(input("введите день недели в числовом формате, где 0 - ПН, 6-ВС: "))
            lessonNumber = int(input("Введите номер урока, который хотите добавить: "))
            className = input("Введите класс, у которого должна быть замена: ")
            teacherName = input("Введите ФИО преподавателя: ")
            subjectName = input("Введите название предмета: ")
            updateStandardScheduleLesson(dayOfWeek,lessonNumber,className,teacherName,subjectName)
            dayOfWeek = None
            lessonNumber = None
            className = None
            teacherName = None
            subjectName = None

        elif choice == "10": #Добавить предмет
            subjectName = input("Введите название предмета, который хотите добавить")
            a=createSubject(subjectName)
            print(a.subjectName)
            subjectName = None
        elif choice == "11": #Удалить предмет
            subjectName = input("Введите название предмета, который хотите удалить")
            deleteSubject(subjectName)
            subjectName = None
        elif choice == "0":
            print("До свидания")
            break
        else:
            print("Нет такого варианта действия")



def studentMenu(user):
    while True:
        print(f"""\nСтудент ({user.login}) 
1.Посмотреть свое расписание
0.Выход
""")
        choice = input("Выберите действие: ")
        if choice == "1":
            interactiveScheduleViewer(user.classId)
        elif choice == "0":
            print("До свидания")
            break
        else:
            print("Нет такого варианта действий")


def teacherMenu(user):
    while True:
        print(f"""\nСтудент ({user.login}) 
1.Посмотреть свое расписание
2.Посмотреть расписание класса
0.Выход
""")
        choice = input("Выберите действие: ")
        if choice == "1":
            interactiveScheduleViewerForTeacher(user.userId)
        elif choice == "2":
            classId = getIdClassByName(input("Введите класс, расписание которого хотите посмотреть: "))
            if not classId:
                print("Нет такого класса")
                continue
            interactiveScheduleViewer(classId)

            classId = None

        elif choice == "0":
            print("До свидания")
            break
        else:
            print("Нет такого варианта действий")


def classTeacherMenu(user):
    while True:
        print(f"""\nКЛАССНЫЙ РУКОВОДИТЕЛЬ ({user.login}) 
1.Посмотреть свое расписание
2.Посмотреть расписание класса
3.Посмотреть состав своего класса
0.Выход
""")
        choice = input("Выберите действие: ")
        if choice == "1":
            interactiveScheduleViewerForTeacher(user.userId)
        elif choice == "2":
            classId = getIdClassByName(input("Введите класс, расписание которого хотите посмотреть: "))
            if not classId:
                print("Нет такого класса")
                continue
            interactiveScheduleViewer(classId)

            classId = None


        elif choice == "3":
            displayClassStudents(user.userId)

        elif choice == "0":
            print("До свидания")
            break
        else:
            print("Нет такого варианта действий")

