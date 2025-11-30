from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.api_routes import api_router

app = FastAPI(title="Zeno-Backend")

# Register routers
app.include_router(api_router)


@app.get("/")
async def get_root():
    return {"message": "This is home route"}


# ---- CORS CONFIG ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


__all__ = ["api_router"]
