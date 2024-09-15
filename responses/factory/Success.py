from responses.factory.Respond import Respond

class Success(Respond):
    def __init__(self, message=None, data=None):
        super().__init__(message, data)
        self.code = 200
        self.status_code = "OK",
