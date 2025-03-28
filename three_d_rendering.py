from typing import List, Sequence
from dotenv import load_dotenv
import base64
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, refinement_chain
from imagen import image_generator, image_editor
from meshy_service import run_agent

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
            # Pass the accumulated dictionary and expect an updated dictionary
            input_data, next_state = func(input_data)
            self.current_state = next_state
        return input_data

# Each state function now updates the existing dictionary instead of replacing it
def generation_state(input_data):
    prompt_input = input_data.get("text")
    if not prompt_input:
        raise ValueError("Text input is required for generation.")
    design_prompt = generation_chain.invoke({"user_input": prompt_input})
    input_data["text"] = design_prompt.content
    return input_data, "refinement"

def refinement_state(input_data):
    refined_prompt = refinement_chain.invoke({"user_input": input_data.get("text")})
    input_data["text"] = refined_prompt.content
    return input_data, "image_generation"

def image_generation_state(input_data):
    # Generate an image based on the refined text prompt
    img = image_generator(input_data.get("text"))
    input_data["image"] = img
    return input_data, "image_editing"

def image_editing_state(input_data):
    user_choice = input("Do you want to edit the image? (yes/no): ")
    if user_choice.lower() == 'yes':
        edits = input("Describe the edits you want: ")
        image = input_data.get("image")
        edited_img = image_editor(image, edits)
        print("Edited image:", edited_img)
        input_data["image"] = edited_img
    return input_data, "three_d_rendering"

def three_d_rendering_state(input_data):
    image_path = input_data.get("image")
    with open(image_path, 'rb') as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
    encoded_string = encoded_bytes.decode('utf-8')

    data_url = f"data:image/png;base64,{encoded_string}"

    result = run_agent(data_url, "msy_Rocf0nAb6n8Skh4YLZ7m5IFmNsigRhiVslxB")
    return input_data, None 

# Main execution: setting up the state graph and running the agent
if __name__ == "__main__":
    user_text = input("Enter your description for the 3D scene/object: ")
    user_image = input("Enter the path to an image file (or leave blank if none): ")
    
    # Package both text and image (if provided) into a dictionary
    user_input = {
        "text": user_text,
        "image": user_image if user_image.strip() != "" else None
    }
    
    # Create and configure the state graph
    sg = StateGraph()
    sg.add_node("generation", generation_state)
    sg.add_node("refinement", refinement_state)
    sg.add_node("image_generation", image_generation_state)
    sg.add_node("image_editing", image_editing_state)
    sg.add_node("three_d_rendering", three_d_rendering_state)
    sg.set_state("generation")
    
    # Run the state machine only once to accumulate all outputs
    final_output = sg.run(user_input)
    print("Final Output:", final_output)
