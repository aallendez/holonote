from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError

from src.models.holos import Holo, HoloCreate, HoloUpdate, HoloDaily, HoloDailyCreate
from src.db.holos import (
    get_holo_config,
    update_holo_config,
    create_holo_config,
    get_holo_daily_by_date,
    get_latest_holo_daily,
    create_holo_daily,
    get_avg_score,
)
from src.db.session import get_db
from src.api.routes.auth import get_current_user

router = APIRouter(prefix="/holos", tags=["holos"])


@router.get("/holo", response_model=Holo)
def get_holo_config_route(
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    """Get the holo questions config for a user"""
    try:
        result = get_holo_config(user["uid"], db)
        if result is None:
            raise HTTPException(status_code=404, detail="Holo configuration not found")
        return result
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error while fetching holo config: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while fetching holo config: {str(e)}",
        )


@router.put("/holo", response_model=Holo)
def update_holo_config_route(
    holo: HoloUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    """Update the holo questions config for the current user"""
    try:
        result = update_holo_config(user["uid"], holo, db)
        if result is None:
            raise HTTPException(status_code=404, detail="Holo configuration not found")
        return result
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error while updating holo config: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while updating holo config: {str(e)}",
        )


@router.post("/holo", response_model=Holo)
def create_holo_config_route(
    holo: HoloCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    """Create a new holo questions config for a user - TODO triggered on signup"""
    try:
        return create_holo_config(user["uid"], holo, db)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Data integrity error: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error while creating holo config: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while creating holo config: {str(e)}",
        )


@router.get(
    "/daily",
    response_model=HoloDaily,
    description="Get the holo daily by date for a user",
)
def get_holo_daily_route(
    entry_date: date, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    """Get the holo daily for a user"""
    try:
        holo = get_holo_config(user["uid"], db)
        if not holo:
            raise HTTPException(404, "No holo config found")
        result = get_holo_daily_by_date(holo.holo_id, entry_date, db)
        if not result:
            raise HTTPException(404, "Holo daily not found")
        return result
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Data integrity error: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error while fetching holo daily: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while fetching holo daily: {str(e)}",
        )


@router.get("/daily/latest", response_model=HoloDaily)
def get_latest_holo_daily_route(
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    """Get the latest holo daily for a user"""
    try:
        holo = get_holo_config(user["uid"], db)
        if not holo:
            raise HTTPException(404, "No holo config found")
        latest_holo = get_latest_holo_daily(holo.holo_id, db)
        if not latest_holo:
            raise HTTPException(404, "No holo daily found")
        return latest_holo
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Data integrity error: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error while fetching latest holo daily: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while fetching latest holo daily: {str(e)}",
        )


@router.post("/daily", response_model=HoloDaily)
def create_holo_daily_route(
    holo_daily: HoloDailyCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Create a new holo daily for a user"""
    try:
        holo = get_holo_config(user["uid"], db)
        if not holo:
            raise HTTPException(404, "No holo config found")
        return create_holo_daily(holo.holo_id, holo_daily, db)
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Data integrity error: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error while creating holo daily: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while creating holo daily: {str(e)}",
        )


@router.get("/avg-score")
def get_avg_score_route(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Get the average score from all holo dailies for a user"""
    try:
        holo = get_holo_config(user["uid"], db)
        if not holo:
            raise HTTPException(404, "No holo config found")

        avg_score = get_avg_score(holo.holo_id, db)
        return {"avg_score": avg_score}
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error while fetching average score: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while fetching average score: {str(e)}",
        )
