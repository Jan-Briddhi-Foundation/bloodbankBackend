from knox.models import AuthToken


def create_knox_token(user, token_model=None,  serializer=None):
    token = AuthToken.objects.create(user=user)
    return token
