from pages.ask_for_text_page import AskForTextPage
import flet



class SettingsControlsOption (flet.Row):
    """A view class that can turn to a many settings controlling option.
    
    Pass a function for `on_change_option_event` to call when value is changed."""
    def __init__ (self, app_class, option_label:str, explaination:str="", on_change_option_event=None):
        super().__init__()
        self.app_class = app_class
        self.option_label = option_label
        self.explaination = explaination
        self.on_change_option_event = on_change_option_event

        self.controls.append(
            flet.Column([
                flet.Text(self.option_label, color=flet.colors.WHITE, weight=flet.FontWeight.W_300, size=14),
                flet.Text(self.explaination, color="#b6b6b6", weight=flet.FontWeight.W_300, size=11, 
                          overflow=flet.TextOverflow.CLIP, width=350)
            ], spacing=1)
        )

        self.controls.append(flet.Text("", expand=True)) # Spacer

        self.option_controller_container = flet.Container()
        self.controls.append(self.option_controller_container)
    
    def put_option (self, type:str, default):
        """Pass the option type, and it will convert the option the correct control."""
        if type == "bool":
            self.boolian_option(default=default)
        elif type == "string":
            self.string_option(default=default)


    # Controls
    def boolian_option (self, default:bool=True):
        """Converts the view to a boolian selecter option."""
        def switch_it(e):
            the_word = str(e.control.content.value)
            if the_word == "Yes":
                self.on_change_option_event(self.option_label, False)
                e.control.content.value = "No"
            else:
                self.on_change_option_event(self.option_label, True)
                e.control.content.value = "Yes"
            e.control.update()

        if default == True: word = "Yes"
        else: word = "No"
        self.option_controller_container.content = flet.TextButton(
            content=flet.Text(word, color="#57b3ff"),
            on_click=switch_it
        )
    
    def string_option (self, default:str=""):
        """Converts the view to a option to write texts"""
        self.default_ = default
        def start_writing (e):
            self.app_class.navigate_to_page(view=AskForTextPage(
                question=self.option_label,
                explaination=self.explaination,
                on_submit=on_submit_text,
                default_value=self.default_
            ))
        
        def on_submit_text (text):
            self.on_change_option_event(self.option_label, text)
            self.option_controller_container.content.content.value = text[:9]
            self.option_controller_container.content.tooltip = f'"{text}"'
            self.default_ = text
            
        
        self.option_controller_container.content = flet.TextButton(
            content=flet.Text(default[:9], color="#57b3ff"),
            on_click=start_writing,
            tooltip=f'"{default}"'
        )