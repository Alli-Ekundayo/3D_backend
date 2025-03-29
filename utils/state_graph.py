import base64
from services import generation, refinement, image_service, meshy_service
from utils.session_store import state_store, generate_session_id

class StateGraph:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_node(self, name, func):
        self.states[name] = func

    def set_state(self, name):
        self.current_state = name

    def run(self, input_data):
        # Run state machine until current_state is None
        while self.current_state is not None:
            func = self.states[self.current_state]
            input_data, next_state = func(input_data)
            self.current_state = next_state
        return input_data

# State functions

def generation_state(input_data):
    prompt_input = input_data.get("text")
    if not prompt_input:
        raise ValueError("Text input is required for generation.")
    design_prompt = generation.generation_chain_invoke({"user_input": prompt_input})
    input_data["text"] = design_prompt.content
    return input_data, "refinement"

def refinement_state(input_data):
    refined_prompt = refinement.refinement_chain_invoke({"user_input": input_data.get("text")})
    input_data["text"] = refined_prompt.content
    return input_data, "image_generation"

def image_generation_state(input_data):
    # Generate an image based on the refined text prompt
    img = image_service.image_generator(input_data.get("text"))
    input_data["image"] = img
    # Instead of calling image_editing_state directly, we now pause
    # and return the generated image and a session id to the client.
    session_id = generate_session_id()
    state_store[session_id] = input_data
    # We return a special marker state "awaiting_feedback"
    input_data["session_id"] = session_id
    return input_data, None

def image_editing_state(input_data):
    # Expect human feedback to be provided via the feedback endpoint.
    # When resuming, the edit_description field should be populated.
    edit_desc = input_data.get("edit_description")
    if not edit_desc:
        # Ideally, this branch should not be reached when resuming
        return input_data, None

    image = input_data.get("image")
    edited_img = image_service.image_editor(image, edit_desc)
    input_data["image"] = edited_img
    return input_data, "three_d_rendering"

def three_d_rendering_state(input_data):
    image_path = input_data.get("image")
    if image_path:
        with open(image_path, 'rb') as image_file:
            encoded_bytes = base64.b64encode(image_file.read())
        encoded_string = encoded_bytes.decode('utf-8')
        data_url = f"data:image/png;base64,{encoded_string}"
        # Pass the data URL to the meshy service with an API key.
        _ = meshy_service.run_agent(data_url, "msy_Rocf0nAb6n8Skh4YLZ7m5IFmNsigRhiVslxB")
    return input_data, None

def run_state_graph(data: dict):
    sg = StateGraph()
    sg.add_node("generation", generation_state)
    sg.add_node("refinement", refinement_state)
    sg.add_node("image_generation", image_generation_state)
    sg.add_node("image_editing", image_editing_state)
    sg.add_node("three_d_rendering", three_d_rendering_state)
    sg.set_state("generation")
    return sg.run(data)
