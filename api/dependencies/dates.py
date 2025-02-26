from datetime import datetime, time

from fastapi import HTTPException


async def validate_dates(start_date: datetime, end_date: datetime):
    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="Конечная дата должна быть позже начальной"
        )
    return start_date, end_date


async def validate_time(start_time: time, end_time: time):
    if start_time > end_time:
        raise HTTPException(status_code=400, detail="Время закрытие должно быть позже")
    return start_time, end_time
