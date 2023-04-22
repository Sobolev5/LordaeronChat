from dateutil.parser import parse as dateutil_parse
from datetime import date
from pydantic import BaseModel, validator
from typing import Optional


class Health(BaseModel):
    check: int

