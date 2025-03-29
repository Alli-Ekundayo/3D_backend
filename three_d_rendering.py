from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, refinement_chain
from    import image_generator, image_editor

class StateGraph:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_node(self, name, func):
        self.states[name] = func

    def set_state(self, name):
        self.current_state = name

    def run(self, input_data):
        while self.current_state is not None:
            func = self.states[self.current_state]
            output, next_state = func(input_data)
            input_data = output
            self.current_state = next_state
        return input_data

# State functions now accept a dictionary with potential keys "text" and "image"
def generation_state(input_data):
    prompt_input = input_data.get("text")
    if not prompt_input:
        raise ValueError("Text input is required for generation.")
    design_prompt = generation_chain.invoke(user_input=prompt_input)
    return design_prompt

def refinement_state(input_data):
    refined_prompt = refinement_chain.run(user_input=input_data.get("text"))
    return refined_prompt

def image_generation_state(input_data):
    img = image_generator(input_data.get("text"))
    return img

def image_editing_state(input_data):
    user_choice = input("Do you want to edit the image? (yes/no): ")
    if user_choice.lower() == 'yes':
        edits = input("Describe the edits you want: ")
        image = input_data.get("image")
        edited_img = image_editor(image, edits)
        print("Edited image:", edited_img)
        return edited_img
    else:
        return input_data

def three_d_rendering_state(input_data):
    rendering = input_data
    return rendering

# Main execution: setting up the state graph and running the agent
if __name__ == "__main__":
    user_text = input("Enter your description for the 3D scene/object: ")
    user_image = input("Enter the path to an image file (or leave blank if none): ")
    
    # Package both text and image (if provided) into a dictionary
    user_input = {"text": user_text, "image": user_image if user_image.strip() != "" else None}
    
    # Create and configure the state graph
    sg = StateGraph()
    sg.add_node("generation", generation_state)
    sg.add_node("refinement", refinement_state)
    sg.add_node("image_generation", image_generation_state)
    sg.add_node("image_editing", image_editing_state)
    sg.add_node("three_d_rendering", three_d_rendering_state)
    sg.set_state("generation")



    app = sg.run()

    print(app.get_graph().draw_mermaid())
    app.get_graph().print_ascii()


    
    final_output = sg.run(user_input)
    print("Final Output:", final_output)