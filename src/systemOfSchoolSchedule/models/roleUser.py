from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from src.systemOfSchoolSchedule.dbConfig.connection import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.systemOfSchoolSchedule.models.user import User

class RoleUser(Base):
    __tablename__ = "roleUser"

    roleId: Mapped[int] = mapped_column("roleId",
                                        sa.Integer,
                                        primary_key=True
    )
    userId: Mapped[int] = mapped_column("userId",
                                        sa.ForeignKey("users.userId", ondelete="CASCADE"),)
    roleName: Mapped[str] = mapped_column("roleName", sa.String)

   #роль пользователя
    user: Mapped["User"] = relationship(
        argument="User",
        back_populates="roles"
    )

    def __repr__(self) -> str:
        return f"UserId - {self.userId}, roleName - {self.roleName}"