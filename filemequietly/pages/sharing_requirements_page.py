from ui_kit.settings_control_option import SettingsControlsOption
import flet, ngrok, socket, time




class SharingRequirementsPage (flet.Container):
    def __init__ (self):
        super().__init__()

        self.padding = 25

        self.main_col = flet.Column()
        self.main_col.alignment = flet.MainAxisAlignment.CENTER
        self.main_col.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        self.content = self.main_col

    def on_navigate(self):
        self.main_col.controls.append(flet.Row([
            flet.Text("To start sharing, you need to provide your ngrok access token.", expand=True, size=28, weight=flet.FontWeight.W_800)
        ]))
        self.main_col.controls.append(flet.Row([
            flet.Container(
            content=flet.Text("Go to ngrok dashboard", color=flet.colors.BLUE, weight=flet.FontWeight.BOLD),
            url="https://dashboard.ngrok.com/get-started/your-authtoken"
        )
        ]))

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

        ngrok_token = SettingsControlsOption(
            app_class=self.app_class,
            option_label="Ngrok Access Token",
            explaination="Your Ngrok Access Token is used to create a global URL for your local host so other people can access it.",
            on_change_option_event=lambda l, token: self.on_give_token(token=token)
        )
        ngrok_token.put_option(type="string", default="Empty")
        self.main_col.controls.append(ngrok_token)

        self.error_label = flet.Text("", color="red")
        self.main_col.controls.append(self.error_label)

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

        self.update()
    

    def on_give_token (self, token:str):
        try:
            listener = ngrok.forward(addr=self.find_free_port(), authtoken=token)
            time.sleep(1)
            ngrok.disconnect(url=listener.url())
            self.app_class.store_access_token(token)
            self.app_class.go_back_page()
        except Exception as e:
            self.error_label.value = "Can't use this Ngrok Access Token!"
    

    def find_free_port(self):
        """
        Finds a free port available on the system.
        Returns the port number.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))  # Bind to an available port provided by the OS
            _, port = s.getsockname()
            return int(port)