import json
import os.path
import unittest
import mock
from unittest.mock import patch, mock_open
from pathlib import Path
from src.Utilities.utilities import get_all_json_files, get_json_object_from_file
from src.Controllers.commandController import CommandController





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

    def test_file_is_json(self):
        json_list = get_all_json_files()
        expected_result = isinstance({}, dict)
        actual_result = get_json_object_from_file
        self.assertEqual(expected_result, isinstance(actual_result, dict))

        # def get_json_object_from_file(file_path):
        #     jsonObject = {}
        #     with open(file_path, "r") as file:
        #         for obj in file:
        #             jsonDict = json.loads(obj)
        #             jsonObject = jsonDict
        #     return jsonObject

if __name__ == '__main__':
    unittest.main()
