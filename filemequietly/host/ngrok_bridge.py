import ngrok




class NgrokBridge:
    def __init__(self):
        self.ngrok_token = None
        self.ngrok_host_url = None

    def start(self, with_port:int) -> str:
        """Returns the URL of the ngrok host"""
        listener = ngrok.forward(with_port, authtoken=self.ngrok_token)
        self.ngrok_host_url = listener.url()
        return str(listener.url())