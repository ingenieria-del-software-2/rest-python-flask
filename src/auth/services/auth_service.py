from bson.objectid import ObjectId
from src.auth.auth_exception import UserNotFoundException


class UserService:
    def create_user(self, user_data, show_password=False):
        from src.app import mongo
        user_data["password"] = _encrypt_password(user_data["password"])
        inserted = mongo.db.user.insert_one(user_data)
        filtered_fields = {'_id': False }
        if not show_password:
            filtered_fields.update({"password": False})

        user = mongo.db.user.find_one(
            {"_id": ObjectId(inserted.inserted_id)},
            filtered_fields
        )
        return user

    def get_user_by(self, field, value, show_password=False):
        from src.app import mongo
        filtered_fields = {'_id': False }
        if not show_password:
            filtered_fields.update({"password": False})
        user = mongo.db.user.find_one({field: value}, filtered_fields)
        if user is None:
            raise UserNotFoundException("User not found")
        return user

    def is_valid_user(self, username, password):
        from src.app import mongo
        user = mongo.db.user.find_one({"username": username})
        return UserService.compare_password(user["password"], password)

    @staticmethod
    def _encrypt_password(password):
        import hashlib
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    @staticmethod
    def compare_password(hashed, plain):
        import hashlib
        return hashed == hashlib.md5(plain.encode('utf-8')).hexdigest()

