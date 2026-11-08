import hashlib

from src.systemOfSchoolSchedule.models import RoleUser, SchoolClass
from src.systemOfSchoolSchedule.models.user import User
from src.systemOfSchoolSchedule.dbConfig.connection import Session



def hashPassword(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def createUser(login, passwordHash, fullname, classId, roleName):


    with Session.begin() as session:


        userExists = session.query(User).filter(User.login == login).first()
        if userExists:
            print(f"Пользователь {userExists.login} уже существует")
            return userExists

        hashedPassword = hashPassword(passwordHash)
        user = User(
            login=login,
            passwordHash=hashedPassword,
            fullName=fullname,
            classId=classId
        )


        session.add(user)
        session.flush()

        if roleName == "classTeacher" and classId:
            schoolClass = session.query(SchoolClass).filter(SchoolClass.classId == classId).first()
            if schoolClass.classLeaderId:
                return None
            schoolClass.classLeaderId = user.userId


        userRole = RoleUser(
            userId = user.userId,
            roleName=roleName
        )

        session.add(userRole)
        return user

def getUserByLogin(login:str) -> User | None:
    with Session.begin() as session:
        user = session.query(User).filter(User.login == login).first()
    return user if user else None

def getUserById(id:int):
    with Session.begin() as session:
        user = session.query(User).filter(User.userId == id).first()
        return user if user else None

def getNameById(id: int) -> str | None:
    with Session.begin() as session:
        user = session.query(User).filter(User.userId == id).first()
    return user.fullName if user else None


def transferUserToClass(id: int, newClassId: int):
    with Session.begin() as session:
        user = session.query(User).filter(User.userId == id).first()
        if user:
            user.className = newClassId
            session.commit()
            print(f"Класс пользователя {user.userId} успешно изменен на {newClassId} ")
        else:
            print("Пользователь не найден!")

def getIdUserByName(fullName: str):
    with Session.begin() as session:
        user = session.query(User).filter(User.fullName == fullName).first()
        return user.userId if user else None


def deleteUserById(id:int):
    with Session.begin() as session:
        user = session.query(User).filter(User.userId == id).first()
        userRole =session.query(RoleUser).filter(RoleUser.userId == id).first()
        if user:
            session.delete(user)
            session.delete(userRole)

def getUserClassIdById(id:int):
    with Session.begin() as session:
        user = session.query(User).filter(User.userId == id).first()
        return user.classId if user else None