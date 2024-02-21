from app.auth import *


#this file is needed to create a user token with flask_login

class UserLogin():
    def fromDB(self, user_id):
        self.__user = get_user(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return str(self.__user.id)
    


#get user from db
def get_user(user_id):
    with Session() as s:
        user = s.query(User).filter(User.id==user_id).first()
        if not user:
            print("User is not exist")
            return False
        return user