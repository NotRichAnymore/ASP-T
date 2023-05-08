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


def build_command_components():
    repo = CommandRepository()
    validator = CommandValidator()
    service = CommandService(repo, validator)
    controller = CommandController(service)
    return controller


def build_settings_components():
    repo = SettingsRepository()
    validator = SettingsValidator()
    service = SettingsService(repo, validator)
    controller = SettingsController(service)
    return controller


def build_window_components():
    controller = WindowController()
    return controller


def build_program():
    settings_controller = build_settings_components()
    command_controller = build_command_components()
    window_controller = build_window_components()
    console = Console(command_controller, window_controller, settings_controller)
    return console


def run_program(aspt):
    aspt.run()


def main():
    aspt = build_program()
    run_program(aspt)


if __name__ == '__main__':
    main()
