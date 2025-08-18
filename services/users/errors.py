class UserNotFound(Exception):
    def __str__(self):
        return "User not found"
