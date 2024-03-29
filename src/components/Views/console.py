import logging
import sys
import traceback
import pysnooper
import PySimpleGUI as sg
import pytz
import time

from src.components.Views import settingsWindow, mainWindow, systemTray
from src.data.files.custom_themes import custom_themes
from src.components.Utilities.loggingUtilities import LoggingUtilities
from src.components.Utilities.utilities import is_iterable
from pathlib import Path


@pysnooper.snoop()
class Console:

    def __init__(self, command_controller, window_controller, settings_controller, logger):
        self.username = None
        self.passwd_command = None
        self.prompt_line = None
        self.save_folder = None
        self.command_controller = command_controller
        self.window_controller = window_controller
        self.settings_controller = settings_controller
        self.theme = None
        self.settings = None
        self.themes = None
        self.custom_themes = custom_themes
        self.main_window_keys = None
        self.suffix = None
        self.main_window_num = 0
        self.settings_window_num = 0
        self.preview_theme_window_num = 0
        self.help_window_num = 0
        self.preview_timezone_window_num = 0
        self.max_window_size = False
        self.min_window_size = False
        self.window_size = None
        self.change_password = None
        self.logger = logger

    def initialise_themes(self):
        self.logger.create_log_entry(level=logging.CRITICAL, message='Initialising Themes')
        for name, theme in zip(self.custom_themes.keys(), self.custom_themes.values()):
            sg.theme_add_new(name, theme)
            self.logger.create_log_entry(level=logging.DEBUG, message=f'Adding Theme: {name}')
        self.logger.create_log_entry(level=logging.CRITICAL, message='Themes set')

    
    def load_settings(self, default_path=False, path=None):
        self.logger.create_log_entry(level=logging.CRITICAL, message='Loading Settings')
        self.settings = self.settings_controller.load_settings(default_path, path)
        self.logger.create_log_entry(level=logging.CRITICAL, message='Settings loaded')

    def establish_current_theme(self, theme=None):
        # If a theme has been chosen update current and previous theme
        # Send the current theme for updating
        # Change the current one, only if a new theme has been chosen
        if theme:
            self.logger.create_log_entry(level=logging.CRITICAL, message='Setting New Theme')
            new_theme = self.settings_controller.manage_theme(theme)
            self.theme = new_theme
        # otherwise return the current theme
        self.logger.create_log_entry(level=logging.CRITICAL, message='Getting Current Theme')
        return self.theme
    
    def establish_save_folder(self, save_folder=None):
        if save_folder:
            updated_settings = self.settings_controller.manage_save_folder(save_folder)
            self.logger.create_log_entry(level=logging.CRITICAL, message='Save Folder Updated')
            self.save_folder = updated_settings['Files']['save_folder']
            self.settings = updated_settings
            self.logger.create_log_entry(level=logging.CRITICAL, message='Settings Updated')
        return self.settings_controller.manage_save_folder()

    def establish_timezone(self, timezone=None):
        if timezone:
            updated_settings = self.settings_controller.manage_timezone(timezone)
            self.logger.create_log_entry(level=logging.CRITICAL, message='Timezone Updated')
            self.save_folder = updated_settings['Files']['timezone']
            self.settings = updated_settings
            self.logger.create_log_entry(level=logging.CRITICAL, message='Settings Updated')

        return self.settings_controller.manage_timezone()


    def establish_user_variables(self, username=None, password=None, check_active_user=None, change_password=None):

        if username and password:
            if not change_password:
                self.logger.create_log_entry(level=logging.CRITICAL, message=f'Setting User Details')
                success = self.settings_controller.manage_user_credentials(username, password)

                self.logger.create_log_entry(level=logging.CRITICAL,
                                             message=f'User Details created: '
                                                     f'{success if success is not None else False}')

            success = self.settings_controller.manage_user_credentials(username, password, change_password)
            if success:
                return username

        if check_active_user:
            return self.settings_controller.manage_user_credentials(username=username,
                                                                    check_active_user=check_active_user)


    def establish_prompt_line(self, username=None, prompt_line=None):
        # Change the prompt line if either param is present
        if username or prompt_line:
            # if changing the prompt line based on username
            if username is not None:
                # ensure that username is the active user
                if not self.settings_controller.manage_user_credentials(username, check_active_user=True):
                    # otherwise raise exception
                    return False
            # in case of username, prompt_line is none so settings is checked for the prompt line
            # (changed after user has been loaded)
            # in case of defined prompt line, prior check has been passed (program startup) and defined prompt line used
            self.prompt_line = self.settings_controller.manage_prompt_line(prompt_line)

        self.logger.create_log_entry(level=logging.CRITICAL, message='Getting prompt line')
        return self.prompt_line

    def establish_datetime_format(self, fmt=None):
        if not fmt:
            return self.settings_controller.manage_datetime_format()
        return self.settings_controller.manage_datetime_format(fmt)

    def system_sleep(self, amount):
        self.logger.create_log_entry(level=logging.CRITICAL, message=f'Program sleeping for {amount}')
        if is_iterable(amount):
            for ele in amount:
                time.sleep(int(ele))
        self.logger.create_log_entry(level=logging.CRITICAL, message=f'Program slept for {amount}')

    def establish_runtime(self, startup=None, current=None):
        return self.settings_controller.manage_runtime(startup, current)

    def execute_command(self, command_arguments):
        additional_parameters = [self.establish_timezone(),
                                 self.establish_datetime_format(),
                                 self.establish_runtime(current=True),
                                 self.establish_user_variables(check_active_user=True)
                                 ]
        return self.command_controller.execute_command(command_arguments, additional_parameters)

    def manage_response(self, command_args, response, window):
        try:
            if response is None:
                return 'continue'
            elif response == 'clear':
                window[f'output_screen{self.suffix}'].update(' ')
                self.log_command(command_args, write=True)

            elif response[0] == 'date':
                match response[2]:
                    case 'current':
                        window[f'output_screen{self.suffix}'].print(response[1])
                        self.log_command(command_args, response[1], write=True)
                    case 'timezones':
                        for line in response[1]:
                            window[f'output_screen{self.suffix}'].print(line)
                            self.log_command(command_args, line, write=True)
                    case 'set time':
                        window[f'output_screen{self.suffix}'].print(self.establish_datetime_format(response[1]))
                        self.log_command(command_args, response[1], write=True)
                return 'continue'
            elif is_iterable(response) and response[0] == 'sleep':
                self.log_command(command_args, response, write=True)
                self.system_sleep(response[1])
                response = ''

            elif response == 'history':
                jsonObject = self.log_command(read=True)
                for obj in jsonObject:
                    window[f'output_screen{self.suffix}'].print("Input: ", obj['Input'], text_color='Green')
                    window[f'output_screen{self.suffix}'].print("Output: ", obj['Output'], text_color='Dark Red')
                return 'continue'

            elif response[0] == 'log':
                for i, line in zip(range(len(response[1])), response[1]):
                    if i % 2:
                        colour = 'Dark Blue'
                    else:
                        colour = 'Blue'
                    window[f'output_screen{self.suffix}'].print(line, text_color=colour)
                    self.log_command(command_args, line, write=True)
                return 'continue'

            elif response == 'id':
                response = self.establish_user_variables(check_active_user=True)
                self.log_command(command_args, response, write=True)

            elif is_iterable(response) and response[0] == 'passwd':
                if response[1] is not None:
                    self.change_password = True
                    self.passwd_command = True
                    self.username = response[1]
                    return 'continue'
                response = ''

            elif response[0] == 'ls':
                response = response[1:]
                response = response[0]
                for i in range(len(response)):
                    self.log_command(command_args, response[i]['data'], write=True)
                    match response[i]['type']:
                        case "directory":
                            for directory in response[i]['data']:
                                window[f'output_screen{self.suffix}'].print(directory, text_color=response[i]['colour'])
                        case "files":
                            for file in response[i]['data']:
                                window[f'output_screen{self.suffix}'].print(file, text_color=response[i]['colour'])
                        case "hidden_files":
                            for hidden_file in response[i]['data']:
                                if response[i]['data'] != '':
                                    window[f'output_screen{self.suffix}'].print(hidden_file,
                                                                                text_color=response[i]['colour'])
                return 'continue'

            elif response[0] == 'cp':
                response = response[1:]
                if response[1]:
                    copy_success = f'{response[0]} was copied to {response[2]} successfully'
                    response = copy_success
                    window[f'output_screen{self.suffix}'].print(copy_success, text_color='Green')
                elif not response[1]:
                    copy_fail = f'Failed to remove {response[0]} to {response[2]}'
                    response = copy_fail
                    window[f'output_screen{self.suffix}'].print(copy_fail, text_color='Dark Red')

                self.log_command(command_args, response, write=True)
                return 'continue'
            
            elif response[0] == 'rm':
                response = response[1:]
                if response[1]:
                    remove_success = f'{response[0]} was removed  successfully'
                    response = remove_success
                    window[f'output_screen{self.suffix}'].print(remove_success, text_color='Green')
                elif not response[1]:
                    remove_fail = f'Failed to remove {response[0]}'
                    response = remove_fail
                    window[f'output_screen{self.suffix}'].print(remove_fail, text_color='Dark Red')

                self.log_command(command_args, response, write=True)
                return 'continue'
                    

            elif isinstance(response, list):
                for line in response:
                    print(line)
                    self.log_command(command_args, line, write=True)
                return 'continue'

            self.log_command(command_args, response, write=True)
            print(response)
            print('\n')
        except Exception:
            print(f"'{command_args}' cannot be recognised as a valid command")

    def log_command(self, command_args=None, response=None, write=None, read=None, startup=None):
        command_response = [{"Input": command_args, "Output": response}]
        return self.command_controller.save_command_response(command_response,
                                                             self.establish_save_folder(),
                                                             write,
                                                             read,
                                                             startup)

    def get_active_window(self):
        self.logger.create_log_entry(level=logging.CRITICAL, message='Getting active window')
        return self.window_controller.get_active_window()

    def update_active_window(self, window_to_close, active_window, program_running=None):
        self.logger.create_log_entry(level=logging.CRITICAL, message='Updating active window')
        self.window_controller.update_active_window_(window_to_close, active_window, program_running)

    def reset_window_size(self, window, values):
        self.window_controller.save_console_output(self.settings, values[f'output_screen{self.suffix}'])
        window.close()
        return True, True, False

    @staticmethod
    def end_program(main_window):
        main_window.close()
        del [main_window]

    def program_setup(self):
        self.logger.start_logger()
        self.logger.create_log_entry(level=logging.CRITICAL, message='Starting Program Setup')
        self.load_settings(default_path=True)
        self.initialise_themes()
        settings = self.settings
        current_theme_from_file = settings['System']['current_theme']
        self.establish_current_theme(current_theme_from_file)
        current_timezone = pytz.timezone(settings['System']['timezone'])
        self.establish_timezone(current_timezone)
        current_prompt_line = settings['System']['prompt_line']
        self.establish_prompt_line(prompt_line=current_prompt_line)
        self.establish_runtime(startup=True)
        self.log_command(startup=True)
        # Set main window as the currently running window and gui is currently running
        self.update_active_window(None, 'main_window', True)
        self.logger.create_log_entry(level=logging.CRITICAL, message='Ending Program Setup')
    
    def run_settings_window(self):
        settings = self.settings
        settings_window_ = settingsWindow.SettingsWindow()
        window = settings_window_.create_new_window(window_num=str(self.settings_window_num),
                                                    timezone=self.establish_timezone(),
                                                    current_user=self.establish_user_variables(check_active_user=True),
                                                    save_folder=self.establish_save_folder())
        # Until the settings window isn't the active window
        active_window = self.get_active_window()
        try:
            while active_window == 'settings_window':
                event, values = window.read()
                print(event, values)
                sg.theme(self.establish_current_theme())
                self.suffix = "_" + str(self.settings_window_num)
                # if the exit button is pressed on the settings menu
                if event == f'settings_window_exit_button{self.suffix}':
                    # update the active window manager for the settings window to be closing
                    self.update_active_window('settings_window', 'main_window', True)
                    if self.get_active_window() != 'settings_window':
                        window.close()
                        break

                elif event == f'settings_window_help_button{self.suffix}':
                    settings_window_.run_help_window(self.help_window_num, self.establish_current_theme())

                elif event == f'program_theme_button{self.suffix}':
                    updated_theme = settings_window_.run_preview_themes_window(self.preview_theme_window_num,
                                                                               self.establish_current_theme())
                    self.establish_current_theme(updated_theme)
                    self.settings_window_num += 1
                    window.close()
                    window = settings_window_.create_new_window(window_num=str(self.settings_window_num),
                                                                new_theme=self.establish_current_theme())

                elif event == f'change_timezone_button{self.suffix}':
                    new_timezone = settings_window_.run_preview_timezones_window(window_num=
                                                                                 self.preview_timezone_window_num,
                                                                                 current_timezone=
                                                                                 self.establish_timezone())
                    self.establish_timezone(new_timezone)
                    self.settings_window_num += 1
                    window.close()
                    window = settings_window_.create_new_window(window_num=str(self.settings_window_num),
                                                                new_theme=self.establish_current_theme(),
                                                                timezone=self.establish_timezone())

                elif event == f'load_save_folder_button{self.suffix}':
                    success = True
                    save_folder = values[f'save_folder_input{self.suffix}']
                    self.establish_save_folder(save_folder)
                    if self.save_folder is None or self.save_folder == save_folder:
                        success = False
                    sg.popup_timed(f'Save Folder Changed: {success}?', keep_on_top=True)

                elif event == f'select_folder_button{self.suffix}':
                    save_folder = settings_window_.run_select_folder_window()
                    self.establish_save_folder(save_folder)
                    window[f'save_folder_input{self.suffix}'].update(self.save_folder)

                elif event == f'login_user_button{self.suffix}':
                    username = self.establish_user_variables(values[f'username_input{self.suffix}'],
                                                             values[f'password_input{self.suffix}'])
                    self.establish_prompt_line(username)

        except Exception as e:
            window.close()
            del[window]

    
    def run(self):
        # Setup Program
        self.program_setup()
        reload_contents = False
        reload_window = False

        # Load System Tray
        # system_tray = systemTray.SystemTray()
        # system_tray.create_system_tray_thread()

        # Setup Window variables
        main_window = mainWindow.MainWindow()
        sg.theme(self.establish_current_theme())
        window = main_window.create_new_window(window_num='0',
                                               new_theme=self.establish_current_theme())

        main_loop = True
        while main_loop:
            try:
                if reload_window:
                    self.main_window_num += 1
                    self.logger.create_log_entry(level=logging.DEBUG, message='Creating New Window')
                    window = main_window.create_new_window(window_num=str(self.main_window_num),
                                                           new_theme=self.establish_current_theme())
                    reload_window = False
                    
                self.suffix = "_" + str(self.main_window_num)

                if not main_loop:
                    self.logger.create_log_entry(level=logging.ERROR, message='Closing Program')
                    break

                window[f'command_prompt{self.suffix}'].update(self.establish_prompt_line())
                window.bind('<F7>', f'reset_window_size_button{self.suffix}')

                run_event_loop = True
                while run_event_loop:
                    self.logger.create_log_entry(level=logging.DEBUG, message='Starting Main Program')

                    if self.main_window_num > 0 and reload_contents:
                        for line in self.window_controller.load_console_output():
                            print(line.rstrip())
                        reload_contents = False

                    if self.change_password:
                        print('New Password: ')
                        self.change_password = False


                    event, values = window.read()
                    # print(event, values)
                    # If Exit button is pressed on the main menu
                    if event == f'main_window_exit_button{self.suffix}':
                        #  update the active window manager
                        self.update_active_window('main_window', None, False)
                        # close and destroy the window
                        self.end_program(window)
                        # exit the loop
                        run_event_loop = False
                        main_loop = False

                    # If the settings button is pressed on the main menu
                    elif event == f'main_window_settings_button{self.suffix}':
                        # update the active window manager for the settings window to be currently running
                        self.update_active_window('main_window', 'settings_window', True)
                        # save the console for reloading, run settings
                        # regardless of the output, reload console
                        if self.get_active_window() == 'settings_window':
                            self.window_controller.save_console_output(self.settings,
                                                                       values[f'output_screen{self.suffix}'])
                            window.close()
                            self.run_settings_window()
                            reload_contents = True
                            reload_window = True
                            run_event_loop = False

                    elif event == f'main_window_minimise_button{self.suffix}':
                        reload_contents, reload_window, run_event_loop = self.reset_window_size(window, values)

                    elif event == f'main_window_maximise_button{self.suffix}':
                        while True:
                            if self.max_window_size:
                                window.normal()
                                self.max_window_size = False
                                break
                            window.maximize()
                            self.max_window_size = True
                            break

                    elif event == f'reset_window_size_button{self.suffix}':
                        reload_contents, reload_window, run_event_loop = self.reset_window_size(window, values)

                    elif event == f'load_input_button{self.suffix}':
                        command_arguments = values[f'command_arguments{self.suffix}']
                        print(command_arguments)
                        if self.passwd_command:
                            self.establish_user_variables(self.username, command_arguments, change_password=True)

                        response = self.execute_command(command_arguments)
                        if self.manage_response(command_arguments, response, window) == 'continue':
                            continue
                    if not run_event_loop:
                        break

            except Exception as e:
                sg.popup_error(e.with_traceback(traceback.print_exc(file=sys.stdout)),
                               auto_close=True, auto_close_duration=0.01)
                continue
                # sg.popup_error(e.with_traceback(traceback.print_exc(file=sys.stdout)), keep_on_top=True)
                # self.settings_controller.get_previous_theme()
                #     if self.theme is None else self.settings_controller.get_current_theme()
