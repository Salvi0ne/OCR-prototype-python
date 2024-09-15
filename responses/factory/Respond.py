from flask import jsonify

class Respond:
    def __init__(self, message, data):
        self.message = message
        self.data = data if data is not None else None
        self.code = 0
        self.status_code: None
        self.messages = []

    def json_respond(self):
        response = {
            "code": self.code,
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data,
            "messages": self.messages
        }
        return jsonify(response), 200

    def set_messages(self,__messages):
        """Return the message."""
        self.messages = __messages
    
    def set_code(self, __code):
        """Return the code."""
        self.code = __code
    
    def set_status_code(self, __status_code):
        self.status_code = __status_code

    def set_message(self, __message):
        self.message = __message

    def set_data(self, __data):
        self.data = __data
