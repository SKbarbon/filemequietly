from ui_kit.settings_control_option import SettingsControlsOption
from utils.check_if_host_exist import check_if_host_exist
from utils.get_host_info import GetHostInfo
from utils.generate_client_code import generate_random_code
from utils.get_computer_name import get_computer_name
from tools.file_downloader import FileDownloader
import flet


class DownloadFilePage (flet.Container):
    def __init__(self):
        super().__init__()

        self.padding = 40

        self.client_name = get_computer_name()
        self.client_code = generate_random_code()

        self.main_col = flet.Column()
        self.content = self.main_col
        self.main_col.alignment = flet.MainAxisAlignment.CENTER
        self.main_col.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    
    def on_navigate(self):
        self.main_col.width = self.page.width
        self.main_col.height = self.page.height - 40

        self.main_col.controls.append(flet.Row([
            flet.Text("Before starting, you need to provide those information", expand=True, size=28, weight=flet.FontWeight.W_800)
        ]))

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

        client_name = SettingsControlsOption(
            app_class=self.app_class,
            option_label="Your Name",
            explaination="Enter your name so the host recognise you.",
            on_change_option_event=lambda l, new_name: self.set_client_name(name=new_name)
        )
        client_name.put_option(type="string", default=get_computer_name())
        self.main_col.controls.append(client_name)

        host_link = SettingsControlsOption(
            app_class=self.app_class,
            option_label="Host Link",
            explaination="Ask the host to provide you with a host link, then provide it here.",
            on_change_option_event=lambda l, host_link: self.when_host_link_set(host_link=host_link)
        )
        host_link.put_option(type="string", default="empty")
        self.main_col.controls.append(host_link)

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

        self.main_col.controls.append(flet.Row([
            flet.TextButton(content=flet.Text("Go Back", color=flet.colors.BLUE), on_click=lambda e: self.go_back())
        ]))

        self.update()
    

    def when_host_link_set (self, host_link):
        self.main_col.controls.clear()

        if check_if_host_exist(host_link=host_link) == False:
            self.show_error(error="This host can't be accessed, click to go back.")
            return
        
        self.host_info = GetHostInfo(host_link=host_link)

        # UI
        file_name_label = flet.Text(self.host_info.file_name, weight=flet.FontWeight.W_900, size=20)
        self.main_col.controls.append(flet.Row([file_name_label]))

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

        self.status_label = flet.Text(f"Hey, {self.client_name}. You are waiting for the host to accept..", width=300,
                                      weight=flet.FontWeight.W_300, size=17)
        self.main_col.controls.append(self.status_label)

        self.download_progress_bar = flet.ProgressBar(
            value=0,
            width=200,
            bgcolor=None,
            color=flet.colors.BLUE
        )
        self.main_col.controls.append(self.download_progress_bar)

        self.client_code_label = flet.Text(self.client_code, weight=flet.FontWeight.W_300, size=25,
                                tooltip="This is your 'client code'. Maybe the host will ask you for the code to verify you.")
        self.main_col.controls.append(self.client_code_label)

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer
        
        warning_text = "Warning: Only download files from hosts you trust. Unknown files can be risky."
        self.main_col.controls.append(
            flet.Text(warning_text, color="#ffeb97", weight=flet.FontWeight.W_300, size=14)
        )

        # Start downloading the file
        file_downloader = FileDownloader(
            url=self.host_info.download_file_url,
            json_data={
                "client_name": self.client_name,
                "client_code": self.client_code
            },
            progress_handler=self.update_download_progress,
            on_done=self.download_finished,
            error_event_handler=self.show_error,
            save_as_name=self.host_info.file_name
        )
        file_downloader.start()
        
    

    def update_download_progress (self, progress_num:int):
        self.download_progress_bar.value = progress_num * 0.01
        self.download_progress_bar.bgcolor = flet.colors.BLACK54
        self.status_label.value = f"Downloading.."
        self.update()
    

    def download_finished (self, downloaded_file_path:str):
        self.main_col.controls.clear()

        file_name_label = flet.Text(self.host_info.file_name, weight=flet.FontWeight.W_900, size=20)
        self.main_col.controls.append(flet.Row([file_name_label]))

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

        if self.host_info.post_download_message is not None:
            self.main_col.controls.append(flet.Row([flet.Text(self.host_info.post_download_message)], expand=True, alignment=flet.MainAxisAlignment.CENTER))
        self.main_col.controls.append(flet.Text("Your file is in the default Downloads folder.", weight=flet.FontWeight.W_300, 
                                                size=13, color=flet.colors.GREY))

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

        self.main_col.controls.append(flet.Row([flet.TextButton("Back", on_click=lambda e: self.go_back())]))

        self.update()
        
        
    

    def show_error (self, error_code:int=None, error:str=""):
        self.main_col.controls.clear()

        if error_code == 401 or str(error) == "HTTP 401":
            error = "The host declined your request."
        self.main_col.controls.append(flet.TextButton(
            content=flet.Text(error, color="red"), 
            on_click=lambda e: self.go_back()
        ))
        if hasattr(self, "page"):
            self.update()

        

    
    def set_client_name (self, name:str):
        self.client_name = name

    def go_back (self):
        self.app_class.go_back_page()
