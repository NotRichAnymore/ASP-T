import PySimpleGUI as sg
from pathlib import Path

import pytz

from src.data.files.settings_help import files_tab, system_tab, database_tab
import pysnooper


class SettingsWindow:

    def __init__(self):

        self.preview_themes_suffix = None
        self.preview_timezones_suffix = None
        image_folder = Path('src').resolve().parent.parent.joinpath('data/images').as_posix()
        self.image_folder = image_folder
        self.title_text = sg.Text(text='ASP-T CMD Prompt: Settings', font=('Commodore 64 Angled', '12'),
                                  key='settings_window_title_0')
        self.help_button = sg.Button(tooltip='Settings Help', image_subsample=16, image_size=(16,16),
                                     image_filename=Path(image_folder).joinpath('help_icon.png').as_posix(),
                                     key='settings_window_help_button_0')

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
        self.timezone_title = sg.Text(f'Timezone: '),
        self.timezone_text = sg.Text(key=f'current_timezone_text_0')
        self.timezone_button = sg.Button(button_text='Change Timezone', expand_x=True, key=f'change_timezone_button_0')

        self.save_folder = sg.Text('Save Folder: ')
        self.save_folder_input = sg.Input(default_text='', expand_x=True, key='save_folder_input_0')
        self.save_folder_button = sg.Button('Select Folder', expand_x=True, key='select_folder_button_0')


        self.user_text = sg.Text('Username: ')
        self.password_text = sg.Text('Password: ')
        self.username_input = sg.Input(default_text='', expand_x=True, key='username_input_0')
        self.password_input = sg.Input(default_text='', expand_x=True, password_char='x', key='password_input_0')
        self.load_user_details_button = sg.Button('Login with User Details', expand_x=True, key='login_user_button_0')

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

    def get_timezone_window_layout(self, suffix, current_timezone):
        layout = [
            [sg.Text(f'Current Timezone: {current_timezone}')],
            [sg.Text("A List of Timezones and it's retrospective country")],
            [sg.Combo(pytz.common_timezones, expand_x=True,
                      default_value=current_timezone,
                      enable_events=True, key=f'timezone_list{suffix}')],
            [sg.Button(button_text='Set current timezone', expand_x=True, key=f'set_timezone_button{suffix}')],
            [sg.Button('Close', expand_x=True, key=f'close_preview_timezones_window{suffix}')]
        ]
        return layout

    def run_preview_timezones_window(self, window_num, current_timezone):
        suffix = '_' + str(window_num)
        self.preview_timezones_suffix = suffix
        layout = self.get_timezone_window_layout(suffix, current_timezone)
        window = sg.Window(f'Preview Timezones{suffix}', layout, modal=True, keep_on_top=True, no_titlebar=True,
                           grab_anywhere=True)
        while True:
            event, values = window.read()
            if event in f'timezone_list{suffix}':
                window.close()
                window_num += 1
                new_suffix = '_' + str(window_num)
                self.preview_timezones_suffix = new_suffix
                window = sg.Window(f'Preview Timezones{new_suffix}',
                                   self.get_timezone_window_layout(self.preview_timezones_suffix,
                                                                   values[f'timezone_list{suffix}']),
                                   modal=True,
                                   keep_on_top=True,
                                   no_titlebar=True,
                                   grab_anywhere=True)
            if event in f'set_timezone_button{self.preview_timezones_suffix}':
                window.close()
                return values[f'timezone_list{self.preview_timezones_suffix}']
            if event in f'close_preview_timezones_window{self.preview_timezones_suffix}':
                window.close()
                break


    @pysnooper.snoop()
    def run_select_folder_window(self):
        background_color = sg.theme_input_background_color()
        layout = [
            [sg.Text('Select a folder for saving!', background_color=background_color)],
            [sg.FolderBrowse('Select folder', size=(18, 1), auto_size_button=True, key='folder_input')],
            [sg.Button('Exit', expand_x=True)]
        ]

        window = sg.Window('folder_browser', layout=layout, background_color=background_color,
                           no_titlebar=True, grab_anywhere=True, keep_on_top=True, modal=True)

        while True:
            event, values = window.read()
            if event in 'Exit':
                window.close()
                return None if values['folder_input'] is None else values['folder_input']


    def run_help_window(self, window_num, theme):
        sg.theme(theme)
        suffix = '_' + str(window_num)

        layout = [
            [sg.Text('Settings Help', justification='center')],
            [sg.Text('Files', justification='center')],
            [sg.Multiline(expand_x=True, expand_y=True, key=f'files_output{suffix}', do_not_clear=True,
                          horizontal_scroll=True)],
            [sg.Text('System', justification='center')],
            [sg.Multiline(expand_x=True, expand_y=True, key=f'system_output{suffix}', do_not_clear=True,
                          horizontal_scroll=True)],
            [sg.Text('Database', justification='center')],
            [sg.Multiline(expand_x=True, expand_y=True, key=f'database_output{suffix}', do_not_clear=True,
                          horizontal_scroll=True)],
            [sg.Button('Close', expand_x=True, key=f'settings_help_close{suffix}')]
        ]
        window = sg.Window(f'Settings Help{suffix}', layout, modal=True, keep_on_top=True, no_titlebar=True,
                           grab_anywhere=True, size=(500, 500), finalize=True)
        while True:

            window[f'files_output{suffix}'].update((f"Save Folder: {files_tab['Save Folder']}\n"))
            window[f'system_output{suffix}'].update((f"Theme: {system_tab['Theme']}\n"))
            window[f'database_output{suffix}'].update((f"{database_tab['Database']}\n"
                                                       f"Username: {database_tab['Username']}\n"
                                                       f"Password: {database_tab['Password']}"))
            event, values = window.read()
            if event in f'settings_help_close{suffix}':
                window.close()
                break




    @staticmethod
    def get_title():
        return 'ASP-T CMD Prompt (Settings)'

    def set_toolbar_layout(self):
        layout = self.title_text, self.help_button, self.minimise_button, self.maximise_button, self.exit_button
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
            [self.save_folder_button]
        ]
        layout = sg.Tab('Files', tab_layout, key='files_tab')
        return layout

    def set_database_tab(self):
        tab_layout = [
            [self.user_text, self.username_input],
            [self.password_text, self.password_text],
            [self.load_user_details_button]
        ]
        layout = sg.Tab('Database', tab_layout, key='database_tab')
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
            [self.build_tab_group()],
            [sg.Sizegrip()]
        ]
        return layout

    def create_window(self, theme=None):
        sg.theme(theme)
        return sg.Window(title=self.get_title(), layout=self.build_layout(), size=(535, 500), no_titlebar=True,
                         grab_anywhere=True, keep_on_top=True, modal=True)

    def create_new_window(self, window_num, timezone, new_theme=None):
        sg.theme(new_theme)
        suffix = '_' + window_num
        new_title = (self.get_title() + suffix)
        new_title_layout = sg.Text(text='ASP-T CMD Prompt: Settings', font=('Commodore 64 Angled', '12'),
                                   key=f'settings_window_title{suffix}'), \
            sg.Button(tooltip='Settings Help', image_subsample=16, image_size=(16, 16),
                      image_filename=Path(self.image_folder).joinpath('help_icon.png').as_posix(),
                      key=f'settings_window_help_button{suffix}'), \
            sg.Button(tooltip='Minimise Window', image_subsample=16, image_size=(16, 16),
                      image_filename=Path(self.image_folder).joinpath('minimise_icon.png').as_posix(),
                      key=f'settings_window_minimise_button{suffix}'), \
            sg.Button(tooltip='Maximise Window', image_subsample=16, image_size=(16, 16),
                      image_filename=Path(self.image_folder).joinpath('maximise_icon.png').as_posix(),
                      key=f'settings_window_maximise_button{suffix}'), \
            sg.Button(tooltip='Close Window', image_subsample=16, image_size=(16, 16),
                      image_filename=Path(self.image_folder).joinpath('exit_icon.png').as_posix(),
                      button_color='red', key=f'settings_window_exit_button{suffix}'), \
            sg.Button(visible=False, bind_return_key=True, key=f'load_save_folder_button{suffix}')

        new_files_tab_layout = [
            [sg.Text('Save Folder: '),
             sg.Input(default_text='', expand_x=True, key=f'save_folder_input{suffix}')],
            [sg.Button('Select Folder', expand_x=True, key=f'select_folder_button{suffix}')]
        ]
        new_files_tab = sg.Tab('Files', new_files_tab_layout, key=f'files_tab{suffix}')

        new_system_tab_layout = [
            [sg.Text(f'Theme: {sg.theme()}', key=f'current_theme_text{suffix}')],
            [sg.Button(button_text='Change current theme', expand_x=True,
                       key=f'program_theme_button{suffix}')],
            [sg.Text('Timezone: ', key=f'current_timezone_text{suffix}'),
             sg.Text(f'{timezone}', key=f'current_timezone_text{suffix}')],
            [sg.Button(button_text='Change Timezone', expand_x=True,
                       key=f'change_timezone_button{suffix}')]
        ]
        new_system_tab = sg.Tab('System', layout=new_system_tab_layout, key=f'system_tab{suffix}')

        new_database_tab_layout = [
            [sg.Text('Username: '), sg.Input(default_text='', expand_x=True, key=f'username_input{suffix}')],
            [sg.Text('Password: '), sg.Input(default_text='', expand_x=True, password_char='X',
                                             key=f'password_input{suffix}')],
            [sg.Button('Login with User Details', expand_x=True, key=f'login_user_button{suffix}')]
        ]
        new_database_tab = sg.Tab('Database', layout=new_database_tab_layout, key=f'database_tab{suffix}'
                                  )
        new_tab_layout = [[new_files_tab], [new_system_tab], [new_database_tab]]
        new_tab_group = sg.TabGroup(new_tab_layout, expand_x=True)

        new_layout = [
            [new_title_layout],
            [new_tab_group],
            [sg.Sizegrip()]
        ]

        return sg.Window(title=new_title, layout=new_layout, size=(535, 500), no_titlebar=True,
                         grab_anywhere=True, keep_on_top=True, modal=True, resizable=True)

    def run_window(self):
        return self.create_window()
