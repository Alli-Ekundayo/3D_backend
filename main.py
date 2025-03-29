from fastapi import FastAPI
from routes.state_graph_routes import router as state_graph_router
from routes.feedback_routes import router as feedback_router

app = FastAPI()

app.include_router(state_graph_router)
app.include_router(feedback_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
