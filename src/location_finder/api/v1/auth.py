from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController


@api_controller("token", tags=["Auth"])
class JWTAuthController(TokenObtainPairController):
    """obtain_token and refresh_token only"""

    ...
