from src.components.Views.console import Console

from src.components.command.Repository.commandRepository import CommandRepository
from src.components.command.Validator.commandValidator import CommandValidator
from src.components.command.Services.commandService import CommandService
from src.components.command.Controllers.commandController import CommandController

from src.components.window.Controllers.windowController import WindowController

from src.components.settings.Repository.settingsRepository import SettingsRepository
from src.components.settings.Validator.settingsValidator import SettingsValidator
from src.components.settings.Services.settingsService import SettingsService
from src.components.settings.Controllers.settingsController import SettingsController

from src.components.Utilities.loggingUtilities import LoggingUtilities


def run_program():
    logger = LoggingUtilities()

    settings_repo = SettingsRepository(logger)
    settings_validator = SettingsValidator(logger)
    settings_service = SettingsService(settings_repo, settings_validator, logger)
    settings_controller = SettingsController(settings_service, logger)

    command_repo = CommandRepository()
    command_validator = CommandValidator()
    command_service = CommandService(command_repo, command_validator)
    command_controller = CommandController(command_service)

    window_controller = WindowController(logger)
    console = Console(command_controller, window_controller, settings_controller, logger)
    console.run()


def main():
    run_program()


if __name__ == '__main__':
    main()
