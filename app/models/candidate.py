from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import Base

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.answer import Answer


class Candidate(Base):
    __tablename__ = "candidates"

    bio: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    resume_link: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="candidate_profile", passive_deletes=True
    )

    answers: Mapped[List["Answer"]] = relationship(
        "Answer", back_populates="candidate", cascade="all, delete-orphan"
    )
