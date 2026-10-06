from fastapi import Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.dependencies import AdminDep, AuthDep, SessionDep
from app.repositories.volunteer_submission import VolunteerSubmissionRepository
from app.services.volunteer_submission_service import VolunteerSubmissionService
from . import router, templates


@router.post("/api/volunteer-submissions")
async def create_volunteer_submission(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    activity: str = Form(...),
    hours: int = Form(...),
    description: str = Form(...),
):
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    if user.id is None or user.role == "admin":
        raise HTTPException(status_code=403, detail="Student access is required")
    try:
        submission = service.create_submission(
            student_id=user.id,
            activity=activity,
            hours=hours,
            description=description,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return {"ok": True, "id": submission.id}


@router.get("/my-activities", response_class=HTMLResponse)
async def my_activities_view(request: Request, user: AuthDep, db: SessionDep):
    if user.id is None or user.role == "admin":
        raise HTTPException(status_code=403, detail="Student access is required")
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    return templates.TemplateResponse(
        request=request,
        name="activity.html",
        context={
            "user": user,
            "view": "activities",
            "my_submissions": service.get_student_submissions(user.id),
            "pending_submissions": [],
            "approved_hours": service.get_approved_hours(user.id),
        },
    )


@router.post("/api/volunteer-submissions/{submission_id}/review")
async def review_volunteer_submission(
    submission_id: int,
    admin: AdminDep,
    db: SessionDep,
    decision: str = Form(...),
):
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    try:
        submission = service.review_submission(submission_id, admin, decision)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {"ok": True, "status": submission.status}


@router.post("/api/volunteer-submissions/{submission_id}/undo")
async def undo_volunteer_submission(
    submission_id: int,
    user: AuthDep,
    db: SessionDep,
):
    service = VolunteerSubmissionService(VolunteerSubmissionRepository(db))
    try:
        submission = service.undo(submission_id, user)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {"ok": True, "status": submission.status}