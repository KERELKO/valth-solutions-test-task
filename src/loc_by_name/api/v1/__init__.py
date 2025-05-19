from ninja import NinjaAPI
from .handlers import router


api = NinjaAPI()
api.add_router("/", router)
