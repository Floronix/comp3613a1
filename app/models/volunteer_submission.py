from sqlmodel import Field, SQLModel
from datetime import datetime

class VolunteerSubmission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id")
    activity: str
    hours: float
    description: str
    status: str = "pending"
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_by: int | None = Field(default=None, foreign_key="user.id")
    reviewed_at: datetime | None = None