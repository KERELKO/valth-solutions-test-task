from ninja import Router
from django.http import HttpRequest


router = Router()


@router.get("/")
async def ping(request: HttpRequest):
    print(request.headers)
    return {"res": "hello world!"}
