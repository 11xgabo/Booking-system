from fastapi import FastAPI, HTTPException, status
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

from schemas.user_schema import UserCreate, UserResponse
from domain.user import User
from repositories.user_repository import SupabaseUserRepository

app = FastAPI(title="Barber Shop Agenda API - Users Module")

# Infrastructure Initialization
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
user_repo = SupabaseUserRepository(supabase_client)


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_21_CREATED)
def create_user(user_in: UserCreate):
    try:
        new_user = User(name=user_in.name, email=user_in.email, role=user_in.role)
        saved_user = user_repo.create(new_user)
        return saved_user.to_dict() | {"id": saved_user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict() | {"id": user.id}


@app.get("/users/", response_model=list[UserResponse])
def get_all_users():
    users = user_repo.get_all()
    return [u.to_dict() | {"id": u.id} for u in users]


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_in: UserCreate):
    user_data = User(name=user_in.name, email=user_in.email, role=user_in.role)
    updated_user = user_repo.update(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found to update")
    return updated_user.to_dict() | {"id": updated_user.id}


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    deleted = user_repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None