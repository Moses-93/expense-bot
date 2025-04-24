from pydantic import BaseModel
from typing import Optional
from datetime import date as Date


class ExpenseDTO(BaseModel):
    title: str
    date: Date
    amount: float


class UpdateExpenseDTO(BaseModel):
    title: Optional[str] = None
    date: Optional[Date] = None
    amount: Optional[float] = None


class ExpenseReportRequestDTO(BaseModel):
    start_date: Date
    end_date: Date


class ExpenseReportFile(BaseModel):
    filename: str
    content: bytes
