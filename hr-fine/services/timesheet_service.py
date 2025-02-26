import datetime
from datetime import date, datetime, time, timedelta
from typing import Optional
from fastapi import HTTPException, Depends
from database.db import get_session
from sqlalchemy.orm import Session, joinedload

from schemas.timesheet_schemas import TimeStampBase
from models.timesheet_model import TimeStamp

from utils.jwt_bearer import JWTBearer, decode_jwt

def stamp_timesheet(stamp_data: TimeStampBase, emp_id: str, db: Session = Depends(get_session)):

    today = datetime.today().date()
    start_of_current_week = today - timedelta(days=today.weekday()) 
    allowed_date = start_of_current_week - timedelta(weeks=2)    

    overtime_start = time(18, 0)

    ### Check time older than 2 week 
    if stamp_data.stamp_date < allowed_date:
        raise HTTPException(
            status_code=400,
            detail=f"Timestamps older than {allowed_date.strftime('%Y-%m-%d')} are not allowed."
        )

    ### Check provent to can't stamp future day.
    if stamp_data.stamp_date > today:
        raise HTTPException(
            status_code=400,
            detail=f"Future timestamps beyond {today.strftime('%Y-%m-%d')} are not allowed."
        )
    
    if stamp_data.end_time <= stamp_data.start_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time."
        )

    if stamp_data.disbursement and (not stamp_data.stamp_details or stamp_data.stamp_details.strip() == ""):
        raise HTTPException(
            status_code=400,
            detail="Stamp details are required when disbursement is set to True."
        )
    
    if stamp_data.disbursement and not (stamp_data.OverTime or stamp_data.travel_expenses):
        raise HTTPException(
            status_code=400,
            detail="If disbursement is True, OverTime or travel_expenses must also be True."
        )

    if (stamp_data.OverTime or stamp_data.travel_expenses) and not (stamp_data.start_time >= overtime_start or stamp_data.end_time >= overtime_start):
        raise HTTPException(
            status_code=400,
            detail="If OverTime or travel_expenses is True, work must be scheduled after 18:00."
        )

    new_stamp = TimeStamp(
        emp_id=emp_id,
        project_id=stamp_data.project_id,
        stamp_date=stamp_data.stamp_date,
        start_time=stamp_data.start_time,
        end_time=stamp_data.end_time,
        stamp_details=stamp_data.stamp_details,
        disbursement=stamp_data.disbursement,
        OverTime=stamp_data.OverTime,
        travel_expenses=stamp_data.travel_expenses,
    )

    db.add(new_stamp)
    db.commit()
    db.refresh(new_stamp)
    
    return new_stamp

def delete_time_stamp(stamp_id: int, db: Session = Depends(get_session), auth: str = Depends(JWTBearer())):
    """Deletes a time stamp entry by `stamp_id`, but only if the logged-in user owns it."""

    time_stamp = db.query(TimeStamp).filter(TimeStamp.stamp_id == stamp_id).first()
    payload = decode_jwt(auth)
    emp_id = payload.get("emp_id")  

    if not emp_id:
        raise HTTPException(status_code=401, detail="Invalid token: Missing emp_id")
    
    if time_stamp.emp_id != emp_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to delete this timestamp."
        )

    if not time_stamp:
        raise HTTPException(
            status_code=404,
            detail=f"TimeStamp with ID {stamp_id} not found."
        )

    db.delete(time_stamp)
    db.commit()

    return {
            "message": f"TimeStamp with ID {stamp_id} deleted successfully"
        }

def edit_time_stamp(stamp_id: int, stamp_data: TimeStampBase, db: Session = Depends(get_session), auth: str = Depends(JWTBearer())):
    """Edits a timestamp entry by `stamp_id`, but only if the logged-in user owns it."""

    time_stamp = db.query(TimeStamp).filter(TimeStamp.stamp_id == stamp_id).first()
    if not time_stamp:
        raise HTTPException(status_code=404, detail=f"TimeStamp with ID {stamp_id} not found.")

    emp_id = decode_jwt(auth).get("emp_id")
    if not emp_id:
        raise HTTPException(status_code=401, detail="Invalid token: Missing emp_id")

    if time_stamp.emp_id != emp_id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this timestamp.")

    today = datetime.today().date()
    allowed_date = today - timedelta(weeks=2)
    overtime_start = time(18, 0)

    if not (allowed_date <= stamp_data.stamp_date <= today):
        raise HTTPException(status_code=400, detail="Timestamps can only be edited within the last 2 weeks.")

    if stamp_data.end_time <= stamp_data.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time.")

    if stamp_data.disbursement and not stamp_data.stamp_details:
        raise HTTPException(status_code=400, detail="Stamp details are required when disbursement is set to True.")

    if stamp_data.disbursement and not (stamp_data.OverTime or stamp_data.travel_expenses):
        raise HTTPException(status_code=400, detail="If disbursement is True, OverTime or travel_expenses must be True.")

    if (stamp_data.OverTime or stamp_data.travel_expenses) and not (stamp_data.start_time >= overtime_start or stamp_data.end_time >= overtime_start):
        raise HTTPException(status_code=400, detail="OverTime or travel expenses must be scheduled after 18:00.")

    update_fields = {key: value for key, value in stamp_data.model_dump().items() if value is not None}
    for key, value in update_fields.items():
        setattr(time_stamp, key, value)

    db.commit()
    db.refresh(time_stamp)

    return {"message": f"TimeStamp with ID {stamp_id} updated successfully", "updated_timestamp": update_fields}

def fetch_time_stamps(
    db: Session = Depends(get_session),
    auth: str = Depends(JWTBearer()),
    target_date: Optional[date] = None,
    week_offset: Optional[int] = 0
):
    """Fetches all timestamps for a specific week (defaults to current week)."""

    emp_id = decode_jwt(auth).get("emp_id")
    if not emp_id:
        raise HTTPException(status_code=401, detail="Invalid token: Missing emp_id")

    if not target_date:
        target_date = datetime.today().date()

    target_date = target_date + timedelta(weeks=week_offset)

    start_of_week = target_date - timedelta(days=target_date.weekday()) 
    end_of_week = start_of_week + timedelta(days=6)  

    time_stamps = (
        db.query(TimeStamp)
        .filter(
            TimeStamp.emp_id == emp_id,
            TimeStamp.stamp_date >= start_of_week,
            TimeStamp.stamp_date <= end_of_week
        )
        .order_by(TimeStamp.stamp_date, TimeStamp.start_time)
        .all()
    )

    return {
        "week_range": {
            "start_date": start_of_week.strftime('%Y-%m-%d'),
            "end_date": end_of_week.strftime('%Y-%m-%d')
        },
        "time_stamps": [
            {
                "stamp_id": ts.stamp_id,
                "emp_id": ts.emp_id,
                "project_id": ts.project_id,
                "stamp_date": ts.stamp_date.strftime('%Y-%m-%d'),
                "start_time": ts.start_time.strftime('%H:%M'),
                "end_time": ts.end_time.strftime('%H:%M'),
                "stamp_details": ts.stamp_details,
                "disbursement": ts.disbursement,
                "OverTime": ts.OverTime,
                "travel_expenses": ts.travel_expenses
            }
            for ts in time_stamps
        ]
    }