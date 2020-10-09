class OutOfRange(Exception):
    def __init__(self, message="Requested Range Not Satisfiable", status_code=416, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
