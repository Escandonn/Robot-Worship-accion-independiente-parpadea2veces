from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.face_controller import router as face_router
from app.controllers.robot_controller import router as robot_router

# Create FastAPI app instance
app = FastAPI(
    title="WORSHIP Face Detection API",
    description="Backend API for the WORSHIP Mascot Robot providing facial components and interpretation services",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4321",
        "http://127.0.0.1:4321",
        "https://robot-worship-accion-independiente-sepia.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(face_router)
app.include_router(robot_router)

@app.get("/", tags=["health"])
async def root():
    return {"message": "WORSHIP Mascot Robot Backend is running", "status": "healthy"}


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}