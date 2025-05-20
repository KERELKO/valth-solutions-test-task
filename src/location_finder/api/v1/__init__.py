from ninja_extra import NinjaExtraAPI
from .handlers import router
from .auth import JWTAuthController


api = NinjaExtraAPI()
api.register_controllers(JWTAuthController)
api.add_router("/", router)
