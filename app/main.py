# app/main.py
from fastapi import FastAPI
from app.config import settings
from app.routers import auth, prescriptions

app = FastAPI(
    title=settings.APP_NAME,
    description="Manage medical prescriptions securely",
    version="1.0.0",
    docs_url="/docs"   # Swagger UI auto-generated at http://localhost:8000/docs
)

# Register routers — this is why routers have prefixes
app.include_router(auth.router)
app.include_router(prescriptions.router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


