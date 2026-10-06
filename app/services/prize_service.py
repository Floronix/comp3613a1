from app.repositories.prize import PrizeRepository


class PrizeService:
    def __init__(self, repository: PrizeRepository):
        self.repository = repository

    def get_prize_page_data(self, student_id: int, is_admin: bool = False):
        return {
            "prizes": self.repository.get_prizes(),
            "redemption_history": self.repository.get_redemption_history(
                None if is_admin else student_id
            ),
            "points_balance": 0 if is_admin else self.repository.get_points_balance(student_id),
            "approved_hours": 0 if is_admin else self.repository.get_approved_hours(student_id),
        }

    def redeem_prize(self, student_id: int, prize_id: int):
        return self.repository.redeem_prize(student_id, prize_id)

    def update_redemption_status(
        self,
        redemption_id: int,
        admin_id: int,
        status: str,
    ):
        if status not in {"pending", "processing", "shipping", "delivered"}:
            raise ValueError("Choose a valid redemption status")
        return self.repository.update_redemption_status(redemption_id, admin_id, status)