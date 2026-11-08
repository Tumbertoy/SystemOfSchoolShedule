from src.systemOfSchoolSchedule.models.roleUser import RoleUser
from src.systemOfSchoolSchedule.dbConfig.connection import Session
##админ, завуч, классРук, учитель, ученик

def getAll() -> list[RoleUser]:
    with Session.begin() as session:
        users = session.query(RoleUser).all()
        return [RoleUser(userId=user[1],
                         roleName=user[2]) for user in users]


def getRoleById(userId: int) -> RoleUser | None:
    with Session.begin() as session:
        user = session.query(RoleUser).filter(RoleUser.userId == userId).first()
        return RoleUser(userId=user.userId, roleName=user.roleName)


