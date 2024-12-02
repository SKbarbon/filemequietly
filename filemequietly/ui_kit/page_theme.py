import flet



def page_theme (page: flet.Page):
    """Pass the `Page` class as a param, then it apply a pre-defined theme."""

    page.theme_mode = flet.ThemeMode.DARK
    page.bgcolor = "#222222"
    page.padding = 0

    page.window.title_bar_hidden = True

    page.window.resizable = False