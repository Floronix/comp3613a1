from fastapi import Request
from fastapi.responses import HTMLResponse
from app.dependencies.session import SessionDep
from app.dependencies.auth import AdminDep
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.volunteer_submission_service import VolunteerSubmissionService
from . import router, templates


@router.get("/admin", response_class=HTMLResponse)
async def admin_home_view(
    request: Request,
    user: AdminDep,
    db:SessionDep
):
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    return templates.TemplateResponse(
        request=request,
        name="activity.html",
        context={
            "user": user,
            "view": "admin",
            "pending_submissions": service.get_pending_submissions(),
            "my_submissions": [],
            "approved_hours": 0,
        }
    )
