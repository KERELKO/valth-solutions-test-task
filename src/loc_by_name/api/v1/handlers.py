from ninja import Router


router = Router()


@router.get("/")
async def ping():
    return "hello world!"
