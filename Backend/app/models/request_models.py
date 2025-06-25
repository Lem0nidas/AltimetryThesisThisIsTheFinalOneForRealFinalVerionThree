from pydantic import BaseModel, Field, field_validator, model_validator
from typing_extensions import Self
from datetime import datetime, timezone


class DownloadRequest(BaseModel):
    satellite: str = Field(max_length=2, description="Satellite abbreviation")
    
    @field_validator('satellite', mode='after')
    @classmethod
    def known_sat(cls, value: str) -> str:
        known_satellites = {"gs", "e1", "tx", "pn", "e2", "g1", "j1", "n1", "j2", "c2", "sa", "j3", "3a", "3b", "6a", "sw"}
        
        if value not in known_satellites:
            raise ValueError(f"Uknown satellite: {value}")
        
        return value

class CustomRequest(DownloadRequest):
    cycle_num: str = Field(description="Cycle number")
    pass_num: str = Field(description="Pass number")

    @field_validator('cycle_num', mode='after')
    @classmethod
    def validate_cycle(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Cycle number must be numeric!")
        
        return value.zfill(3)
    
    @field_validator('pass_num', mode='after')
    @classmethod
    def validate_pass(cls, value: str) -> str:
        if value == "":
            return ''
        
        if not value.isdigit():
            raise ValueError("Pass number must be numeric!")
        
        return value.zfill(4)

class DateRequest(DownloadRequest):
    start_date: str = Field(description="Data start date based on which pass is located")
    end_date: str = Field(description="Data end date based on which pass is located")

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        start = datetime.strptime(self.start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end = datetime.strptime(self.end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        if (end < start):
            raise ValueError("End date must be after Start date!")
        
        return self

