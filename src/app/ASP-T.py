from src.components.Views.console import Console

from src.components.Repository.commandRepository import CommandRepository
from src.components.Validator.commandValidator import CommandValidator
from src.components.Services.commandService import CommandService
from src.components.Controllers.commandController import CommandController

from src.components.Controllers.windowController import WindowController

from src.components.Repository.settingsRepository import SettingsRepository
from src.components.Validator.settingsValidator import SettingsValidator
from src.components.Services.settingsService import SettingsService
from src.components.Controllers.settingsController import SettingsController


def run_program():
    settings_repo = SettingsRepository()
    settings_validator = SettingsValidator()
    settings_service = SettingsService(settings_repo, settings_validator)
    settings_controller = SettingsController(settings_service)

    command_repo = CommandRepository()
    command_validator = CommandValidator()
    command_service = CommandService(command_repo, command_validator)
    command_controller = CommandController(command_service)

    window_controller = WindowController()
    console = Console(command_controller, window_controller, settings_controller)
    console.run()


def main():
    run_program()


if __name__ == '__main__':
    main()
