from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse

from app.dependencies import AuthDep, SessionDep
from app.repositories.milestone import MilestoneRepository
from app.services.leaderboard_service import LeaderboardService
from . import router, templates


@router.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard_view(request: Request, user: AuthDep, db: SessionDep):
    if user.id is None or user.role == "admin":
        raise HTTPException(status_code=403, detail="Student access is required")
    service = LeaderboardService(MilestoneRepository(db))
    data = service.get_leaderboard_data(user.id)
    return templates.TemplateResponse(
        request=request,
        name="leaderboard.html",
        context={"user": user, **data},
    )