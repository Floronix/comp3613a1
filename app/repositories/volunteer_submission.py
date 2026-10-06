from datetime import datetime

from sqlmodel import Session, case, func, select

from app.models.user import User
from app.models.volunteer_submission import VolunteerSubmission


class VolunteerSubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_submission(
        self,
        student_id: int,
        activity: str,
        hours: int,
        description: str,
    ) -> VolunteerSubmission:
        submission = VolunteerSubmission(
            student_id=student_id,
            activity=activity,
            hours=hours,
            description=description,
        )
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def get_pending_submissions(self) -> list[tuple[VolunteerSubmission, User]]:
        statement = (
            select(VolunteerSubmission, User)
            .join(User, User.id == VolunteerSubmission.student_id)
            .where(VolunteerSubmission.status == "pending")
            .order_by(VolunteerSubmission.submitted_at.asc())
        )
        return self.db.exec(statement).all()

    def get_student_submissions(self, student_id: int) -> list[VolunteerSubmission]:
        statement = (
            select(VolunteerSubmission)
            .where(VolunteerSubmission.student_id == student_id)
            .order_by(
                case((VolunteerSubmission.status == "pending", 0), else_=1),
                VolunteerSubmission.submitted_at.desc(),
            )
        )
        return self.db.exec(statement).all()

    def get_approved_hours(self, student_id: int) -> float:
        statement = select(func.coalesce(func.sum(VolunteerSubmission.hours), 0)).where(
            VolunteerSubmission.student_id == student_id,
            VolunteerSubmission.status == "approved",
        )
        return float(self.db.exec(statement).one())

    def review_submission(
        self,
        submission_id: int,
        admin_id: int,
        decision: str,
    ) -> VolunteerSubmission:
        submission = self.db.get(VolunteerSubmission, submission_id)
        if submission is None:
            raise LookupError("Submission not found")
        if submission.status != "pending":
            raise ValueError("Only pending submissions can be reviewed")

        submission.status = "approved" if decision == "approved" else "removed"
        submission.reviewed_by = admin_id
        submission.reviewed_at = datetime.utcnow()
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def cancel_pending_submission(self, submission_id: int, student_id: int) -> VolunteerSubmission:
        submission = self.db.get(VolunteerSubmission, submission_id)
        if submission is None or submission.student_id != student_id:
            raise LookupError("Submission not found")
        if submission.status != "pending":
            raise ValueError("Only pending submissions can be removed")

        submission.status = "removed"
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def undo_review(self, submission_id: int, admin_id: int) -> VolunteerSubmission:
        submission = self.db.get(VolunteerSubmission, submission_id)
        if submission is None:
            raise LookupError("Submission not found")
        if submission.status not in {"approved", "removed"}:
            raise ValueError("This submission has no review to undo")
        if submission.reviewed_by != admin_id:
            raise PermissionError("Only the reviewing admin can undo this review")

        submission.status = "pending"
        submission.reviewed_by = None
        submission.reviewed_at = None
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission