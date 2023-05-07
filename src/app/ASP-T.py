from src.components.Views.console import Console
from src.components.Repository.commandRepository import CommandRepository
from src.components.Validator.commandValidator import CommandValidator
from src.components.Services.commandService import CommandService
from src.components.Controllers.commandController import CommandController
from src.components.Controllers.windowController import WindowController


def build_program():
    repo = CommandRepository()
    validator = CommandValidator()
    service = CommandService(repo, validator)
    command_controller = CommandController(service)
    window_controller = WindowController()
    console = Console(command_controller, window_controller)
    return console


def run_program(aspt):
    aspt.run()


def main():
    aspt = build_program()
    run_program(aspt)


if __name__ == '__main__':
    main()
