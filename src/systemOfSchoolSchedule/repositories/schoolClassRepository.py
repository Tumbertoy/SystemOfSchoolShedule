from repositories.roleUserRepository import getRoleById
from src.systemOfSchoolSchedule.models.user import User
from src.systemOfSchoolSchedule.models.schoolClass import SchoolClass
from src.systemOfSchoolSchedule.dbConfig.connection import Session
from src.systemOfSchoolSchedule.repositories.userRepostiory import getUserById


def getNameClassById(schoolClassId: int) -> str:
    with Session() as session:
        name = session.query(SchoolClass).filter(SchoolClass.classId == schoolClassId).first().className
        return name


def getIdClassByName(nameClass: str) -> int:
    with Session() as session:
        classId = session.query(SchoolClass).filter(SchoolClass.className == nameClass).first()
        return classId.classId



def getFullClass(schoolClassId: int) -> list:
    with Session() as session:
        fullClass = session.query(SchoolClass).filter(SchoolClass.id == schoolClassId).all()
        names = []
        for student in fullClass:
            names.append(student.className)
    return names

def createClass(className:str,classLeaderId:int):
    with Session.begin() as session:
        classExists = session.query(SchoolClass).filter(SchoolClass.className == className).first()
        if classExists:
            print(f"Класс {className} уже существует")
            return classExists

        userClassTeacher = session.query(User).filter(User.userId == classLeaderId).first()

        if getRoleById(classLeaderId).roleName != "classTeacher":
            print("Это не классный руководитель")
            return userClassTeacher

        if userClassTeacher.classId != None:
            print("Этот учитель уже является классным руководителем другого класса")
            return userClassTeacher

        newClass = SchoolClass(className=className,classLeaderId=classLeaderId)
        session.add(newClass)
        session.flush()
        classId = newClass.classId

    updateTeacherId(classLeaderId, classId)





def deleteClass(className:str):
    with Session() as session:
        classForDelete = session.query(SchoolClass).filter(SchoolClass.className == className).first()
        if classForDelete:
            session.delete(classForDelete)
            return 1
        else:
            return 0

def getStudentsByClassLeader(classLeaderId:int):
    with Session.begin() as session:
        schoolClass = session.query(SchoolClass).filter(SchoolClass.classLeaderId == classLeaderId).first()
        if not schoolClass:
            return []

        students = session.query(User).filter(User.classId == SchoolClass.classId).order_by(User.fullName.asc()).all()

        return students



def updateTeacherId(userId: int, classId: int):
    with Session.begin() as session:

        teacher = session.query(User).filter(User.userId==userId).first()
        if teacher:
            teacher.classId = classId

