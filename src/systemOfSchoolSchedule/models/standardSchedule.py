from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from src.systemOfSchoolSchedule.dbConfig.connection import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.systemOfSchoolSchedule.models.schoolClass import SchoolClass
    from src.systemOfSchoolSchedule.models.user import User
    from src.systemOfSchoolSchedule.models.subject import Subject

class StandardSchedule(Base):
    __tablename__ = "standardSchedule"

    standardScheduleId: Mapped[int] = mapped_column("standardScheduleId",
                                                    sa.Integer,
                                                    primary_key=True)
    dayOfWeek: Mapped[int] = mapped_column("dayOfWeek",
                                           sa.Integer,
                                           nullable=False)

    lessonNumber: Mapped[int] = mapped_column("lessonNumber",
                                              sa.Integer,
                                              nullable=False)
    #Внешний ключ на класс, у которого идет урок
    classId: Mapped[int] = mapped_column("classId",
                                         sa.ForeignKey("schoolClasses.classId"),
                                         nullable=False)
    #Внешний ключ на учителя, который ведет этот урок
    teacherId: Mapped[int] = mapped_column("teacherId",
                                           sa.ForeignKey("users.userId"),
                                           nullable=False)

    #Внешний ключ на предмет
    subjectId: Mapped[int] = mapped_column("subjectId",
                                           sa.ForeignKey("subjects.subjectId"),
                                           nullable=False)

    #Связи
    schoolClass: Mapped["SchoolClass"] = relationship(argument="SchoolClass",
                                                      back_populates="standardSchedules")

    teacher: Mapped["User"] = relationship(argument="User",
                                           back_populates="standardSchedule")

    subject: Mapped["Subject"] = relationship(argument="Subject",
                                              back_populates="standardSchedules")
