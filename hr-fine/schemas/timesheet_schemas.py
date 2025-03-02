from pydantic import BaseModel, field_validator
from datetime import datetime, date, time
from typing import List, Optional

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

class CalculateTotalTime(BaseModel):
    start_time: time
    end_time: time

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def validate_time(cls, v):
        if isinstance(v, str):  
            try:
                return datetime.strptime(v, "%H:%M").time()  
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM (e.g., 09:30)")
        return v 
    
class FetchTimeSheet(BaseModel):     
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

class TimeStampSchema(BaseModel):
    stamp_id: int
    emp_id: str
    project_id: Optional[int]
    project_code: str
    project_name: str
    period_number: Optional[int]
    stamp_date: date
    start_time: time
    end_time: time
    total_time: time
    stamp_details: Optional[str]
    disbursement: bool
    OverTime: bool
    travel_expenses: bool
    
    class Config:
        orm_mode = True 

class WeekRangeSchema(BaseModel):
    start_date: str
    end_date: str

class TimeStampResponseSchema(BaseModel):
    week_range: WeekRangeSchema
    time_stamps: List[TimeStampSchema]
