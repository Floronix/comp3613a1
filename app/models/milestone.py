from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class Milestone(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    threshold: int = Field(index=True, unique=True)
    badge_icon: str
    reward: int


class StudentMilestone(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("student_id", "milestone_id", name="uq_student_milestone"),
    )

    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id", index=True)
    milestone_id: int = Field(foreign_key="milestone.id", index=True)
    points_awarded: int
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)
    notification_pending: bool = Field(default=True)