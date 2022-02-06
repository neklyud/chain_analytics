from fastapi import APIRouter
from datetime import date
from loguru import logger


api_router = APIRouter()


@api_router.get('/history/')
async def load_history(date_from: date, date_to: date):
    logger.info("from {} to {}".format(date_from, date_to))
    return {"id": 1}
