import ngrok




class NgrokBridge:
    def __init__(self):
        self.ngrok_token = None

    def start(self, with_port:int):
        listener = ngrok.forward(with_port, )