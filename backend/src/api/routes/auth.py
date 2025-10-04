from fastapi import APIRouter, Depends, HTTPException, Header
from src.core.auth import verify_token

router = APIRouter(prefix="/auth", tags=["auth"])

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    try:
        decoded = verify_token(token)
        if decoded is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return decoded  # contains uid, email, etc.
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"message": f"Hello {user['uid']}, you are authenticated!"}