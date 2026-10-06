from app.repositories.milestone import MilestoneRepository


class LeaderboardService:
    def __init__(self, repository: MilestoneRepository):
        self.repository = repository

    def get_leaderboard_data(self, student_id: int):
        return self.repository.get_leaderboard_data(student_id)

    def unlock_reached_milestones(self, student_id: int):
        return self.repository.unlock_reached_milestones(student_id)