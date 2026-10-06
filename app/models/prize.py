from datetime import datetime

from sqlmodel import Field, SQLModel


class Prize(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = ""
    cost: int


class Redemption(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id", index=True)
    prize_id: int = Field(foreign_key="prize.id", index=True)
    status: str = "pending"
    redeemed_at: datetime = Field(default_factory=datetime.utcnow)
    confirmed_by: int | None = Field(default=None, foreign_key="user.id")
    confirmed_at: datetime | None = None