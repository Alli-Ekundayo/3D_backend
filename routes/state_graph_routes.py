from fastapi import APIRouter
from schemas.input_schema import StateGraphInput
from schemas.output_schema import StateGraphOutput
from utils.state_graph import run_state_graph

router = APIRouter()

@router.post("/process", response_model=StateGraphOutput)
def process_state_graph(data: StateGraphInput):
    # Convert the Pydantic model to a dict
    input_data = data.dict()
    # Run the state machine until the image is generated and paused for feedback
    result = run_state_graph(input_data)
    # Return the current output with the session_id for feedback
    return result
