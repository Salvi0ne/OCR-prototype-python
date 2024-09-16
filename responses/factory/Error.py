from responses.factory.Respond import Respond


class Error(Respond):
    def __init__(self, message=None, code=400, status_code="Bad Request"):
        super().__init__(message, None)
        self.code = code
        self.status_code = status_code
