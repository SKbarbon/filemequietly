from ui_kit.page_theme import page_theme
import flet



class App:
    def __init__(self, page: flet.Page):
        self.page : flet.Page = page

        # Set Page Theme
        page_theme(page=page)
        page.title = "FileMeQuietly"

        
        page.update()


flet.app(target=App)