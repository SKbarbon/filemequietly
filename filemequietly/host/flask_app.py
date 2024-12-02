from flask import Flask, send_file, request
import socket, traceback, logging, os


class FlaskApp:
    def __init__(self):
        self.app = Flask("__main__")

        self.flask_app_port = None

        self.host_info_class = None

        self.file_path_to_download = None
        self.on_download_file = None
        
        self.info_holder_class = None
    

    def start_host (self):
        @self.app.route("/")
        def index ():
            return ""
        

        @self.app.route("/download_file", methods=['POST', 'GET'])
        def download_file ():
            if self.file_path_to_download is None: return "<title>No File To Download</title>", 204
            if self.on_download_file is None: "<title>No File To Download</title>", 204

            if request.method == 'GET':
                data = {"request_method": 'GET'}
            else:
                data = request.json
                data['request_method'] = 'POST'
            if self.on_download_file(data) == False:
                return "Host refused", 401
            
            try: return send_file(self.file_path_to_download, as_attachment=True)
            except Exception as e:
                traceback.print_exc()
                return "Error", 500
        

        @self.app.route("/host_information", methods=['POST', 'GET'])
        def host_information ():
            if self.file_path_to_download is None: return {"ok": True, "host_active": False}
            return {
                "ok": True, 
                "host_active": True,
                "file_name": str(os.path.basename(self.file_path_to_download)),
                "post_download_message": str(self.info_holder_class.current_host_permissions['Post-download message'])
            }

        self.flask_app_port = self.find_free_port()

        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        self.app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
        self.app.run(host="localhost", port=self.flask_app_port, debug=False)
    

    def find_free_port(self):
        """
        Finds a free port available on the system.
        Returns the port number.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))  # Bind to an available port provided by the OS
            _, port = s.getsockname()
            return int(port)