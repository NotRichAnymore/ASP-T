import PySimpleGUI as sg
from pathlib import Path

import pysnooper


class SettingsWindow:

    def __init__(self):

        self.preview_themes_suffix = None
        image_folder = Path('src').resolve().parent.parent.joinpath('data/images').as_posix()
        self.image_folder = image_folder
        self.title_text = sg.Text(text='ASP-T CMD Prompt: Settings', font=('Commodore 64 Angled', '12'),
                                  key='settings_window_title_0')

        self.minimise_button = sg.Button(tooltip='Minimise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=Path(image_folder).joinpath('minimise_icon.png').as_posix(),
                                         key='settings_window_minimise_button_0')

        self.maximise_button = sg.Button(tooltip='Maximise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=Path(image_folder).joinpath('maximise_icon.png').as_posix(),
                                         key='settings_window_maximise_button_0')

        self.exit_button = sg.Button(tooltip='Close Window', image_subsample=16, image_size=(16, 16),
                                     image_filename=Path(image_folder).joinpath('exit_icon.png').as_posix(),
                                     button_color='red', key='settings_window_exit_button_0')

        self.theme_text = sg.Text(f'Theme: {sg.theme()}', key='current_theme_text_0')
        self.theme_button = sg.Button(button_text='Change current theme', expand_x=True, key='program_theme_button_0')

        self.save_folder = sg.Text('Save Folder: ')
        self.save_folder_input = sg.Input(default_text='', expand_x=True, key='save_folder_input_0')
        self.save_folder_button = sg.Button('Select Folder', expand_x=True, key='select_folder_button_0')
        self.load_user_details_button = sg.Button('Load User Details', expand_x=True, key='load_user_button_0')

    def get_preview_themes_window_layout(self, suffix, new_theme=None):
        sg.theme(new_theme)
        layout = [
            [sg.Text(f'Current Theme: {sg.theme() if new_theme is None else new_theme}',
                     background_color=sg.theme_background_color())],
            [sg.Text('Here are a list of possible themes', background_color=sg.theme_background_color())],
            [sg.Combo(sg.theme_list(), expand_x=True, default_value=sg.theme() if new_theme is None else new_theme,
                      enable_events=True, key=f'theme_list{suffix}')],
            [sg.Button(button_text='Set current theme', expand_x=True, key=f'set_theme_button{suffix}')],
            [sg.Button('Close', expand_x=True, key=f'close_preview_theme_window{suffix}')]
        ]
        return layout

    @pysnooper.snoop()
    def run_preview_themes_window(self, window_num, new_theme=None):
        sg.theme(new_theme)
        suffix = '_' + str(window_num)
        self.preview_themes_suffix = suffix
        layout = self.get_preview_themes_window_layout(suffix, new_theme)
        window = sg.Window(f'Preview Themes{suffix}', layout, modal=True, keep_on_top=True, no_titlebar=True,
                           grab_anywhere=True)
        while True:
            event, values = window.read()
            if event in f'theme_list{suffix}':
                window.close()
                window_num += 1
                new_suffix = '_' + str(window_num)
                self.preview_themes_suffix = new_suffix
                window = sg.Window(f'Preview Themes{new_suffix}',
                                   self.get_preview_themes_window_layout(self.preview_themes_suffix,
                                                                         values[f'theme_list{suffix}']),
                                   modal=True,
                                   keep_on_top=True,
                                   no_titlebar=True,
                                   grab_anywhere=True)
            if event in f'set_theme_button{self.preview_themes_suffix}':
                window.close()
                return values[f'theme_list{self.preview_themes_suffix}']
            if event in f'close_preview_theme_window{self.preview_themes_suffix}':
                window.close()
                break

    @staticmethod
    def get_title():
        return 'ASP-T CMD Prompt (Settings)'

    def set_toolbar_layout(self):
        layout = self.title_text, self.minimise_button, self.maximise_button, self.exit_button
        return layout

    def set_system_tab(self):
        tab_layout = [
            [self.theme_text],
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

    def create_new_window(self, window_num, new_theme=None):
        sg.theme(new_theme)
        suffix = '_' + window_num
        new_title = (self.get_title() + suffix)
        new_title_layout = sg.Text(text='ASP-T CMD Prompt: Settings', font=('Commodore 64 Angled', '12'),
                                   key=f'settings_window_title{suffix}'), \
            sg.Button(tooltip='Minimise Window', image_subsample=16, image_size=(16, 16),
                      image_filename=Path(self.image_folder).joinpath('minimise_icon.png').as_posix(),
                      key=f'settings_window_minimise_button{suffix}'), \
            sg.Button(tooltip='Maximise Window', image_subsample=16, image_size=(16, 16),
                      image_filename=Path(self.image_folder).joinpath('maximise_icon.png').as_posix(),
                      key=f'settings_window_maximise_button{suffix}'), \
            sg.Button(tooltip='Close Window', image_subsample=16, image_size=(16, 16),
                      image_filename=Path(self.image_folder).joinpath('exit_icon.png').as_posix(),
                      button_color='red', key=f'settings_window_exit_button{suffix}')

        new_files_tab_layout = [
            [sg.Text(f'Theme: {sg.theme()}', key=f'current_theme_text{suffix}')],
            [sg.Button(button_text='Change current theme', expand_x=True,
                       key=f'program_theme_button{suffix}')]
        ]

        new_files_tab = sg.Tab('Files', new_files_tab_layout, key=f'files_tab{suffix}')

        new_system_tab_layout = [
            [sg.Text('Save Folder: ')],
            [sg.Input(default_text='', expand_x=True, key=f'save_folder_input{suffix}')],
            [sg.Button('Select Folder', expand_x=True, key=f'select_folder_button{suffix}')],
            [sg.Button('Load User Details', expand_x=True, key=f'load_user_button{suffix}')]
        ]
        new_system_tab = sg.Tab('System', layout=new_system_tab_layout, key=f'system_tab{suffix}')
        new_tab_layout = [[new_files_tab], [new_system_tab]]
        new_tab_group = sg.TabGroup(new_tab_layout, expand_x=True)

        new_layout = [
            [new_title_layout],
            [new_tab_group]
        ]

        return sg.Window(title=new_title, layout=new_layout, size=(535, 500), no_titlebar=True,
                         grab_anywhere=True, keep_on_top=True, modal=True)

    def run_window(self):
        return self.create_window()
