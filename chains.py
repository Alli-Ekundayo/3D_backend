from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Generation prompt
generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         "You are a meticulous 3D design expert. Your task is to define a user’s initial description of a 3D scene or object in a way that includes minor details like materials, lighting, etc. "
         "Generate the best 3D design prompt based on the user's description. "
         "If the user provides additional information, use it to define the design."
         "summarize the prompt as short as possible"
        ),
        ("user", "{user_input}"),
    ]
)

# Refinement prompt
refinement_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """You are a meticulous 3D design expert. Your task is to refine a user’s initial description of a 3D scene or object by filling in the details for a high-quality design. 
         Begin by summarizing the user’s input, then fill in the best options covering the following areas:
         Materials and Textures
         Geometry
         Positioning and Layout
         Lighting and Environment
         Functionality and Additional Details
         """
        ),
        ("user", "{user_input}"), 
    ]
)


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key="AIzaSyDe1Et9beIvybcJfx25L1ESheFDB6yCMx0", max_tokens=500)


generation_chain = generation_prompt | llm
refinement_chain = refinement_prompt | llm
