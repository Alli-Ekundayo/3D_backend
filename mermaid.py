# stategraph_diagram.py

def generate_mermaid_diagram() -> str:
    """
    Generates a Mermaid diagram representing the stategraph flow.
    """
    mermaid_code = """
stateDiagram-v2
    [*] --> Generation
    Generation --> Refinement
    Refinement --> ImageGeneration
    ImageGeneration --> AwaitingFeedback : Pause & return session_id
    AwaitingFeedback --> ImageEditing : Feedback received
    ImageEditing --> ThreeDRendering
    ThreeDRendering --> [*]
    """
    return mermaid_code.strip()

def main():
    diagram = generate_mermaid_diagram()
    
    # Write the Mermaid diagram to a file
    output_filename = "stategraph.mmd"
    with open(output_filename, "w") as file:
        file.write(diagram)
    
    # Print the Mermaid diagram
    print("Mermaid Diagram:")
    print(diagram)
    print(f"\nDiagram written to '{output_filename}'. You can visualize it using a Mermaid live editor.")

if __name__ == "__main__":
    main()
