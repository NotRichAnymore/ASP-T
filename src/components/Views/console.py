from src.components.Views import settingsWindow, mainWindow



class Console:

    def __init__(self, command_controller, window_controller):
        self.command_controller = command_controller
        self.window_controller = window_controller
        self.settings_window = settingsWindow.SettingsWindow()
        self.main_window = mainWindow.MainWindow()


    def execute_command(self, command_arguments):
        command = self.command_controller.load_command(command_arguments)
        return self.command_controller.run_command(command)

    def get_active_window(self):
        return self.window_controller.get_active_window()

    def update_active_window(self, window_to_close, active_window, program_running):
        self.window_controller.update_active_window_(window_to_close, active_window, program_running)

    def end_program(self, main_window):
        main_window.close()
        del [main_window]

    def run_settings_window(self):
        settings_window = self.settings_window.run_window()
        active_window = self.get_active_window()
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
                        self.update_active_window('settings_window', active_window, True)
                        settings_window.close()

    def run(self):
        try:
            # Set main window as the currently running window and gui is currently running
            active_window = self.get_active_window()
            self.update_active_window(None, 'main_window', True)
            # Run the main window
            main_window = self.main_window.run_window()
            while True:
                event, values = main_window.read()
                print(event, values)
                match event:
                    # If Exit button is pressed on the main menu
                    case 'main_window_exit_button':
                        #  update the active window manager
                        self.update_active_window('main_window', None, False)
                        # close and destroy the window
                        self.end_program(main_window)
                        # exit the loop
                        break

                    # If the settings button is pressed on the main menu
                    case 'main_window_settings_button':
                        # update the active window manager for the settings window to be currently running
                        self.update_active_window('main_window', 'settings_window', True)
                        # hide the main menu
                        main_window.hide()
                        # run the settings window
                        self.run_settings_window()
                        # un hide the main menu on settings window completion
                        main_window.un_hide()

                    case 'load_input_button':
                        command_arguments = values['command_arguments']
                        print(command_arguments)
                        print(self.execute_command(command_arguments))


        except Exception as e:
            print(e)
