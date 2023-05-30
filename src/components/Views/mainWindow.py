import PySimpleGUI as sg
from src.components.Utilities.utilities import get_root_directory
from pathlib import Path


class MainWindow:

    def __init__(self):
        image_folder = Path('src').resolve().parent.parent.joinpath('data/images').as_posix()
        self.image_folder = image_folder
        self.title_text = sg.Text(text='ASP-T CMD Prompt', background_color=sg.theme_background_color(),
                                  font=('Commodore 64 Angled', '12'), key='program_title_0')

        self.settings_button = sg.Button(tooltip='Settings', image_subsample=3, image_size=(16, 16),
                                         image_filename=Path(image_folder).joinpath('settings_icon.png').as_posix(),
                                         pad=((660, 0), (0, 0)), key='main_window_settings_button_0')

        self.minimise_button = sg.Button(tooltip='Reset Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=Path(image_folder).joinpath('minimise_icon.png').as_posix(),
                                         key='main_window_minimise_button_0')

        self.maximise_button = sg.Button(tooltip='Maximise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=Path(image_folder).joinpath('maximise_icon.png').as_posix(),
                                         key='main_window_maximise_button_0')

        self.exit_button = sg.Button(tooltip='Close Window', image_subsample=16, image_size=(16, 16),
                                     image_filename=Path(image_folder).joinpath('exit_icon.png').as_posix(),
                                     button_color='red', key='main_window_exit_button_0')

        self.console_window = sg.Multiline(expand_x=True, expand_y=True, autoscroll=True, write_only=False,
                                           #reroute_stderr=True,
                                           reroute_stdout=True,
                                           font=('Commodore 64 Angled', '12'), key='output_screen_0')


        self.command_prompt = sg.Text(text=('{username}|' + get_root_directory() + '$'), justification='left',
                                      text_color=sg.theme_text_color(),
                                      background_color=sg.theme_background_color(),
                                      font=('Commodore 64 Angled', '10'), key='command_prompt_0')

        self.command_arguments = sg.Input(expand_x=True, font=('Commodore 64 Angled', '10'),
                                          background_color=sg.theme_background_color(),
                                          text_color=sg.theme_input_text_color(), do_not_clear=False,
                                          key='command_arguments_0')

        self.load_input_button = sg.Button(visible=False, bind_return_key=True, key='load_input_button_0')



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
        layout = self.command_prompt, self.command_arguments, self.load_input_button
        return layout

    def build_layout(self):
        layout = [
            [self.set_toolbar_layout()],
            [self.set_output_screen()],
            [self.set_input_bar()],
            [sg.Sizegrip()]
        ]
        return layout

    def create_window(self):
        return sg.Window(title=self.get_title(), layout=self.build_layout(), size=(1000, 700), no_titlebar=True,
                         grab_anywhere=True, keep_on_top=True, modal=True)

    def create_new_window(self, window_num, new_theme=None, size=None, keep_on_top=None):
        sg.theme(new_theme)
        suffix = '_' + window_num
        new_title = (self.get_title() + suffix)
        new_layout = [
            [sg.Text(text='ASP-T CMD Prompt', font=('Commodore 64 Angled', '12'), key=f'program_title{suffix}'),
             sg.Button(tooltip='Settings', image_subsample=3, image_size=(16, 16),
                       image_filename=Path(self.image_folder).joinpath('settings_icon.png').as_posix(),
                       pad=((660, 0), (0, 0)), key=f'main_window_settings_button{suffix}'),
             sg.Button(tooltip='Reset Window', image_subsample=16, image_size=(16, 16),
                       image_filename=Path(self.image_folder).joinpath('minimise_icon.png').as_posix(),
                       key=f'main_window_minimise_button{suffix}'),
             sg.Button(tooltip='Maximise Window', image_subsample=16, image_size=(16, 16),
                       image_filename=Path(self.image_folder).joinpath('maximise_icon.png').as_posix(),
                       key=f'main_window_maximise_button{suffix}'),
             sg.Button(tooltip='Close Window', image_subsample=16, image_size=(16, 16),
                       image_filename=Path(self.image_folder).joinpath('exit_icon.png').as_posix(),
                       button_color='red', key=f'main_window_exit_button{suffix}')
             ],

            [sg.Multiline(expand_x=True, expand_y=True, autoscroll=True, write_only=False,
                                           #reroute_stderr=True,
                                           reroute_stdout=True,
                                           font=('Commodore 64 Angled', '9'), key=f'output_screen{suffix}')],

            [sg.Text(text=('{guest}|' + get_root_directory() + '$'), justification='left',
                     font=('Commodore 64 Angled', '10'), key=f'command_prompt{suffix}'),
             sg.Input(expand_x=True, font=('Commodore 64 Angled', '10'),
                      background_color=sg.theme_background_color(),
                      text_color=sg.theme_input_text_color(), do_not_clear=False,
                      key=f'command_arguments{suffix}'),
             sg.Button(visible=False, bind_return_key=True, key=f'load_input_button{suffix}')
             ],
            [sg.Sizegrip()]


        ]
        return sg.Window(title=new_title, layout=new_layout, size=(size if size is not None else (1000, 700)),
                         no_titlebar=True, resizable=True, return_keyboard_events=True, grab_anywhere=True,
                         keep_on_top=(keep_on_top if keep_on_top is not None else True), modal=True, finalize=True,
                         use_default_focus=False)

    def run_window(self):
        return self.create_window()
