from pydantic import BaseModel

class FeedbackSchema(BaseModel):
    session_id: str
    edit_description: str
