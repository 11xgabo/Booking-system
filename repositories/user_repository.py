from abc import ABC, abstractmethod
from typing import List, Optional
from supabase import Client
from domain.user import User

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User: pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]: pass
    
    @abstractmethod
    def get_all(self) -> List[User]: pass
    
    @abstractmethod
    def update(self, user_id: str, user: User) -> Optional[User]: pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool: pass


class SupabaseUserRepository(UserRepository):
    def __init__(self, supabase_client: Client):
        self.client = supabase_client
        self.table_name = "users"  # Remember to name your table 'users' in Supabase too!

    def create(self, user: User) -> User:
        payload = user.to_dict()
        response = self.client.table(self.table_name).insert(payload).execute()
        row = response.data[0]
        return User(user_id=row["id"], name=row["name"], email=row["email"], role=row["role"])

    def get_by_id(self, user_id: str) -> Optional[User]:
        response = self.client.table(self.table_name).select("*").eq("id", user_id).execute()
        if not response.data:
            return None
        row = response.data[0]
        return User(user_id=row["id"], name=row["name"], email=row["email"], role=row["role"])

    def get_all(self) -> List[User]:
        response = self.client.table(self.table_name).select("*").execute()
        return [
            User(user_id=row["id"], name=row["name"], email=row["email"], role=row["role"])
            for row in response.data
        ]

    def update(self, user_id: str, user: User) -> Optional[User]:
        payload = user.to_dict()
        response = self.client.table(self.table_name).update(payload).eq("id", user_id).execute()
        if not response.data:
            return None
        row = response.data[0]
        return User(user_id=row["id"], name=row["name"], email=row["email"], role=row["role"])

    def delete(self, user_id: str) -> bool:
        response = self.client.table(self.table_name).delete().eq("id", user_id).execute()
        return len(response.data) > 0