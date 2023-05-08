import PySimpleGUI as sg
from pathlib import Path


class SettingsWindow:

    def __init__(self):
        image_folder = Path('src').resolve().parent.joinpath('data/images').as_posix()
        self.title_text = sg.Text(text='ASP-T CMD Prompt: Settings', font=('Commodore 64 Angled', '12'),
                                  key='settings_window_title')

        self.minimise_button = sg.Button(tooltip='Minimise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=Path(image_folder).joinpath('minimise_icon.png').as_posix(),
                                         key='settings_window_minimise_button')

        self.maximise_button = sg.Button(tooltip='Maximise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=Path(image_folder).joinpath('maximise_icon.png').as_posix(),
                                         key='settings_window_maximise_button')

        self.exit_button = sg.Button(tooltip='Close Window', image_subsample=16, image_size=(16, 16),
                                     image_filename=Path(image_folder).joinpath('exit_icon.png').as_posix(),
                                     button_color='red', key='settings_window_exit_button')

        self.theme_text = sg.Text('Theme: ')
        self.chosen_theme_text = sg.Text(sg.theme(), key='program_theme')
        self.theme_button = sg.Button(button_text='Change current theme', expand_x=True,
                                      key='program_theme_button')

        self.save_folder = sg.Text('Save Folder: ')
        self.save_folder_input = sg.Input(default_text='', expand_x=True, key='save_folder_input')
        self.save_folder_button = sg.Button('Select Folder', expand_x=True, key='select_folder_button')
        self.load_user_details_button = sg.Button('Load User Details', expand_x=True, key='load_user_button')

    @staticmethod
    def preview_themes_layout(theme=None):

        layout = [
            [sg.Text(f'Current Theme: {sg.theme()}', background_color=sg.theme_background_color())],
            [sg.Text('Here are a list of possible themes', background_color=sg.theme_background_color())],
            [sg.Combo(sg.theme_list(), expand_x=True, default_value=sg.theme(theme), enable_events=True,
                      key='theme_list')],
            [sg.Button(button_text='Set current theme', expand_x=True, key='set_theme_button')],
            [sg.Button('Close', expand_x=True, key='close_preview_theme_window')]
        ]
        window = sg.Window('Preview Themes', layout, modal=True, keep_on_top=True, no_titlebar=True, grab_anywhere=True)
        return window

    def run_preview_themes_window(self):
        window = self.preview_themes_layout()
        print('viewing themes')
        while True:
            event, values = window.read()
            if event in 'theme_list':
                window.close()
                window = self.preview_themes_layout(values['theme_list'])
            if event in 'set_theme_button':
                window.close()
                return sg.theme(values['theme_list'])
            if event in 'close_preview_theme_window':
                window.close()
                return sg.theme()

    @staticmethod
    def get_title():
        return 'ASP-T CMD Prompt (Settings)'

    def set_toolbar_layout(self):
        layout = self.title_text, self.minimise_button, self.maximise_button, self.exit_button
        return layout

    def set_system_tab(self):
        tab_layout = [
            [self.theme_text, self.chosen_theme_text],
            [self.theme_button]
        ]
        layout = sg.Tab('System', tab_layout, key='system_tab')
        return layout

    def set_files_tab(self):
        tab_layout = [
            [self.save_folder, self.save_folder_input],
            [self.save_folder_button],
            [self.load_user_details_button]
        ]
        layout = sg.Tab('Files', tab_layout, key='files_tab')
        return layout

    def build_tab_group(self):
        layout = sg.TabGroup([
            [self.set_system_tab()],
            [self.set_files_tab()]
        ], expand_x=True)
        return layout

    def build_layout(self):
        layout = [
            [self.set_toolbar_layout()],
            [self.build_tab_group()]
        ]
        return layout

    def create_window(self, theme=None):
        sg.theme(theme)
        return sg.Window(title=self.get_title(), layout=self.build_layout(), size=(535, 500), no_titlebar=True,
                         grab_anywhere=True, keep_on_top=True, modal=True)

    def run_window(self, theme=None):
        return self.create_window(theme)
