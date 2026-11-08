from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from src.systemOfSchoolSchedule.dbConfig.connection import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.systemOfSchoolSchedule.models.standardSchedule import StandardSchedule
    from src.systemOfSchoolSchedule.models.changeSchedule import ChangeSchedule

class Subject(Base):
    __tablename__ = "subjects"
    subjectId: Mapped[int] = mapped_column("subjectId", sa.Integer,primary_key=True)
    subjectName: Mapped[str] = mapped_column("subjectName", sa.String, nullable=False)


    #связи
    standardSchedules: Mapped[list["StandardSchedule"]] = relationship(
        argument="StandardSchedule",
        back_populates="subject"
    )

    changeSchedules: Mapped[list["ChangeSchedule"]] = relationship(
        argument="ChangeSchedule",
        back_populates="subject"
    )