import logging

from src.components.command.exceptions import InvalidCommandFormatError
from src.components.Utilities.mySQLUtilities import MySQLUtilities
from mysql.connector import Error
import pysnooper
import re
from pathlib import Path


@pysnooper.snoop()
class CommandService:
    def __init__(self, repo, validator, logger):
        self.log_line_num = None
        self.repository = repo
        self.validator = validator
        self.logger = logger
        self.command_name = None
        self.command_args = []
        self.command_opts = []
        self.command = []
        self.command_format = None
        self.datetime_format = None
        self.sql = None

    def establish_command_format(self, command):
        return self.repository.get_command_format(command)

    def determine_command_arguments(self, command, arg_format, tokens):
        args = []
        match command:
            case 'help':
                for token in tokens:
                    if token in self.repository.get_all_commands():
                        return token
            case 'clear' | 'history' | 'date' | 'uptime' | 'log':
                return None
            case 'sleep':
                return tokens
            case 'id':
                try:
                    self.sql = MySQLUtilities(host='127.0.0.1',
                                              username='test_user',
                                              password='test_pass763',
                                              database='aspt')
                except Exception:
                    return 'unable to check id'
                for token in tokens:
                    ids = self.sql.get_all_users_ids()
                    users = self.sql.get_all_users()
                    for i in range(len(ids)):
                        if int(token) == ids[i][0] or token == users[i][0]:
                            return token
            case 'passwd':
                try:
                    self.sql = MySQLUtilities(host='127.0.0.1',
                                              username='test_user',
                                              password='test_pass763',
                                              database='aspt')
                except Exception:
                    return 'unable to change password'
                username_valid = False
                password_valid = False
                max_length = False
                user_details = []
                users = self.sql.get_all_users()
                users_length = len(users)
                while not max_length or not (username_valid and password_valid):
                    for token in tokens:
                        for i in range(users_length):
                            if i == users_length:
                                max_length = True
                                break

                            if token in users[i][0]:
                                user_details.append(token)
                                username_valid = True

                            if username_valid:
                                try:
                                    password = self.sql.query_user_details(user_details)[2][0]
                                    if self.validator.validate_password(token, password):
                                        user_details.append(token)
                                        password_valid = True
                                except Error:
                                    continue

                        if len(user_details) == 2:
                            username_valid, password_valid = True, True
                            break
                        else:
                            continue

                return user_details if len(user_details) == 2 else None
            case 'ls':
                for token in tokens:
                    if self.validator.validate_directory(token):
                        return token
            case 'cp':
                for token in tokens:
                    if self.validator.validate_path(token):
                        args.append(token)
                    elif self.validator.is_pathlike(token) and not token.startswith('-'):
                        args.append(token)
                return args

    def get_options_from_format(self, opt_format, tokens):
        options = []
        for token in tokens:
            if token in opt_format:
                options.append(token)
        return options

    @pysnooper.snoop()
    def determine_command_options(self, command, opt_format, tokens):
        match command:
            case 'help':
                pass
            case 'clear' | 'history' | 'sleep' | 'uptime' | 'passwd':
                return None
            case 'date' | 'id':
                if len(tokens) == 0:
                    return None
                return self.get_options_from_format(opt_format, tokens)
            case 'ls' | 'cp' | 'log':
                return self.get_options_from_format(opt_format, tokens)

    def help_command(self):
        jsonObject = self.repository.get_all_help_command_details()
        jsonObj = self.repository.get_all_command_details()
        for index in range(len(jsonObject)):
            help_command_details = jsonObject[index]
            command_details = jsonObj[index]
            if self.command_args == help_command_details['name'] and self.command_args in command_details['name'] \
                    and self.command_opts is None:
                response = f"Command Name: {help_command_details['name']}\n" \
                           f"Description: {help_command_details['description']}\n" \
                           f"Arguments: {command_details['arguments']}\n" \
                           f"Options: {command_details['options']}\n" \
                           f"Description: {help_command_details['options']}\n"

                return response

    def clear_command(self):
        return self.command_name

    def history_command(self):
        return self.command_name

    def log_command(self):
        if len(self.command_opts) == 0:
            raise InvalidCommandFormatError

        log_contents = None
        match self.command_opts:
            case ['-a' | '-all']:
                log_contents = self.repository.get_log_file_contents(all_lines=True)
            case ['-f' | '--from=']:
                log_contents = self.repository.get_log_file_contents(datestr=self.datetime_format, from_date=True)
            case ['-s' | '--setup']:
                log_contents = self.repository.get_log_file_contents(program_setup=True)
            case ['-l' | '--last=']:
                log_contents = self.repository.get_log_file_contents(line_num=self.log_line_num, last=True)

        return self.command_name, log_contents

    def date_command(self, additional_details):
        timezone, format_string = additional_details[:2]
        if len(self.command) == 1:
            return self.command_name, self.repository.get_current_datetime(timezone, format_string), 'current'

        valid_date_format = self.validator.validate_date_format((self.command_name, self.command_format),
                                                                self.datetime_format)
        output, date_type = None, None
        match self.command_opts:
            case ['-u']:
                output, date_type = self.repository.get_global_datetimes(format_string), 'timezones'
            case ['-u', '--format='] if valid_date_format:
                output, date_type = self.repository.get_global_datetimes(self.datetime_format), 'timezones'
            case ['--format='] if valid_date_format:
                output, date_type = self.repository.get_current_datetime(timezone, self.datetime_format), 'current'
            case ['--format=', '-s'] if valid_date_format:
                output, date_type = self.repository.set_datetime_format(self.datetime_format), 'set time'
            case ['-s' | '--Set='] if valid_date_format:
                output, date_type = self.repository.set_datetime_format(self.datetime_format), 'set time'

        return self.command_name, output, date_type

    def sleep_command(self):
        return self.command_name, self.command_args

    def uptime_command(self, additional_details):
        current_time = additional_details[2]
        return current_time

    def id_command(self):
        if len(self.command) == 1:
            return self.command_name

        name_and_id = self.sql.get_usernames_and_ids()
        for i in range(len(name_and_id)):
            for uid in name_and_id:
                if self.command_args in uid:
                    match uid.index(self.command_args):
                        case 0:
                            return self.sql.get_username_by_id(uid[uid.index(self.command_args)])[0][0]
                        case 1:
                            return self.sql.get_id_by_username(uid[uid.index(self.command_args)])[0][0]
        return 'id not found'

    def passwd_command(self, additional_details):
        if not self.command_args[0] == additional_details[3]:
            return None
        return self.command_name, self.command_args

    def ls_command(self):
        directory_contents = None
        if len(self.command_opts) == 0:
            directory_contents = self.repository.get_directory_contents(self.command_args)

        match self.command_opts:
            case ['-a']:
                directory_contents = self.repository.get_directory_contents(self.command_args, show_hidden=True)
            case ['-l']:
                directory_contents = self.repository.get_directory_contents(self.command_args, directory_details=True)
            case ['-d']:
                directory_contents = self.repository.get_directory_contents(self.command_args, only_directory=True)
            case ['-t']:
                directory_contents = self.repository.get_directory_contents(self.command_args, modification_date=True)
            case ['-r']:
                directory_contents = self.repository.get_directory_contents(self.command_args, in_reverse=True)

        return self.command_name, directory_contents

    def get_cp_options(self):
        backup = None
        force = None
        no_clobber = None
        recursive = None
        remove_dest = None
        suffix = None
        target_directory = None
        no_target_directory = None
        verbose = None

        match self.command_opts:
            case ['-b'] | ['--backup']:
                backup = True
            case ['-f'] | ['--force']:
                force = True
            case ['-n'] | ['--no-clobber']:
                no_clobber = True
            case ['r'] | ['-R'] | ['--recursive']:
                recursive = True
            case ['--remove-destination']:
                remove_dest = True
            case ['-S'] | ['--Suffix=']:
                suffix = True
            case ['t'] | ['--target-directory=']:
                target_directory = True
            case ['-T'] | ['--no-target-directory']:
                no_target_directory = True
            case ['-v'] | ['--verbose']:
                verbose = True

        return backup, force, no_clobber, recursive, remove_dest, \
            suffix, target_directory, no_target_directory, verbose

    def cp_command(self):
        copy_success = None
        src_path = self.command_args[0]
        dest_path = self.command_args[1]

        backup, force, no_clobber, recursive, remove_dest, \
            suffix, target_directory, no_target_directory, verbose = self.get_cp_options()

        match self.validator.check_path_type(self.command_args):
            case ('file', 'file'):
                copy_success = self.repository.copy_path(src_path, dest_path, file_to_file=True,
                                                         backup=backup, force=force, no_clobber=no_clobber,
                                                         remove_dest=remove_dest, suffix=suffix,
                                                         target_directory=target_directory,
                                                         no_target_directory=no_target_directory, verbose=verbose)
            case ('file', 'directory'):
                copy_success = self.repository.copy_path(src_path, dest_path, file_to_directory=True,
                                                         backup=backup, force=force, no_clobber=no_clobber,
                                                         recursive=recursive, remove_dest=remove_dest, suffix=suffix,
                                                         target_directory=target_directory,
                                                         no_target_directory=no_target_directory, verbose=verbose
                                                         )
            case ('directory', 'directory'):
                copy_success = self.repository.copy_path(src_path, dest_path, directory_to_directory=True,
                                                         backup=backup, force=force, no_clobber=no_clobber,
                                                         recursive=recursive, remove_dest=remove_dest, suffix=suffix,
                                                         target_directory=target_directory,
                                                         no_target_directory=no_target_directory, verbose=verbose
                                                         )
            case ('directory', 'file'):
                raise InvalidCommandFormatError(self.command_name, self.command_format)

        return self.command_name, src_path, copy_success, dest_path

    def remove_none_values(self):
        command = []
        for ele in self.command:
            if (isinstance(ele, str) and ele is not None) or (isinstance(ele, list) and len(ele) > 0):
                command.append(ele)
        self.command = command

    def additional_requirements(self):
        match self.command_name:
            case 'date':
                self.remove_none_values()
                return True
            case 'uptime':
                return True
            case 'passwd':
                return True
        return False

    def sort_setter_option(self, tokens):
        for token in tokens:
            try:
                setter_value = token[token.index('=') + 1:]
                setter_opt = token[:token.index('=') + 1]
                i = tokens.index(token)

                match self.command_name:
                    case 'date' | 'log' if re.match(r"(^%[a-zA-Z]|%%)+([-:/._]?%[a-zA-Z]+)*$", setter_value):
                        self.datetime_format = setter_value
                        tokens.remove(token)
                        tokens.insert(i, setter_opt)
                    case 'log' if re.match(r"^\d$", token):
                        self.log_line_num = setter_value
                        tokens.remove(token)
                        tokens.insert(i, setter_opt)
            except (ValueError, IndexError):
                continue

        return tokens

    def has_single_quotes(self, tokens):
        quote_present = False
        for token in tokens:
            if "'" in token:
                quote_present = True

        return quote_present

    def determine_path_order(self, tokens: list) -> tuple[list, list]:
        indices = []
        split_paths = []
        starting_quote_regex = r"^('[a-zA-Z]+\:+\\+)(\\*[a-zA-Z]*)*$"
        split_path_regex = r"^[a-zA-Z]+\\+[a-zA-Z]+[^\']+$"
        ending_quote_regex = r"^([a-zA-Z]+)(\\+[a-zA-Z]+\d*)*(\.+[a-zA-Z]+)*('$)+"
        regexs = [starting_quote_regex, split_path_regex, ending_quote_regex]

        all_tokens_tried = False
        all_regexes_tried = False
        lists_same_length = False
        main_loop = True

        while main_loop:

            token_tries = 0
            for token in tokens:
                # 'Starting loop'

                regex_tries = 0
                for regex in regexs:
                    # 'Trying regex (tries', regex_tries, ')'
                    # f'Does {regex} work for {token}?')
                    if re.match(regex, token) and token not in split_paths:
                        # f'Yes, adding {token} to paths')
                        split_paths.append(token)
                        # f'Also adding {regexs.index(regex)} to indices'
                        indices.append(regexs.index(regex))

                        # len(split_paths), len(indices))
                        if (len(split_paths) and len(indices)) == len(tokens):
                            lists_same_length = True
                            all_tokens_tried = True
                            # 'path order gained'
                            break

                    regex_tries += 1
                    # f'advancing regex tries to {regex_tries}'
                    if regex_tries == len(regexs):
                        all_regexes_tried = True
                        # 'All regexes Tried'
                        break

                if all_regexes_tried:
                    token_tries += 1
                    # f'token tried {token_tries} times'

                    if token_tries == len(tokens) or all_tokens_tried or lists_same_length:
                        # f'all tokens tried = {all_tokens_tried} or lists are same length = {lists_same_length}'
                        main_loop = False
                        break

            if not main_loop:
                break

        return indices, split_paths

    def build_path_from_indices(self, indices: list, split_paths: list) -> list:
        paths = []
        ordered_path = []
        j = 0

        # Using indices to build the quoted path in correlating order
        for i, p in zip(indices, split_paths):

            if i == 0:
                ordered_path.insert(0, p)
                j += 1
            elif i == 1:
                ordered_path.insert(j, p)
                j += 1
            elif i == 2:
                ordered_path.insert(len(ordered_path) + 1, p)
                j = 0

            # Add each ordered_path as a joined string to list
            # Based on if i is ending quote
            # And it's preceded by a starting/middle quote or
            # Followed by a starting quote
            prev_index = indices[indices.index(i) - 1]
            if i == 2 and (prev_index == 0 or prev_index == 1) \
                    or (indices[i + 1] == 0):
                paths.append(' '.join(ordered_path)[1:-1])
                ordered_path = []

        return paths

    def sort_path(self, tokens, opt_format):
        command = tokens[0]
        tokens = tokens[1:]

        if not self.has_single_quotes(tokens):
            return [command] + tokens

        indices, split_paths = self.determine_path_order(tokens)
        paths = self.build_path_from_indices(indices, split_paths)

        path = [command] + paths
        for token in tokens:
            if token in opt_format:
                path += [token]
        return path

    def build(self, tokens):
        self.command_args = self.determine_command_arguments(self.command_name, self.command_format[1], tokens[1:])
        self.command_opts = self.determine_command_options(self.command_name, self.command_format[2], tokens[1:])
        self.command = [self.command_name, self.command_args, self.command_opts]

    def parse(self, tokens):
        self.command_format = self.establish_command_format(tokens[0])
        self.command_name = self.command_format[0]
        match self.command_name:
            case 'date' | 'log':
                tokens = self.sort_setter_option(tokens)
            case 'ls' | 'cp':
                tokens = self.sort_path(tokens, self.command_format[2])
        self.validator.validate_command(tokens, self.command_name, self.command_format)
        self.build(tokens)
        return self.additional_requirements()

    def execute_command(self, additional_details=None):
        match self.command_name:
            case 'help':
                return self.help_command()
            case 'clear':
                return self.clear_command()
            case 'history':
                return self.history_command()
            case 'log':
                return self.log_command()
            case 'date':
                self.remove_none_values()
                return self.date_command(additional_details)
            case 'sleep':
                return self.sleep_command()
            case 'uptime':
                return self.uptime_command(additional_details)
            case 'id':
                self.remove_none_values()
                return self.id_command()
            case 'passwd':
                return self.passwd_command(additional_details)
            case 'ls':
                return self.ls_command()
            case 'cp':
                return self.cp_command()

    def run_command(self, command_statement, additional_details):
        if not self.parse(command_statement.split(' ')):
            return self.execute_command()
        return self.execute_command(additional_details)

    def write_command_response(self, save_folder, command_response=None, clear_file=None):
        save_path = Path(save_folder).joinpath('command_history.json')
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Using {save_path}')

        jsonObj = self.read_command_history(save_folder)
        mode = 'a+'
        if clear_file:
            self.repository.clear_file(save_path)
            self.repository.write_json_object_to_file(save_path, 'w+', command_response)
        else:
            if len(jsonObj[0]) == 0:
                self.repository.write_json_object_to_file(save_path, mode, command_response)
            self.repository.append_json_object_to_file(save_path, command_response)
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Command Response written to {save_path}')

    def read_command_history(self, save_folder):
        save_path = Path(save_folder).joinpath('command_history.json')
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Reading from {save_path}')
        return self.repository.read_json_object_from_file(save_path)
