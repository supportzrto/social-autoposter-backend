from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine 
from app.models.post_model import Post
from app.api.post_routes import router as post_router
from app.api.brand_routes import router as brand_router

app = FastAPI(
    title="Social Poster API",
    version="1.0.0"
)

# Create tables
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(brand_router)

@app.get("/")
def home():
    return {
        "message": "Social Poster Backend Running"
    }