import PySimpleGUI as sg


class SettingsWindow:

    def __init__(self):
        self.title_text = sg.Text(text='ASP-T CMD Prompt: Settings', font=('Commodore 64 Angled', '12'), key='program_title')

        self.settings_button = sg.Button(tooltip='Settings', image_subsample=3, image_size=(16, 16),
                                         image_filename=r'C:\Users\tyres\Documents\ASP-T\src\Images\settings_icon.png',
                                         pad=((660, 0), (0, 0)), key='settings_button')

        self.minimise_button = sg.Button(tooltip='Minimise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=r'C:\Users\tyres\Documents\ASP-T\src\Images\minimise_icon.png',
                                         key='minimise_button')

        self.maximise_button = sg.Button(tooltip='Maximise Window', image_subsample=16, image_size=(16, 16),
                                         image_filename=r'C:\Users\tyres\Documents\ASP-T\src\Images\maximise_icon.png',
                                         key='maximise_button')

        self.exit_button = sg.Button(tooltip='Close Window', image_subsample=16, image_size=(16, 16),
                                     image_filename=r'C:\Users\tyres\Documents\ASP-T\src\Images\exit_icon.png',
                                     key='exit_button')

        self.theme_text = sg.Text('Theme: ')
        self.chosen_theme_text = sg.Text(sg.theme(), key='program_theme')
        self.theme_button = sg.Button(button_text='Change current theme', expand_x=True,
                                      key='program_theme_button')

        self.save_folder = sg.Text('Save Folder: ')
        self.save_folder_input = sg.Input(default_text='', key='save_folder_input')
        self.save_folder_button = sg.Button('Select Folder', expand_x=True, key='select_folder_button')

    @staticmethod
    def get_title():
        return 'ASP-T CMD Prompt (Settings)'

    def set_toolbar_layout(self):
        layout = self.title_text, self.settings_button, self.minimise_button, self.maximise_button, self.exit_button
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
            [self.save_folder_button]
        ]
        layout = sg.Tab('Files', tab_layout, key='files_tab')
        return layout

    def build_tab_group(self):
        layout = sg.TabGroup([
            [self.set_system_tab()],
            [self.set_files_tab()]
        ])
        return layout

    def build_layout(self):
        layout = [
            [self.set_toolbar_layout()],
            [self.build_tab_group()]
        ]
        return layout

    def create_window(self):
        return sg.Window(title=self.get_title(), layout=self.build_layout(), size=(380, 500), no_titlebar=True,
                         grab_anywhere=True, keep_on_top=True, modal=True)


def main():
    sg.theme('SystemDefault')
    main_window = SettingsWindow().create_window()
    while True:
        event, values = main_window.read()
        print(event, values)

if __name__ == '__main__':
    main()