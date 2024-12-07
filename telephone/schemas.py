from pydantic import BaseModel,Field
from typing import List

class VirtualPhoneNumberDetail(BaseModel):
    phone_number:str = Field(..., min_length=10, max_length=15, description="Phone number must be between 10 and 15 characters long")


class VirtualPhoneNumberDetailResponse(BaseModel):
    count:int
    data: List[VirtualPhoneNumberDetail]