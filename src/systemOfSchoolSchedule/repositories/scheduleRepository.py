import datetime

from models import SchoolClass, User, Subject, StandardSchedule,ChangeSchedule
from src.systemOfSchoolSchedule.repositories.subjectRepository import getSubjectIdByName
from src.systemOfSchoolSchedule.repositories.schoolClassRepository import getIdClassByName
from src.systemOfSchoolSchedule.repositories.userRepostiory import getIdUserByName
from src.systemOfSchoolSchedule.dbConfig.connection import Session
from src.systemOfSchoolSchedule.repositories.subjectRepository import getSubjectById



def validateChangeInput(changeDate: str, lessonNumber:int, className:str, teacherName:str, subjectName:str, changeType:int) -> tuple[bool,str]:
    #Проверка формата даты
    try:
        parsedDate = datetime.datetime.strptime(changeDate, "%Y.%m.%d").date()
    except ValueError:
        return False, "Неверный формат даты! Ожидается ГГГГ.ММ.ДД (например, 2026.10.28"

    #Проверка логических границ даты
    if parsedDate < datetime.date.today() - datetime.timedelta(days=30):
        return False, "Нельзя вносить изменения в расписание более чем на месяц вперед"

    #Проверка номера урока
    if not(1<=lessonNumber<=8):
        return False, "Номер урока должен быть в диапазоне от 1 до 8"

    #Проверка существования сущностей в БД
    with Session() as session:
        #Проверяем класс
        classExists = session.query(SchoolClass).filter(SchoolClass.className == className).first()
        if not classExists:
            return False, f"Класс  {className} не существует в Базе данных"

        #Если это замена, то учитель и предмет обязательны
        if changeType == 1 or changeType == 2:
            if not teacherName or not subjectName:
                return False, "Для замены (1) или добавления (2)  необходимо указать ФИО учителя и название предмета"

            teacherExists = session.query(User).filter(User.fullName == teacherName).first()
            if not teacherExists:
                return False, f"Учитель {teacherName} не найден."

            subjectExists = session.query(Subject).filter(Subject.subjectName == subjectName).first()
            if not subjectExists:
                return False, f"Предмет {subjectName} не найден."

            teacherBusyInChanges = session.query(ChangeSchedule).filter(
                ChangeSchedule.changeDate == parsedDate,
                ChangeSchedule.lessonNumber == lessonNumber,
                ChangeSchedule.teacherId == getIdUserByName(teacherName),
                ChangeSchedule.classId != getIdClassByName(className),
                ChangeSchedule.changeType.in_([1,2])
            ).first()

            if teacherBusyInChanges:
                return False, f"Учитель {teacherName} на дату {changeDate} на {lessonNumber}-м уже ведет урок с другим классом"

            dayOfWeek = parsedDate.weekday()

            standardLesson = session.query(StandardSchedule).filter(
                StandardSchedule.dayOfWeek == dayOfWeek,
                StandardSchedule.lessonNumber == lessonNumber,
                StandardSchedule.teacherId == getIdUserByName(teacherName),
                StandardSchedule.classId != getIdClassByName(className)
            ).first()

            if standardLesson:

                isStandardLessonCancelled = session.query(ChangeSchedule).filter(
                    ChangeSchedule.changeDate == parsedDate,
                    ChangeSchedule.lessonNumber == lessonNumber,
                    ChangeSchedule.classId == getIdClassByName(className),
                    ChangeSchedule.chngeType == 0
                ).first()

                if not isStandardLessonCancelled:
                    return False, f"Учитель {teacherName} занят: по основному расписанию у него урок в другом классе!"




        elif changeType ==  0:
            if teacherName is not None or subjectName is not None:
                return False, "Для отмены урока (False) поля teacherId, subjectId, должны быть пустыми (None)"
    return True, "OK"




def createChangeInSchedule(changeDate: str, lessonNumber:int, className:str, teacherName: str, subjectName:str, changeType:int):
    validation, msg = validateChangeInput(changeDate, lessonNumber, className, teacherName, subjectName, changeType)
    if not validation:
        print(f"[bold red]Ошибка валидации:[/bold red] {msg}")
    else:

        parsedDate = datetime.datetime.strptime(changeDate, "%Y.%m.%d").date()

        with Session.begin() as session:
            changeSchedule = ChangeSchedule(changeDate=parsedDate,
                                            lessonNumber=lessonNumber,
                                            classId=getIdClassByName(className),
                                            teacherId=getIdUserByName(teacherName),
                                            subjectId=getSubjectIdByName(subjectName),
                                            changeType=changeType)
            session.add(changeSchedule)




def getScheduleForClass(classId:int, startOfWeekDate) -> dict:
    with Session() as session:

        #Стандартное расписание
        schedules = session.query(StandardSchedule).filter(StandardSchedule.classId == classId).order_by(
            StandardSchedule.dayOfWeek.asc(),
            StandardSchedule.lessonNumber.asc()).all()

        weeklySchedule = {i: [] for i in range(7)}

        for item in schedules:
            lessonNumber = item.lessonNumber
            teacherId = item.teacherId
            subject = getSubjectById(item.subjectId)
            weeklySchedule[item.dayOfWeek].append([lessonNumber, subject, teacherId])

    #Один запрос на единичные замены
    endOfWeekDate = startOfWeekDate + datetime.timedelta(days=6)
    changes = session.query(ChangeSchedule).filter(ChangeSchedule.classId == classId,
                                                   ChangeSchedule.changeDate >= startOfWeekDate,
                                                   ChangeSchedule.changeDate <= endOfWeekDate).order_by(ChangeSchedule.changeScheduleId.desc()).all()
    for change in changes:
        dayIndex = change.changeDate.weekday()
        dayLessons = weeklySchedule[dayIndex]

        if change.changeType == 2: #добавление
            dayLessons.append([change.lessonNumber,  f"[bold yellow]{change.subject}[/bold yellow]", change.teacherId])
            continue

        for idx, lesson in enumerate(dayLessons):
            if lesson[0] == change.lessonNumber:
                if change.changeType == 0: #отмена
                    dayLessons[idx][1] = f"[strike dim]{lesson[1]} (ОТМЕНЕН)[/strike dim]"

                elif change.changeType == 1: #замена
                    dayLessons[idx][1] = f"[strike dim]{lesson[1]}[/strike dim] -> [bold yellow]{change.subject.subjectName}"
                    dayLessons[idx][2] = change.teacherId
                break

    #Сортируем значения
    for dayIndex in range(7):
        weeklySchedule[dayIndex].sort(key=lambda x: x[0])

    return weeklySchedule


def getScheduleForTeacher(teacherId: int, startOfWeekDate) -> dict:
    with Session() as session:



        schedules = session.query(StandardSchedule).filter(StandardSchedule.teacherId == teacherId).order_by(
            StandardSchedule.dayOfWeek.asc(),
            StandardSchedule.lessonNumber.asc()).all()

        weeklySchedule = {i: [] for i in range(7)}

        for item in schedules:
            lessonNumber = item.lessonNumber
            classId = item.classId
            subject = getSubjectById(item.subjectId)
            weeklySchedule[item.dayOfWeek].append([lessonNumber, subject ,classId])

    #Один запрос на единичные замены
    endOfWeekDate = startOfWeekDate + datetime.timedelta(days=6)
    changes = session.query(ChangeSchedule).filter(ChangeSchedule.teacherId == teacherId,
                                                   ChangeSchedule.changeDate >= startOfWeekDate,
                                                   ChangeSchedule.changeDate <= endOfWeekDate).order_by(ChangeSchedule.changeScheduleId.desc()).all()
    for change in changes:
        dayIndex = change.changeDate.weekday()
        dayLessons = weeklySchedule[dayIndex]

        if change.changeType == 2: #добавление
            dayLessons.append([change.lessonNumber, f"[bold yellow]{change.subject}[/bold yellow]", change.classId])
            continue

        for idx, lesson in enumerate(dayLessons):
            if lesson[0] == change.lessonNumber:
                if change.changeType == 0: #отмена
                    dayLessons[idx][1] = f"[strike dim]{lesson[1]} (ОТМЕНЕН)[/strike dim]"

                elif change.changeType == 1: #замена
                    dayLessons[idx][1] = f"[strike dim]{lesson[1]}[/strike dim] -> [bold yellow]{change.subject.subjectName}"
                    dayLessons[idx][2] = change.classId
                break

    #Сортируем значения
    for dayIndex in range(7):
        weeklySchedule[dayIndex].sort(key=lambda x: x[0])

    return weeklySchedule


def validateStandardSchedule(dayOfWeek:int, lessonNumber:int, className:str, teacherName:str, subjectName:str) -> tuple[bool, str]:

    if not(0<=dayOfWeek<=6):
        return False, "dayOfWeek должен быть в диапазоне от 0 до 6"

    if not(1<=lessonNumber<=8):
        return False, "lessonNumber должнен быть в диапазоне от 1 до 8"
    with Session() as session:

        classExists = session.query(SchoolClass).filter(SchoolClass.className == className).first()
        if not classExists:
            return False, f"Класса {className} не существует."

        teacherExists = session.query(User).filter(User.fullName == teacherName).first()
        if not teacherExists:
            return False, f"Учитель {teacherName} не найден."

        subjectExists = session.query(Subject).filter(Subject.subjectName == subjectName).first()
        if not subjectExists:
            return False, f"Предмет {subjectName} не найден."

        teacherBusy = session.query(StandardSchedule).filter(
            StandardSchedule.dayOfWeek == dayOfWeek,
            StandardSchedule.lessonNumber == lessonNumber,
            StandardSchedule.teacherId == getIdUserByName(teacherName),
            StandardSchedule.classId != getIdClassByName(className)
        ).first()
        if teacherBusy:
            return False, f"Учитель {teacherName} в этот час уже ведет урок в другом классе"

    return True, "Ok"


def createStandardScheduleLesson(dayOfWeek:int, lessonNumber:int, className:str, teacherName:str, subjectName:str):
    with Session.begin() as session:
        validation, msg =validateStandardSchedule(dayOfWeek,lessonNumber,className,teacherName,subjectName)
        if not validation:
            print(f"[bold red]Ошибка валидации:[/bold red] {msg}")
        else:
            lessonExists = session.query(StandardSchedule).filter(StandardSchedule.classId == getIdClassByName(className),
                                                                  StandardSchedule.dayOfWeek == dayOfWeek,
                                                                  StandardSchedule.lessonNumber == lessonNumber).first()
            if lessonExists:
                return f"У класса {className} в день {dayOfWeek} на {lessonNumber} уроке уже стоит предмет."

            newLesson = StandardSchedule(
                dayOfWeek=dayOfWeek,
                lessonNumber=lessonNumber,
                classId=getIdClassByName(className),
                teacherId=getIdUserByName(teacherName),
                subjectId=getSubjectIdByName(subjectName)
            )
            session.add(newLesson)
    return newLesson

def updateStandardScheduleLesson(dayOfWeek: int, lessonNumber: int, className:str, teacherName:str, subjectName:str):
    with Session() as session:
        validateStandardSchedule(dayOfWeek,lessonNumber,className,teacherName,subjectName)

        lesson = session.query(StandardSchedule).filter(StandardSchedule.classId == getIdClassByName(className),
                                                        StandardSchedule.dayOfWeek == dayOfWeek,
                                                        StandardSchedule.lessonNumber == lessonNumber).first()
        if not lesson:
            return f"Невозможно изменить урок: в шаблоне класса {className} еще нет {lessonNumber}-го урока в день {dayOfWeek}"

        with session.begin():
            lesson.teacherId = getIdUserByName(teacherName)
            lesson.subjectId = getSubjectIdByName(subjectName)
    return lesson