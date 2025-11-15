import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING, Optional

from app.db.database import Base

if TYPE_CHECKING:
        from app.models.candidate import Candidate
        from app.models.employer import Employer

class UserRole(str, enum.Enum):
    candidate = "candidate"
    employer = "employer"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(55), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[enum.Enum] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)

    profile_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    candidate_profile: Mapped[Optional["Candidate"]] = relationship(
        "Candidate",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    employer_profile: Mapped[Optional["Employer"]] = relationship(
        "Employer",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )