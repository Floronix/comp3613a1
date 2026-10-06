from sqlalchemy import func
from sqlmodel import Session, select

from app.models.milestone import Milestone, StudentMilestone
from app.models.prize import Prize, Redemption
from app.models.user import User
from app.models.volunteer_submission import VolunteerSubmission

MILESTONE_THRESHOLDS = (1, 5, 10, *range(20, 101, 10))


class MilestoneRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_leaderboard_data(self, student_id: int):
        milestones = self.ensure_milestones()
        ranked_students = self.get_ranked_students()
        current_student = next(
            (student for student in ranked_students if student["id"] == student_id),
            None,
        )
        if current_student is None:
            raise LookupError("Student not found")

        unlocked_records = self.db.exec(
            select(StudentMilestone).where(StudentMilestone.student_id == student_id)
        ).all()
        unlocked_by_id = {record.milestone_id: record for record in unlocked_records}
        pending_awards = []
        for record in unlocked_records:
            if record.notification_pending:
                milestone = self.db.get(Milestone, record.milestone_id)
                if milestone is not None:
                    pending_awards.append(
                        {"threshold": milestone.threshold, "points": record.points_awarded}
                    )
                record.notification_pending = False
                self.db.add(record)
        if pending_awards:
            self.db.commit()

        approved_hours = current_student["approved_hours"]
        next_milestone = next(
            (milestone for milestone in milestones if milestone.threshold > approved_hours),
            None,
        )
        if next_milestone is None:
            milestone_start_index = max(0, len(milestones) - 3)
        elif len(unlocked_records) < 2:
            milestone_start_index = 0
        else:
            milestone_start_index = max(0, milestones.index(next_milestone) - 2)
        progress_target = next_milestone.threshold if next_milestone else 100
        progress_percent = min(100, int(approved_hours * 100 / progress_target)) if progress_target else 100
        earned_milestone_points = sum(record.points_awarded for record in unlocked_records)
        top_students = ranked_students[:7]
        student_in_top = any(student["id"] == student_id for student in top_students)

        return {
            "top_students": top_students,
            "current_student": current_student if not student_in_top else None,
            "milestones": [
                {
                    "id": milestone.id,
                    "name": milestone.name,
                    "threshold": milestone.threshold,
                    "badge_icon": milestone.badge_icon,
                    "reward": milestone.reward,
                    "unlocked": milestone.id in unlocked_by_id,
                }
                for milestone in milestones
            ],
            "approved_hours": approved_hours,
            "points_balance": self.get_points_balance(student_id),
            "next_milestone": next_milestone.threshold if next_milestone else None,
            "milestone_start_index": milestone_start_index,
            "progress_percent": progress_percent,
            "new_awards": pending_awards,
        }

    def ensure_milestones(self) -> list[Milestone]:
        milestones = self.db.exec(select(Milestone).order_by(Milestone.threshold)).all()
        existing_thresholds = {milestone.threshold for milestone in milestones}
        for threshold in MILESTONE_THRESHOLDS:
            if threshold not in existing_thresholds:
                milestone = Milestone(
                    name=f"{threshold} Hour" if threshold == 1 else f"{threshold} Hours",
                    threshold=threshold,
                    badge_icon="deployed_code",
                    reward=threshold * 10,
                )
                self.db.add(milestone)
                milestones.append(milestone)
        self.db.commit()
        return sorted(milestones, key=lambda milestone: milestone.threshold)

    def get_approved_hours(self, student_id: int) -> float:
        statement = select(func.coalesce(func.sum(VolunteerSubmission.hours), 0)).where(
            VolunteerSubmission.student_id == student_id,
            VolunteerSubmission.status == "approved",
        )
        return float(self.db.exec(statement).one())

    def get_points_balance(self, student_id: int) -> int:
        approved_points = int(self.get_approved_hours(student_id) * 10)
        milestone_points = sum(
            self.db.exec(
                select(StudentMilestone.points_awarded).where(
                    StudentMilestone.student_id == student_id
                )
            ).all()
        )
        spent_statement = (
            select(func.coalesce(func.sum(Prize.cost), 0))
            .join(Redemption, Redemption.prize_id == Prize.id)
            .where(Redemption.student_id == student_id)
        )
        spent_points = int(self.db.exec(spent_statement).one())
        return max(0, approved_points + milestone_points - spent_points)

    def get_ranked_students(self) -> list[dict[str, int | str | float]]:
        users = self.db.exec(select(User).where(User.role != "admin")).all()
        statement = (
            select(
                VolunteerSubmission.student_id,
                func.coalesce(func.sum(VolunteerSubmission.hours), 0),
            )
            .where(VolunteerSubmission.status == "approved")
            .group_by(VolunteerSubmission.student_id)
        )
        hours_by_student = {
            student_id: float(hours)
            for student_id, hours in self.db.exec(statement).all()
        }
        ranked = [
            {
                "id": user.id,
                "username": user.username,
                "approved_hours": hours_by_student.get(user.id, 0.0),
            }
            for user in users
        ]
        ranked.sort(key=lambda student: (-student["approved_hours"], student["username"].casefold()))
        for rank, student in enumerate(ranked, start=1):
            student["rank"] = rank
        return ranked

    def unlock_reached_milestones(self, student_id: int) -> list[StudentMilestone]:
        milestones = self.ensure_milestones()
        approved_hours = self.get_approved_hours(student_id)
        unlocked_ids = set(
            self.db.exec(
                select(StudentMilestone.milestone_id).where(
                    StudentMilestone.student_id == student_id
                )
            ).all()
        )
        new_unlocks = []
        for milestone in milestones:
            if milestone.threshold <= approved_hours and milestone.id not in unlocked_ids:
                unlock = StudentMilestone(
                    student_id=student_id,
                    milestone_id=milestone.id,
                    points_awarded=milestone.reward,
                )
                self.db.add(unlock)
                new_unlocks.append(unlock)
        if new_unlocks:
            self.db.commit()
            for unlock in new_unlocks:
                self.db.refresh(unlock)
        return new_unlocks