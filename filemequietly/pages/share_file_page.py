from utils.host_permissions import HOST_PERMISSIONS
from ui_kit.settings_control_option import SettingsControlsOption
from tools.play_alert_sound import play_alert_sound
from urllib.parse import urljoin
from utils.get_time import get_current_time
import flet, time, os, random


class ShareFilePage (flet.Column):
    def __init__(self):
        super().__init__()
        self.app_class = None # Will be updated when navigated to here.
        self.selected_file_path = None
        self.current_host_permissions = {}

        self.current_users_on_hold = []
        self.refused_users = []
        # UI Base
        self.disabled = True
        self.main_row = flet.Row(spacing=0)
        self.controls.append(self.main_row)

        self.left_section_container = flet.Container(padding=15)
        self.left_section_column = flet.Column()
        self.left_section_container.content = self.left_section_column
        self.main_row.controls.append(self.left_section_container)

        self.main_row.controls.append(flet.Text("", expand=True)) # Spacer

        self.right_section_container = flet.Container(padding=20, bgcolor=flet.colors.BLACK)
        self.right_section_column = flet.Column(scroll=flet.ScrollMode.ADAPTIVE, spacing=15)
        self.right_section_container.content = self.right_section_column
        self.main_row.controls.append(self.right_section_container)

        # UI - Left Section
        self.file_name_label = flet.Container(
            content=flet.Text("No File", weight=flet.FontWeight.W_900, size=29, 
                              overflow=flet.TextOverflow.ELLIPSIS, width=200, height=50),
            on_click=lambda e: self.select_another_file(),
            tooltip="Click to change the selected file."
        )
        self.left_section_column.controls.append(self.file_name_label)

        self.stop_sharing_button = flet.Container(content=flet.Text("Stop Sharing", color="#ff6d6d"), 
                                                  on_click=lambda e: self.on_stop_sharing(),
                                                  tooltip="Click to stop sharing the file")
        self.left_section_column.controls.append(self.stop_sharing_button)

        self.left_section_column.controls.append(flet.Row([
            flet.Container(content=flet.Text("Copy host link", color="blue", weight=flet.FontWeight.W_300), 
                            on_click=lambda e: self.copy_host_link_clipboard()),
            flet.Text("|"),
            flet.Container(content=flet.Text("Copy download link", color="blue", weight=flet.FontWeight.W_300), 
                            on_click=lambda e: self.copy_host_link_clipboard(download_link=True))
        ], spacing=10))


        self.left_section_column.controls.append(flet.Text("", height=25)) # PADDING

        self.subtitle_status_label = flet.Text("Status", color="#dcdcdc", size=15)
        self.left_section_column.controls.append(self.subtitle_status_label)

        self.downloads_counter_label = flet.Text("0 Downloads", color="#838383", size=13, weight=flet.FontWeight.W_300)
        self.left_section_column.controls.append(self.downloads_counter_label)

        self.column_who_downloaded = flet.Column(expand=True, scroll=flet.ScrollMode.ADAPTIVE)
        self.left_section_column.controls.append(self.column_who_downloaded)

        self.waiting_for_accept_place = flet.Stack(height=150)
        self.left_section_column.controls.append(self.waiting_for_accept_place)

        # UI - Right Section
        self.right_section_title_label = flet.Text("Sharing &\nPermissions", color=flet.colors.WHITE,
                                             size=29, weight=flet.FontWeight.W_900)
        self.right_section_column.controls.append(self.right_section_title_label)
        
    
    def user_select_file (self) -> str:
        """Waits until the user select a file.
        
        Returns a full path of the selected file. If cancled returns `False`"""
        def stop_waiting (): self.wait_to_select_file = False
        def file_result (e):
            fp = ", ".join(map(lambda f: f.path, e.files)) if e.files else False
            self.selected_file_path = fp
            stop_waiting()

        self.wait_to_select_file = True
        pick_files_dialog = flet.FilePicker(on_result=file_result, )
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        pick_files_dialog.pick_files(allow_multiple=False)
        
        while self.wait_to_select_file: time.sleep(2)
        return self.selected_file_path
    

    def start_sharing_file (self, file_path:str):
        """Pass the file path, and it will make the page focus on it and 
        forward the host to share the given file path when requested to download."""
        self.disabled = False
        self.app_class.host_class.set_download_file_path(file_path)
        self.app_class.host_class.set_on_download_event(self.on_try_to_download)

        self.file_name_label.content.value = str(os.path.basename(file_path))
        self.column_who_downloaded.controls.clear()

        self.update()
    

    def copy_host_link_clipboard (self, download_link=False):
        if download_link:
            host_link = str(self.app_class.host_class.ngrok_bridge.ngrok_host_url)
            full_url = urljoin(host_link, "download_file")
            self.page.set_clipboard(value=str(full_url))
        else:
            self.page.set_clipboard(value=str(self.app_class.host_class.ngrok_bridge.ngrok_host_url))
    

    def ask_to_download (self, waiting_number:int, client_name:str=None, client_code:str=None) -> bool:
        """Shows an alert to ask for download. Time out after a minute (dicline the request)."""
        def answered (e):
            if e.control.text == "Allow":
                self.log_a_client(client_name=client_name)
                self.current_users_on_hold.remove(waiting_number)
            else: self.refused_users.append(waiting_number)
            self.waiting_for_accept_place.controls.remove(c)
            self.update()
        if client_name is None: client_name = "Unknown"
        if client_code is None: client_code = "None"

        # Add the asking card and play a notify sound.
        c = flet.Container(
            content=flet.Column([
                flet.Text(f"Allow '{client_name[:20]}' to download?", size=10),
                flet.Text(f"Client Code: {client_code}", size=10),
                flet.Row([
                    flet.TextButton("Allow", on_click=answered),
                    flet.TextButton("Refuse", on_click=answered)
                ]),
                flet.Text("Ask the client for their code to compare.", size=8)
            ], alignment=flet.MainAxisAlignment.CENTER, horizontal_alignment=flet.CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor=self.page.bgcolor
        )
        self.waiting_for_accept_place.controls.append(c)
        self.update()
        play_alert_sound()

        # Start a timeout and check if host answered, per min.
        for t in range(60):
            if waiting_number not in self.current_users_on_hold: return True # User is accepted
            if waiting_number in self.refused_users:
                # User is refused, return a Decline
                self.current_users_on_hold.remove(waiting_number)
                self.refused_users.remove(waiting_number)
                return False
            time.sleep(1)
        
        # Timeout has reached and host still did not answer. Result is Decline.
        self.current_users_on_hold.remove(waiting_number)
        self.waiting_for_accept_place.controls.remove(c)
        self.update()
        return False
    

    def log_a_client (self, client_name:str):
        """Shows the client name who did download the file with the time of download.
        
        Also increase the downloads counter by one."""
        current_time = get_current_time()

        self.column_who_downloaded.controls.append(flet.Row([
            flet.Text(f"{current_time}", weight=flet.FontWeight.W_300, size=10, color="#ababab"),
            flet.Text(f"{client_name[:20]}", weight=flet.FontWeight.W_300, size=14, color="white")
        ]))

        count_plus = int(self.downloads_counter_label.value.replace(" Downloads", ""))
        count_plus = count_plus + 1
        self.downloads_counter_label.value = f"{count_plus} Downloads"
        self.update()



    def update_current_host_perm (self, permission_name:str, new_permission_value):
        """Update the current permission of the sharing host."""
        self.current_host_permissions[permission_name] = new_permission_value
    

    def select_another_file (self):
        """This will ask the user to select another file so the download link be updated with new file."""
        selected_file_path = self.user_select_file()
        if selected_file_path != False:
            self.start_sharing_file(file_path=selected_file_path)

    
    # Events
    def on_navigate(self):
        """Called when user navigate to this Page."""
        self.app_class.host_class.flask_app.info_holder_class = self
        self.left_section_column.height = self.page.height - 20

        self.right_section_column.width = self.page.width / 1.75
        self.right_section_column.height = self.page.height - 20
        self.update()

        # Put Permissions controllers
        for hp in HOST_PERMISSIONS:
            hp_type = HOST_PERMISSIONS[hp]['type']
            hp_explaination = HOST_PERMISSIONS[hp]['explaination']
            hp_default_value = HOST_PERMISSIONS[hp]['default']
            self.current_host_permissions[hp] = hp_default_value
            sco = SettingsControlsOption(app_class=self.app_class,
                                         option_label=hp, explaination=hp_explaination, 
                                         on_change_option_event=self.update_current_host_perm)
            sco.put_option(type=hp_type, default=hp_default_value)
            self.update_current_host_perm(permission_name=hp, new_permission_value=hp_default_value)
            self.right_section_column.controls.append(sco)
        
        # Ask user to select a file.
        selected_file_path = self.user_select_file()
        if selected_file_path == False:
            self.app_class.go_back_page()
            return
        self.start_sharing_file(file_path=selected_file_path)
    

    def on_stop_sharing (self):
        self.app_class.host_class.stop_sharing()
        self.app_class.go_back_page()
    

    def on_try_to_download (self, download_request_data) -> bool:
        """This function will be called when a user try to download the selected file. if returns `False` download is cancelled."""
        if self.current_host_permissions['Ask to download'] == False:
            if download_request_data['request_method'] == "POST":
                if "client_name" in download_request_data: self.log_a_client(client_name=download_request_data['client_name']); return
                else: self.log_a_client(client_name="Unknown")
            self.log_a_client(client_name="Unknown")
            return True

        # Give the user a waiting number.
        waiting_number = random.choice(range(999, 99999))
        times_of_try = 0
        while waiting_number in self.current_users_on_hold: 
            waiting_number = random.choice(range(999, 99999))
            times_of_try = times_of_try + 1
            if times_of_try > 10000: print("Can't generate waiting number"); return False
        self.current_users_on_hold.append(waiting_number)
        
        # Ask the host to accept the user request.
        if download_request_data['request_method'] == "GET":
            ask_state = self.ask_to_download(waiting_number=waiting_number)
        else:
            if 'client_name' in download_request_data and 'client_code' in download_request_data:
                ask_state = self.ask_to_download(waiting_number,
                                                 download_request_data['client_name'], 
                                                 download_request_data['client_code'])
            else:
                print("Bad POST request")
                return False
        
        return ask_state