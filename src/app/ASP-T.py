from src.components.Views.console import Console


def build_program():
    # repo = commandRepository()
    # validator = commandValidator()
    # service = commandService(repo, validator)
    # controller = commandController(service)
    # console = Console(controller)
    console = Console()
    return console


def run_program(aspt):
    aspt.run()


def main():
    aspt = build_program()
    run_program(aspt)


if __name__ == '__main__':
    main()
