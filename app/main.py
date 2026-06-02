from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine 
from app.models.post_model import Post
from app.models.user_model import User
from app.api.post_routes import router as post_router
from app.api.brand_routes import router as brand_router
from app.api.auth_router import router as auth_router
from app.api.user_routes import router as user_router
from app.api.user_routes import router as brand_router
from app.api.upload_routes import (
    router as upload_router
)




app = FastAPI(
    title="Social Poster API",
    version="1.0.0"
)

# Create tables
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "https://socail-autoposter-frontend.vercel.app",
        "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(brand_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(brand_router)
app.include_router(upload_router)

@app.get("/")
def home():
    return {
        "message": "Social Poster Backend Running"
    }