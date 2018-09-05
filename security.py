from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, "chao", "jsu")
]

user_name_mapping = {u.username: u for u in users}
user_id_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = user_name_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return user_id_mapping.get(user_id, None)
