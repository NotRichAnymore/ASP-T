from src.components.Views.console import Console

from components.command.commandRepository import CommandRepository
from components.command.commandValidator import CommandValidator
from components.command.commandService import CommandService
from components.command.commandController import CommandController

from components.window.windowRepository import WindowRepository
from components.window.windowValidator import WindowValidator
from components.window.windowService import WindowService
from components.window.windowController import WindowController

from components.settings.settingsRepository import SettingsRepository
from components.settings.settingsValidator import SettingsValidator
from components.settings.settingsService import SettingsService
from components.settings.settingsController import SettingsController

from src.components.Utilities.loggingUtilities import LoggingUtilities


def run_program():
    logger = LoggingUtilities()

    settings_repo = SettingsRepository(logger)
    settings_validator = SettingsValidator(logger)
    settings_service = SettingsService(settings_repo, settings_validator, logger)
    settings_controller = SettingsController(settings_service, logger)

    command_repo = CommandRepository(logger)
    command_validator = CommandValidator(logger)
    command_service = CommandService(command_repo, command_validator, logger)
    command_controller = CommandController(command_service)

    window_repo = WindowRepository(logger)
    window_validator = WindowValidator(logger)
    window_service = WindowService(window_repo, window_validator, logger)
    window_controller = WindowController(window_service, logger)
    console = Console(command_controller, window_controller, settings_controller, logger)
    console.run()


def main():
    run_program()


if __name__ == '__main__':
    main()
