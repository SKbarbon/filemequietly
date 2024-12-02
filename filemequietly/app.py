from ui_kit.page_theme import page_theme
from pages.start_page import StartPage
import flet



class App:
    def __init__(self, page: flet.Page):
        self.page : flet.Page = page

        # Host Data (if host is initialized those will be updated).
        self.ngrok_token = self.get_access_token()
        self.host_class = None

        # Set Page Theme
        page_theme(page=page)
        page.title = "FileMeQuietly"
        page.update()

        # UI Data
        self.pages_memory = [] # Stores the navigated pages so the user can get back.

        # UI
        self.view_conatiner = flet.AnimatedSwitcher(content=flet.Text(""), duration=200, reverse_duration=50)
        self.view_conatiner.width = page.window.width
        self.view_conatiner.height = page.window.height
        page.add(self.view_conatiner)

        page.update()

        # Show starting page
        self.navigate_to_page(view=StartPage(app_class=self))
        
    
    def navigate_to_page (self, view, its_back_navigation=False):
        """Navigate to a new page."""
        view.app_class = self
        # Stores the page in the pages memory so it can be navigated back to it.
        if its_back_navigation == False: self.pages_memory.append(self.view_conatiner.content)
        self.view_conatiner.content = view
        self.view_conatiner.update()

        # Call the `on_navigate` event handler if existed.
        if hasattr(view, "on_navigate") and its_back_navigation == False:
            view.on_navigate()
        
    def go_back_page (self):
        """Navigate to the previous page"""
        if len(self.pages_memory) > 1:
            the_page = self.pages_memory[-1]
            self.pages_memory.remove(the_page)
            self.navigate_to_page(the_page, its_back_navigation=True)

            # Call the `on_navigate_back` event handler if existed.
            if hasattr(the_page, "on_navigate_back"):
                the_page.on_navigate_back()
    


    # tools
    def get_access_token (self):
        """Returns user's ngrok access token, or `None`."""
        filemequietly_d = self.page.client_storage.get("filemequietly")
        if isinstance(filemequietly_d, dict):
            if "ngrok_access_token" in filemequietly_d:
                return filemequietly_d['ngrok_access_token']
        return None
    
    def store_access_token (self, token:str):
        """Stores ngrok access token using `flet`'s storage tool.
        
        Source of usage: https://flet.dev/docs/cookbook/client-storage/"""
        filemequietly_d = {
            "ngrok_access_token": token
        }
        self.page.client_storage.set(key="filemequietly", value=filemequietly_d)
        self.ngrok_token = token
        

flet.app(target=App)