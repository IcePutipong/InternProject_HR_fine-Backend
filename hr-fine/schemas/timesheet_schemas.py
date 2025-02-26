from pydantic import BaseModel, field_validator
from datetime import datetime, date, time
from typing import Optional

class TimeStampBase(BaseModel):
    project_id: int
    stamp_date: date
    start_time: time
    end_time: time
    stamp_details: Optional[str]
    disbursement: bool = False
    OverTime: bool = False
    travel_expenses: bool = False

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def validate_time(cls, v):
        if isinstance(v, str):  
            try:
                return datetime.strptime(v, "%H:%M").time()  
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM (e.g., 09:30)")
        return v  
