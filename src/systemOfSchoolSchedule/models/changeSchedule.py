from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from src.systemOfSchoolSchedule.dbConfig.connection import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.systemOfSchoolSchedule.models.schoolClass import SchoolClass
    from src.systemOfSchoolSchedule.models.user import User
    from src.systemOfSchoolSchedule.models.subject import Subject

class ChangeSchedule(Base):
    __tablename__ = "changeSchedule"

    changeScheduleId: Mapped[int] = mapped_column("changeScheduleId",
                                                  sa.Integer,
                                                  primary_key=True)
    changeDate: Mapped[date] = mapped_column("changeDate",
                                                 sa.Date,
                                                 nullable=False)
    lessonNumber: Mapped[int] = mapped_column("lessonNumber",
                                              sa.Integer,
                                              nullable=False)

    classId: Mapped[int] = mapped_column("classId",
                                         sa.ForeignKey("schoolClasses.classId"),
                                         nullable=False)

    teacherId: Mapped[int] = mapped_column("teacherId",
                                           sa.ForeignKey("users.userId"),
                                           nullable=False)
    subjectId: Mapped[int] = mapped_column("subjectId",
                                           sa.ForeignKey("subjects.subjectId"),
                                           nullable=False)

    changeType: Mapped[int] = mapped_column("changeType",
                                             sa.Integer,
                                             nullable=False)
    #Связи
    schoolClass: Mapped["SchoolClass"] = relationship(argument="SchoolClass", back_populates="changeSchedules")

    teacher: Mapped["User"] = relationship(argument="User", back_populates="changeSchedule")

    subject: Mapped["Subject"] = relationship(argument="Subject", back_populates="changeSchedules")