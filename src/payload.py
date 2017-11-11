class Payload:
    bytecode = bytes
    header = bytes
    message = bytes
    type = 0

    def __init__(self, type):
        if type == 1:
            self.header = b'system'
        else:
            self.header = b'data'

    def loadstring(self, data):
        self.message = str.encode(data)
