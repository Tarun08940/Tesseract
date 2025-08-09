# chat/middleware.py
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

@sync_to_async
def get_user_for_token(token):
    """
    Uses DRF SimpleJWT's JWTAuthentication to validate token and return user.
    Runs in a thread (sync) wrapped by sync_to_async so we can call from async code.
    """
    jwt_auth = JWTAuthentication()
    validated_token = jwt_auth.get_validated_token(token)
    user = jwt_auth.get_user(validated_token)
    return user

class JWTAuthMiddleware:
    """
    ASGI middleware that looks for ?token=... in the querystring and, if present,
    authenticates a user and sets scope['user'].
    """
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self.inner)

class JWTAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = dict(scope)  # shallow copy
        self.inner = inner

    async def __call__(self, receive, send):
        # Parse query string
        query_string = self.scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token_list = params.get('token')

        if token_list:
            token = token_list[0]
            try:
                user = await get_user_for_token(token)
                self.scope['user'] = user
            except Exception:
                # any failure -> anonymous
                self.scope['user'] = AnonymousUser()
        else:
            # no token -> anonymous (you can choose to fallback to session auth later)
            self.scope['user'] = AnonymousUser()

        inner = self.inner(self.scope)
        return await inner(receive, send)
