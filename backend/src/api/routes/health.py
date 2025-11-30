from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@router.get("/ping")
def ping():
    """Simple ping endpoint for health checks"""
    return {"message": "pong"}
