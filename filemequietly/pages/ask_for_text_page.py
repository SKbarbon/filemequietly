import flet



class AskForTextPage (flet.Container):
    """A page used to ask the user to write a text, with ability go back to previous page."""
    def __init__ (self, question:str, explaination:str, default_value:str="", allow_go_back=True, on_submit=None, allow_cancel=True):
        super().__init__()

        self.question = question
        self.allow_go_back = allow_go_back
        self.on_submit_event = on_submit

        self.padding = 40

        self.main_col = flet.Column([
            flet.Row([flet.Text(value=question, weight=flet.FontWeight.W_900, size=28)]),
            flet.Row([flet.Text(value=explaination, expand=True, weight=flet.FontWeight.W_300)])
        ])
        self.content = self.main_col

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

        self.text_field = flet.TextField(
            value=default_value,
            label="Type Something..",
            focus_color=None,
            border="none",
            bgcolor="black",
            border_radius=18
        )
        self.main_col.controls.append(self.text_field)

        self.main_col.controls.append(flet.Row([
            flet.TextButton(content=flet.Text("Cancel", color="#cccccc", disabled=allow_cancel==False), on_click=self.go_back),
            flet.ElevatedButton(content=flet.Text("Submit", color="white"), bgcolor="#7d9eff", on_click=self.on_submit)
        ]))

        self.main_col.controls.append(flet.Text("", expand=True)) # Spacer

    
    def on_submit (self, e=None):
        self.on_submit_event(self.text_field.value)
        self.go_back()
    

    def go_back (self, e=None):
        self.app_class.go_back_page()
    

    def on_navigate(self):
        self.text_field.focus()