class User:
    def __init__(self, name: str, email: str, role: str, user_id: str = None):
        self.__id = user_id
        self.name = name
        self.email = email
        self.role = role  # e.g., 'barber', 'admin', 'customer'

    @property
    def id(self) -> str:
        return self.__id

    def is_admin(self) -> bool:
        return self.role.lower() == "admin"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "role": self.role
        }