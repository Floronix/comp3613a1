from app.models.user import User
from app.repositories.milestone import MilestoneRepository
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.leaderboard_service import LeaderboardService


class VolunteerSubmissionService:
    def __init__(self, repository: VolunteerSubmissionRepository):
        self.repository = repository
        self.leaderboard_service = LeaderboardService(MilestoneRepository(repository.db))

    def create_submission(
        self,
        student_id: int,
        activity: str,
        hours: int,
        description: str,
    ):
        activity = activity.strip()
        description = description.strip()
        if not activity or not description:
            raise ValueError("Activity and description are required")
        if hours <= 0:
            raise ValueError("Hours must be a positive whole number")
        return self.repository.create_submission(
            student_id,
            activity,
            hours,
            description,
        )

    def get_pending_submissions(self):
        return self.repository.get_pending_submissions()

    def get_student_submissions(self, student_id: int):
        return self.repository.get_student_submissions(student_id)

    def get_approved_hours(self, student_id: int) -> float:
        return self.repository.get_approved_hours(student_id)

    def review_submission(self, submission_id: int, admin: User, decision: str):
        if admin.role != "admin" or admin.id is None:
            raise PermissionError("Admin access is required")
        if decision not in {"approved", "rejected"}:
            raise ValueError("Choose approve or reject")
        submission = self.repository.review_submission(submission_id, admin.id, decision)
        if submission.status == "approved":
            self.leaderboard_service.unlock_reached_milestones(submission.student_id)
        return submission

    def undo(self, submission_id: int, user: User):
        if user.id is None:
            raise PermissionError("A signed-in account is required")
        if user.role == "admin":
            return self.repository.undo_review(submission_id, user.id)
        return self.repository.cancel_pending_submission(submission_id, user.id)