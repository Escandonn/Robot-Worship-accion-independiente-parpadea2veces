from fastapi import FastAPI
from app.controllers.face_controller import router as face_router
from app.controllers.robot_controller import router as robot_router

# Create FastAPI app instance
app = FastAPI(
    title="WORSHIP Mascot Robot - Backend",
    description="Backend API for the WORSHIP Mascot Robot providing facial components and interpretation services",
    version="0.1.0"
)

# Include routers
app.include_router(face_router)
app.include_router(robot_router)

# Root endpoint for health check
@app.get("/", tags=["health"])
async def root():
    """Root endpoint for health checking."""
    return {"message": "WORSHIP Mascot Robot Backend is running", "status": "healthy"}