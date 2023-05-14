from pathlib import Path


class SettingsService:
    def __init__(self, repo, validator):
        self.repository = repo
        self.validator = validator
        self.object_loaded = None

    def create_new_settings_obj(self):
        settings = self.repository.initialise_config_file()
        self.object_loaded = True
        return settings

    def existing_settings_obj(self, path):
        settings = self.repository.get_settings_by_path(path)
        self.object_loaded = True
        return settings

    def present(self, path=None):
        if path:
            return Path(path).exists()
        return False if not self.object_loaded or self.object_loaded is None else True

    def change_current_theme(self, theme):
        return self.repository.set_theme(theme)

    def get_default_theme(self):
        return self.repository.default_theme()

    def get_previous_theme(self):
        return self.repository.get_last_theme()

    def establish_theme(self, new_theme=None):
        current_theme, previous_theme = self.repository.get_themes()
        match current_theme:
            #   program startup previous theme should be none and current theme should be systemdefault
            case current_theme if current_theme is None and previous_theme is None and new_theme is None:
                self.repository.change_theme_order(default=True)
            #   Initial entry to change settings: previous should be none,
            #   should be new_theme and current_theme should be system default
            case current_theme if current_theme == 'SystemDefault' and previous_theme is None and new_theme:
                self.repository.change_theme_order(previous=current_theme, current=new_theme)
            #   any subsequent changes to current theme, swap current theme and previous, current theme now is new_theme
            case current_theme if current_theme and previous_theme and new_theme:
                self.repository.change_theme_order(previous=current_theme, current=new_theme)
            #   if new_theme is none then change to be the last theme
            case current_theme if new_theme is None:
                return current_theme
