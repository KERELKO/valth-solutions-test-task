class ApplicationException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class ServiceException(ApplicationException): ...
