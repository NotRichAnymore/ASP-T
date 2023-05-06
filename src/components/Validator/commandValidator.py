#                      if user_args is None:
#                          valid_user_args = True
#                     case 'date':
#                      if self.valid_date_format(user_args):
#                          valid_user_args = True
#                     case 'sleep':
#                      if self.valid_sleep_format(user_args):
#                          valid_user_args = True
#                     case ['id', 'groups', 'passwd', 'last']:
#                      if user_args in self.get_user_list():
#                          valid_user_args = True
#                     case 'who':
#                      if user_args == 'am i':
#                          valid_user_args = True
#                     case 'ls':
#                      if Path(user_args).is_dir():
#                          valid_user_args = True
#                     case 'cp':
#                      if Path(user_args[0]).exists() and Path(user_args[1]).exists():
#                          valid_user_args = True
#                     case ['rm', 'cat', 'more', 'head', 'less', 'tail']:
#                      if Path(user_args).is_file():
#                          valid_user_args = True
#                     case 'mv':
#                      if (Path(user_args[0]).is_file() and Path(user_args[1]).is_file()) or\
#                              (Path(user_args[0]).is_file() and Path(user_args[1]).is_dir()):
#                          valid_user_args = True
#                     case ['chown', 'chmod']:
#                      if user_args[0] in self.get_permissions_list and \
#                              (Path(user_args[1]).is_file() or Path(user_args[1]).is_file()):
#                          valid_user_args = True
#                     case 'grep':
#                      if isinstance(user_args[0], str) and Path(user_args[1]).is_file():
#                          valid_user_args = True
#                     case 'ln':
#                      if Path(user_args[0]).is_absolute() and isinstance(user_args[1], str):
#                          valid_user_args = True
#                     case ['mkdir', 'rmdir']:
#                      if Path(user_args).is_dir():
#                          valid_user_args = True
#                     case 'ps':
#                      if isinstance(user_args, int):
#                          valid_user_args = True
#                     case 'kill':
#                      if isinstance(user_args[0], int) and isinstance(user_args[1], int):
#                          valid_user_args = True