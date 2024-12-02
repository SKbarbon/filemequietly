from .flask_app import FlaskApp
from .ngrok_bridge import NgrokBridge
import threading, time, sys


class Host:
    def __init__(self, ngrok_token:int):
        self.host_is_running = False
        self.ngrok_token = ngrok_token

        self.flask_app = FlaskApp()
        self.ngrok_bridge = None

    
    def start_host (self):
        """Designed to run inside a thread ONLY!. Otherwise it will stop the whole python script if tried to stop the host."""
        self.host_is_running = True

        threading.Thread(target=self.flask_app.start_host, daemon=True).start()
        time.sleep(2)

        self.ngrok_bridge = NgrokBridge()
        self.ngrok_bridge.ngrok_token = self.ngrok_token
        self.ngrok_bridge.start(with_port=self.flask_app.flask_app_port)

        while self.host_is_running: time.sleep(2)
        sys.exit()
        
    
    def set_download_file_path (self, new_file_path:str):
        self.flask_app.file_path_to_download = new_file_path
    

    def set_on_download_event (self, on_download_event):
        self.flask_app.on_download_file = on_download_event
    

    def set_post_download_message (self, message:str):
        if hasattr(self, "flask_app"):
            self.flask_app.post_download_message = message
    
    
    def stop_sharing (self):
        """Will not affect the on-going downloads"""
        self.flask_app.file_path_to_download = None


    def close_host (self):
        """This function doesn't work for now."""
        self.host_is_running = False