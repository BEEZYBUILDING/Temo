from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['email'] = user.email
        token['user_id'] = user.id
        token['role'] = user.role
        
        return token