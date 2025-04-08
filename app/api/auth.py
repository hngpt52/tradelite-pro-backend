from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from app.db.supabase import get_supabase_client

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, supabase=Depends(get_supabase_client)):
    """
    Register a new user
    """
    try:
        # Register user with Supabase Auth
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        
        if response.error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.error.message
            )
        
        # Return user data
        return {
            "id": response.user.id,
            "email": response.user.email
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, supabase=Depends(get_supabase_client)):
    """
    Login user and return access token
    """
    try:
        # Sign in user with Supabase Auth
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if response.error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Return access token
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/logout")
async def logout(supabase=Depends(get_supabase_client)):
    """
    Logout user
    """
    try:
        # Sign out user
        response = supabase.auth.sign_out()
        
        if response.error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.error.message
            )
        
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/reset-password")
async def reset_password(email: str, supabase=Depends(get_supabase_client)):
    """
    Send password reset email
    """
    try:
        # Send password reset email
        response = supabase.auth.reset_password_email(email)
        
        if response.error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.error.message
            )
        
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
