from app import auth

users = {
    'web': 'test'
}

@auth.verify_password
def verify_password(uname, pwd):
    if uname in users:
        return users.get(uname) == pwd 