from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from sqlalchemy.util import typing
from src.systemOfSchoolSchedule.dbConfig.connection import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.systemOfSchoolSchedule.models.user import User
    from src.systemOfSchoolSchedule.models.standardSchedule import StandardSchedule
    from src.systemOfSchoolSchedule.models.changeSchedule import ChangeSchedule

class SchoolClass(Base):
    __tablename__ = 'schoolClasses'

    classId: Mapped[int] = mapped_column("classId", sa.Integer, primary_key=True)
    className: Mapped[str] = mapped_column("className", sa.String, nullable=False)

    classLeaderId: Mapped[typing.Optional[int]] = mapped_column(
        "classLeaderId", sa.ForeignKey("users.userId",ondelete="SET NULL"), nullable=True)

    #Связи
    students: Mapped[list["User"]] = relationship(
        argument="User",
        foreign_keys="User.classId",
        back_populates="schoolClass"
    )

    #Классный руководитель
    classLeader: Mapped[typing.Optional["User"]] = relationship(
        argument="User",
        primaryjoin="SchoolClass.classLeaderId == User.userId",
        back_populates="ledClass"
    )

    #Стандартное расписание
    standardSchedules: Mapped[list["StandardSchedule"]] = relationship(
        argument="StandardSchedule",
        back_populates="schoolClass"
    )

    #Изменение расписания
    changeSchedules: Mapped[list["ChangeSchedule"]] = relationship(
        argument="ChangeSchedule",
        back_populates="schoolClass"
    )