from pydantic import BaseModel
from typing import Optional

class StateGraphInput(BaseModel):
    text: str
    image: Optional[str] = None
    # In a backend setting, instead of interactive input(),
    # the client can indicate if image editing is desired
    edit_image: Optional[bool] = False
    edit_description: Optional[str] = None
