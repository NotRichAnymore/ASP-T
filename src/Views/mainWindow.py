import os.path

import PySimpleGUI as sg
from src.Utilities.utilities import get_root_directory
from pathlib import Path


class MainWindow:

    def __init__(self):
        self.image_folder = Path('src/data/images').resolve().as_posix()
        self.title_text = sg.Text(text='ASP-T CMD Prompt', font=('Commodore 64 Angled', '12'), key='program_title')

        self.settings_button = sg.Button(tooltip='Settings', image_subsample=3, image_size=(16, 16),
                                         image_filename=os.path.join(self.image_folder, '\\settings_icon.png'),
                                         pad=((660, 0), (0, 0)), key='main_window_settings_button')

        self.minimise_button = sg.Button(tooltip='Minimise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=os.path.join(self.image_folder, '\\minimise_icon.png'),
                                         key='main_window_minimise_button')

        self.maximise_button = sg.Button(tooltip='Maximise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=os.path.join(self.image_folder, '\\maximise_icon.png'),
                                         key='main_window_maximise_button')

        self.exit_button = sg.Button(tooltip='Close Window', image_subsample=16, image_size=(16, 16),
                                     image_filename=os.path.join(self.image_folder, '\\exit_icon.png'),
                                     button_color='red', key='main_window_exit_button')

        self.console_window = sg.Output(expand_x=True, expand_y=True, echo_stdout_stderr=True,
                                        key='output_screen')

        self.command_prompt = sg.Text(text=('{username}|' + get_root_directory() + '$'), justification='left',
                                      font=('Commodore 64 Angled', '8'), key='command_prompt')

        self.command_arguments = sg.Input(expand_x=True, font=('Commodore 64 Angled', '8'),
                                          background_color=sg.theme_background_color(),
                                          text_color=sg.theme_input_text_color(), do_not_clear=False,
                                          key='command_arguments')

    @staticmethod
    def get_title():
        return 'ASP-T CMD Prompt'

    def set_toolbar_layout(self):
        layout = self.title_text, self.settings_button, self.minimise_button, self.maximise_button, self.exit_button
        return layout

    def set_output_screen(self):
        layout = self.console_window
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
        return sg.Window(title=self.get_title(), layout=self.build_layout(), size=(1000, 700), no_titlebar=True,
                         grab_anywhere=True, keep_on_top=True, modal=True)

    def run_window(self):
        return self.create_window()
