from beanie import Document, Indexed


class User(Document):
    email: Indexed(str, unique=True)
    username: Indexed(str)
    password: str

    class Settings:
        name = 'users'
