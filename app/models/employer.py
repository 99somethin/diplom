from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import Base

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project


class Employer(Base):
    __tablename__ = "employers"

    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_description: Mapped[Optional[str]] = mapped_column(
        String(2000), nullable=True
    )
    industry: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="employer_profile", passive_deletes=True
    )

    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="employer", cascade="all, delete-orphan"
    )
