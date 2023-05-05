from src.Views import mainWindow, settingsWindow
from src.Models.Windows import windowManager
import PySimpleGUI as sg
import pysnooper as ps


class MainController:

    def __init__(self):
        self.window_manager = windowManager.WindowManager()

    def run_settings_window(self):
        settings_window = settingsWindow.SettingsWindow().run_window()
        window_manager = self.window_manager
        active_window = window_manager.get_active_window()
        # Until the settings window isn't the active window
        while active_window == 'settings_window':
            event, values = settings_window.read()
            print(event, values)

            match event:
                # if the exit button is pressed on the settings menu
                case 'settings_window_exit_button':
                    # update the active window manager for the settings window to be closing
                    active_window = 'main_window'
                    if active_window != 'settings_window':
                        window_manager.update_window_manager('settings_window', active_window, True)
                        settings_window.close()

    def run(self):
        try:
            window_manager = self.window_manager
            # Set main window as the currently running window and gui is currently running
            active_window = window_manager.get_active_window()
            window_manager.update_window_manager(None, 'main_window', True)
            # Run the main window
            main_window = mainWindow.MainWindow().run_window()
            while True:
                event, values = main_window.read()
                print(event, values)
                match event:
                    # If Exit button is pressed on the main menu
                    case 'main_window_exit_button':
                        #  update the active window manager
                        window_manager.update_window_manager('main_window', None, False)
                        # close and destroy the window
                        main_window.close()
                        del[main_window]
                        # exit the loop
                        break

                    # If the settings button is pressed on the main menu
                    case 'main_window_settings_button':
                        # update the active window manager for the settings window to be currently running
                        window_manager.update_window_manager('main_window', 'settings_window', True)
                        # hide the main menu
                        main_window.hide()
                        # run the settings window
                        self.run_settings_window()
                        # un hide the main menu on settings window completion
                        main_window.un_hide()

                    case 'load_input_button':
                        command_arguments = values['command_arguments']
                        print(command_arguments)

        except Exception as e:
            print(e)
