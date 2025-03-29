import requests
import time
import json
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display, HTML
from typing import Any, List, Dict
import requests
import time
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display, HTML
from typing import Any, List, Dict

API_KEY = "msy_Rocf0nAb6n8Skh4YLZ7m5IFmNsigRhiVslxB"
IMAGE_URL = "https://plus.unsplash.com/premium_photo-1706140675031-1e0548986ad1?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8bGl2aW5ncm9vbXxlbnwwfHwwfHx8MA%3D%3D" 

class AgentState(TypedDict):
    image_url: str
    api_key: str
    task_id: Any
    generated_3d_model: Any

class MeshyClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.meshy.ai/openapi/v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def create_image_to_3d_task(self, image_url):
        payload = {
            "image_url": image_url,
            "enable_pbr": True,
            "should_remesh": True,
            "should_texture": True
        }
        response = requests.post(f"{self.base_url}/image-to-3d", headers=self.headers, json=payload)
        response_json = response.json()
        
        print("Response Status:", response.status_code)
        print("Response Content:", response_json)

        response.raise_for_status()
        
        task_id = response_json.get("result")  
        if not task_id:
            raise ValueError(f"Meshy API did not return a valid task_id. Response: {response_json}")
        
        return task_id

    def get_task_status(self, task_id):
        response = requests.get(f"{self.base_url}/image-to-3d/{task_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, task_id, interval=5, timeout=300):
        start_time = time.time()
        while time.time() - start_time < timeout:
            task_status = self.get_task_status(task_id)
            if task_status['status'] in ['SUCCEEDED', 'FAILED', 'CANCELED']:
                return task_status
            time.sleep(interval)
        raise TimeoutError("Task timed out.")


def initiate_task(state):
    image_url = state['image_url']
    api_key = state['api_key']
    client = MeshyClient(api_key)
    task_id = client.create_image_to_3d_task(image_url)
    state['task_id'] = task_id
    return state

def check_task_status(state):
    task_id = state['task_id']
    api_key = state['api_key']
    client = MeshyClient(api_key)
    task_result = client.wait_for_completion(task_id)
    state['generated_3d_model'] = task_result
    return state

workflow = StateGraph(AgentState)
workflow.add_node("initiate_task", initiate_task)
workflow.add_node("check_task_status", check_task_status)
workflow.set_entry_point("initiate_task")
workflow.add_edge("initiate_task", "check_task_status")

graph_executor = workflow.compile()


# try:
#     display(Image(graph_executor.get_graph().draw_mermaid_png()))
# except Exception as e:
#     print(e)

def run_agent(image_url: str, api_key):
    state = {
        "image_url": image_url,
        "api_key": api_key
    }
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    result = graph_executor.invoke(state)
    data = result

    task_id = data.get("result")
    if not task_id:
        raise ValueError("No task ID received from POST response.")
    
    print(f"Task initiated with ID: {task_id}")

    # Optionally, you might want to wait/poll until the process is finished.
    # For a simple case, we'll perform one GET request.
    get_url = f"https://api.meshy.ai/openapi/v1/image-to-3d/{task_id}"
    

    while True:
        get_response = requests.get(get_url, headers=headers)
        get_response.raise_for_status()
        get_data = get_response.json()

        if get_data.get("status") == "completed":
            break
        print("Task not completed yet, waiting 5 seconds...")
        time.sleep(5)

    get_response = requests.get(get_url, headers=headers)
    get_response.raise_for_status()
    get_data = get_response.json()

    return get_data.model_urls