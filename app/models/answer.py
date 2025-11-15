from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import Base

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
        from app.models.candidate import Candidate
        from app.models.project import Project

class Answer(Base):
    __tablename__ = "answers"

    answear_link: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    review_feedback: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)

    candidate_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )
    candidate: Mapped["Candidate"] = relationship(
        "Candidate", back_populates="answers", passive_deletes=True
    )

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    project: Mapped["Project"] = relationship(
        "Project", back_populates="answers", passive_deletes=True
    )
