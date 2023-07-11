import os.path
import unittest
from unittest.mock import patch
from pathlib import Path

import mock

from components.command.commandController import CommandController





class TestFileObjects(unittest.TestCase):
    def setUp(self):
        self.command_controller = CommandController()
        self.controller_instance = mock.MagicMock()


    @patch('src.Controllers.commandController.CommandController')
    def test_file_exists(self, controller_mock):
        self.controller_instance.get_filenames.return_value = ['src/data/files/command_list.json',
                                                               'src/data/files/command_arguments_list.json',
                                                               'src/data/files/command_options_list.json']
        controller_mock.return_value = self.controller_instance

        actual_result = self.command_controller.get_paths()
        expected_result = ['src/data/files/command_list.json', 'src/data/files/command_arguments_list.json',
                           'src/data/files/command_options_list.json']

        for expected_path, actual_path in zip(expected_result, actual_result):
            self.assertEqual(os.path.exists(Path(expected_path).resolve().as_posix()), os.path.exists(actual_path))



    

























if __name__ == '__main__':
    unittest.main()
