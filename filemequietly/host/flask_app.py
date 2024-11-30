from flask import Flask
import socket


class FlaskApp:
    def __init__(self):
        self.app = Flask("__main__")

        self.flask_app_port = None

        self.host_info_class = None

        self.on_download_file = None
    

    def start_host (self):
        @self.app.route("/")
        def index ():
            return ""
        
        @self.app.route("/host_info")
        def host_info ():
            return ""
        

        @self.app.route("/download_file")
        def download_file ():
            return ""
        

        self.flask_app_port = self.find_free_port()
        self.app.run(host="localhost")
    

    def find_free_port(self):
        """
        Finds a free port available on the system.
        Returns the port number.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))  # Bind to an available port provided by the OS
            _, port = s.getsockname()
            return port