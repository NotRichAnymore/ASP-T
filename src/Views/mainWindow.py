import PySimpleGUI as sg
import os



class MainWindow:

    def __init__(self):
        self.minimise_button = sg.Button(image_filename='', key='minimise_button')
        self.maximise_button = sg.Button(image_filename='', key='maximise_button')
        self.exit_button = sg.Button(image_filename='', key='exit_button')

        self.output_box = sg.Output(key='output_screen')

        self.command_prompt = sg.Text(key='command_prompt')
        self.command_arguments = sg.InputText(key='command_arguments')


    def get_title(self):
        return 'ASP-T CMD Prompt'

    def set_toolbar_layout(self):
        layout = self.minimise_button, self.maximise_button, self.exit_button
        return layout

    def set_output_screen(self):
        layout = self.output_box
        return layout

    def set_input_bar(self):
        layout = self.command_prompt, self.command_arguments
        return layout

    def build_layout(self):
        layout = [
            [self.set_toolbar_layout()],
            [self.set_output_screen()],
            [self.set_input_bar()]
        ]
        return layout

    def create_window(self):
        return sg.Window(title=self.get_title(), layout=self.build_layout(), no_titlebar=True, grab_anywhere=True,
                         keep_on_top=True, modal=True)


