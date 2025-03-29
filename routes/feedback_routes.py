from fastapi import APIRouter, HTTPException
from schemas.feedback_schema import FeedbackSchema
from schemas.output_schema import StateGraphOutput
from utils.state_graph import image_editing_state, three_d_rendering_state
from utils.session_store import state_store

router = APIRouter()

@router.post("/feedback", response_model=StateGraphOutput)
def process_feedback(feedback: FeedbackSchema):
    session_id = feedback.session_id
    if session_id not in state_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Retrieve the stored state machine data
    input_data = state_store.pop(session_id)
    # Update the input with the provided edit description
    input_data["edit_description"] = feedback.edit_description
    
    # Resume the state machine from the image editing state
    updated_data, next_state = image_editing_state(input_data)
    # If additional processing is needed, continue with 3D rendering
    if next_state == "three_d_rendering":
        updated_data, _ = three_d_rendering_state(updated_data)
    
    return updated_data
