import uuid

# A simple in‑memory store for state machine sessions
state_store = {}

def generate_session_id() -> str:
    return str(uuid.uuid4())
