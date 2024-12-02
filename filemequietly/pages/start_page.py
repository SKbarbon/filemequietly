from pages.share_file_page import ShareFilePage
from pages.download_file_page import DownloadFilePage
from pages.sharing_requirements_page import SharingRequirementsPage
from host.host import Host
import flet, threading, time



class StartPage (flet.Column):
    def __init__ (self, app_class):
        super().__init__()
        self.app_class = app_class

        self.alignment = flet.MainAxisAlignment.CENTER
        self.horizontal_alignment = flet.CrossAxisAlignment.CENTER

        download_a_file = flet.TextButton(content=flet.Text(
            value="Download\na File",
            weight=flet.FontWeight.BOLD,
            size=30,
            color="white"
        ), on_click=lambda e: self.open_download_page())
        
        share_a_file = flet.TextButton(content=flet.Text(
            value="Share\nYour File",
            weight=flet.FontWeight.BOLD,
            size=30,
            color="white"
        ), on_click=lambda e: self.open_share_page())

        self.controls.append(flet.Row([
            download_a_file,
            flet.Text("|"),
            share_a_file
        ], alignment=flet.MainAxisAlignment.CENTER, 
            vertical_alignment=flet.CrossAxisAlignment.CENTER,
            spacing=30))
    

    def open_share_page (self):
        if self.app_class.host_class is None:
            if self.app_class.ngrok_token is None:
                self.app_class.navigate_to_page(view=SharingRequirementsPage())
                return
            self.app_class.host_class = Host(ngrok_token=self.app_class.ngrok_token)
            threading.Thread(target=self.app_class.host_class.start_host, daemon=True).start()
        
        self.app_class.navigate_to_page(view=ShareFilePage())

    def open_download_page (self):
        self.app_class.navigate_to_page(view=DownloadFilePage())