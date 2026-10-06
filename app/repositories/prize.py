from datetime import datetime

from sqlmodel import Session, select

from app.models.prize import Prize, Redemption
from app.models.user import User
from app.repositories.milestone import MilestoneRepository

PRIZE_CATALOG = (
    ("Coffee Voucher", 50),
    ("$10 Amazon Gift Card", 200),
    ("Campus Water Bottle", 400),
    ("Movie Ticket", 600),
    ("Campus Hoodie", 1000),
    ("Laptop", 5000),
)


class PrizeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_prizes(self) -> list[Prize]:
        prizes = self.db.exec(select(Prize).order_by(Prize.cost)).all()
        if not prizes:
            for name, cost in PRIZE_CATALOG:
                self.db.add(Prize(name=name, cost=cost))
            self.db.commit()
            prizes = self.db.exec(select(Prize).order_by(Prize.cost)).all()
        return prizes

    def get_redemption_history(
        self,
        student_id: int | None = None,
    ) -> list[tuple[Redemption, Prize, User]]:
        statement = (
            select(Redemption, Prize, User)
            .join(Prize, Prize.id == Redemption.prize_id)
            .join(User, User.id == Redemption.student_id)
            .order_by(Redemption.redeemed_at.desc())
        )
        if student_id is not None:
            statement = statement.where(Redemption.student_id == student_id)
        return self.db.exec(statement).all()

    def get_points_balance(self, student_id: int) -> int:
        return MilestoneRepository(self.db).get_points_balance(student_id)

    def get_approved_hours(self, student_id: int) -> float:
        return MilestoneRepository(self.db).get_approved_hours(student_id)

    def redeem_prize(self, student_id: int, prize_id: int) -> tuple[Redemption, int, str]:
        prize = self.db.get(Prize, prize_id)
        if prize is None:
            raise LookupError("Prize not found")
        balance = self.get_points_balance(student_id)
        if balance < prize.cost:
            raise ValueError("Not enough points for this prize")

        redemption = Redemption(student_id=student_id, prize_id=prize_id)
        self.db.add(redemption)
        self.db.commit()
        self.db.refresh(redemption)
        return redemption, balance - prize.cost, prize.name

    def update_redemption_status(
        self,
        redemption_id: int,
        admin_id: int,
        status: str,
    ) -> Redemption:
        redemption = self.db.get(Redemption, redemption_id)
        if redemption is None:
            raise LookupError("Redemption not found")
        if status not in {"pending", "processing", "shipping", "delivered"}:
            raise ValueError("Choose a valid redemption status")

        redemption.status = status
        redemption.confirmed_by = admin_id if status == "delivered" else None
        redemption.confirmed_at = datetime.utcnow() if status == "delivered" else None
        self.db.add(redemption)
        self.db.commit()
        self.db.refresh(redemption)
        return redemption