from fastapi import Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.dependencies import AdminDep, AuthDep, SessionDep
from app.repositories.prize import PrizeRepository
from app.services.prize_service import PrizeService
from . import router, templates


@router.get("/prizes", response_class=HTMLResponse)
async def prizes_view(request: Request, user: AuthDep, db: SessionDep):
    service = PrizeService(PrizeRepository(db))
    if user.id is None:
        raise HTTPException(status_code=401, detail="Sign in required")
    data = service.get_prize_page_data(user.id, user.role == "admin")
    return templates.TemplateResponse(
        request=request,
        name="prizes.html",
        context={"user": user, **data},
    )


@router.post("/api/prizes/{prize_id}/redeem")
async def redeem_prize(prize_id: int, user: AuthDep, db: SessionDep):
    service = PrizeService(PrizeRepository(db))
    if user.id is None or user.role == "admin":
        raise HTTPException(status_code=403, detail="Student access is required")
    try:
        redemption, points_balance, prize_name = service.redeem_prize(user.id, prize_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {
        "ok": True,
        "id": redemption.id,
        "status": redemption.status,
        "points_balance": points_balance,
        "prize_name": prize_name,
    }


@router.post("/api/redemptions/{redemption_id}/status")
async def update_redemption_status(
    redemption_id: int,
    admin: AdminDep,
    db: SessionDep,
    status: str = Form(...),
):
    if admin.id is None:
        raise HTTPException(status_code=401, detail="Sign in required")
    service = PrizeService(PrizeRepository(db))
    try:
        redemption = service.update_redemption_status(redemption_id, admin.id, status)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {"ok": True, "status": redemption.status}