from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from sqlalchemy.util import typing
from src.systemOfSchoolSchedule.dbConfig.connection import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.systemOfSchoolSchedule.models.schoolClass import SchoolClass
    from src.systemOfSchoolSchedule.models.roleUser import RoleUser
    from src.systemOfSchoolSchedule.models.standardSchedule import StandardSchedule
    from src.systemOfSchoolSchedule.models.changeSchedule import ChangeSchedule


class User(Base):
    __tablename__ = 'users'

    userId: Mapped[int] = mapped_column("userId",sa.Integer, primary_key=True)
    login: Mapped[str] = mapped_column("login",sa.String, nullable=False, unique=True)
    passwordHash: Mapped[str] = mapped_column("passwordHash",sa.String, nullable=False)
    fullName: Mapped[str] = mapped_column("fullName",sa.String, nullable=False)

    #Внешний ключ в классе
    classId: Mapped[typing.Optional[int]] = mapped_column("classId", sa.ForeignKey("schoolClasses.classId"),
                                                          nullable=True)

    #Связи

    #Класс, где пользователь учится
    schoolClass: Mapped[typing.Optional["SchoolClass"]] = relationship(
        argument="SchoolClass", foreign_keys=[classId], back_populates="students"
    )

    #Класс, где пользователь является классным руководителем
    ledClass: Mapped[typing.Optional["SchoolClass"]] = relationship(
        argument="SchoolClass", primaryjoin="User.userId == SchoolClass.classLeaderId",
        back_populates = "classLeader",
        uselist=False
    )

    #Роли пользователя
    roles: Mapped[list["RoleUser"]] = relationship(
        argument="RoleUser", back_populates="user"
    )

    #Стандартное расписание(Teacher)
    standardSchedule: Mapped[typing.Optional["StandardSchedule"]] = relationship(
        argument="StandardSchedule", back_populates="teacher"
    )

    #Изменения в расписании (Teacher)
    changeSchedule: Mapped[typing.Optional["ChangeSchedule"]] = relationship(
        argument="ChangeSchedule", back_populates="teacher"
    )