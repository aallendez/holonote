from fastapi import APIRouter, Depends, Header, HTTPException
from src.core.auth import verify_token, verify_token_and_ensure_user

router = APIRouter(prefix="/auth", tags=["auth"])


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    try:
        decoded = verify_token_and_ensure_user(token)
        if decoded is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return decoded  # contains uid, email, user_data, etc.
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"message": f"Hello {user['uid']}, you are authenticated!"}


@router.get("/user-info")
def get_user_info(user=Depends(get_current_user)):
    """Get current user information from database"""
    return {"firebase_uid": user["uid"], "user_data": user.get("user_data", {})}
