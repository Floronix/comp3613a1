from fastapi import Request
from fastapi.responses import HTMLResponse
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.volunteer_submission_service import VolunteerSubmissionService
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    return templates.TemplateResponse(
        request=request,
        name="activity.html",
        context={
            "user": user,
            "view": "submit",
            "my_submissions": [],
            "pending_submissions": service.get_pending_submissions() if user.role == "admin" else [],
            "approved_hours": service.get_approved_hours(user.id) if user.role != "admin" and user.id is not None else 0,
        }
    )