from pydantic import BaseModel, Field


class DownloadRequest(BaseModel):
    satellite: str = Field(max_length=2, description="Satellite abbreviation")

class CustomRequest(DownloadRequest):
    cycle_num: str = Field(pattern=r'^\d{3}$', description="Cycle number")
    pass_num: str = Field(pattern=r'^\d{4}$', description="Pass number")

class DateRequest(DownloadRequest):
    start_date: str = Field(description="Data start date based on which pass is located")
    end_date: str = Field(description="Data end date based on which pass is located")

