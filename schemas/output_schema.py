from pydantic import BaseModel
from typing import Optional

class StateGraphOutput(BaseModel):
    text: str
    image: Optional[str] = None
    session_id: Optional[str] = None
