from sqlalchemy import Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.db.database import Base

from datetime import date

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
        from app.models.employer import Employer
        from app.models.answer import Answer

class Project(Base):
    __tablename__ = "projects"

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(4000), nullable=False)
    # необходимые навыки
    requirements: Mapped[Optional[JSONB]] = mapped_column(JSONB, nullable=True)
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    employer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("employers.id", ondelete="CASCADE"), nullable=False
    )
    employer: Mapped["Employer"] = relationship(
        "Employer", back_populates="projects", passive_deletes=True
    )

    answers: Mapped[List["Answer"]] = relationship(
        "Answer", back_populates="project", cascade="all, delete-orphan"
    )
