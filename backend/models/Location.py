from pydantic import BaseModel, Field
from typing import Optional, List


class Location(BaseModel):
    """位置信息(经纬度坐标)"""
    longitude: float = Field(..., description="经度", ge=-180, le=180)
    latitude: float = Field(..., description="纬度", ge=-90, le=90)


