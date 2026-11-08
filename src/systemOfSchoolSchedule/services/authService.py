import hashlib
from src.systemOfSchoolSchedule.models.user import User
import src.systemOfSchoolSchedule.repositories.userRepostiory as userRepository

studentRoleId = 1
teacherRoleId = 2
managerRoleId = 3
adminRoleId = 4


def hashPassword(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(login: str, password: str) -> User | None:
    user = userRepository.getUserByLogin(login)

    if not user:
        return None

    if user.passwordHash != hashPassword(password):
        return None

    return user


def createDefaultAdmin():
    if userRepository.getUserByLogin("admin"):
        return
    userRepository.createUser("admin", hashPassword("admin"), "Admin", None, "admin")


def registerClassTeacher():
    pass

def registerManager():
    pass

def registerUser():
    pass


