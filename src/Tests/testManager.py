import sys
import unittest
import os
from pathlib import Path
import pysnooper
import importlib.util as implib_util
import importlib as implib

class TestManager:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent

    # @pysnooper.snoop()
    def get_test_suites_modules(self):
        scripts = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for file in filenames:
                if '\\src\\Tests' in dirpath:
                    if not os.path.exists(os.path.join(dirpath, file)):
                        continue

                    if '.py' == Path(file).suffix and file != 'testManager.py':
                        if os.path.join(dirpath, file) not in scripts:
                            scripts.append(os.path.join(dirpath, file))

        return scripts

    @pysnooper.snoop()
    def controller_suites(self):
        test_suite = unittest.TestSuite()
        controller_suites = self.get_test_suites_modules()
        for suite_path in controller_suites:
            suite_name = Path(suite_path).name

            spec = implib_util.spec_from_file_location(suite_name, suite_path)
            module = implib_util.module_from_spec(spec)
            spec.loader.exec_module(module)

            module_contents = dir(module)
            classes = [getattr(module, ele) for ele in module_contents if ele.startswith('Test')]

            main_class = classes[0]
            sub_classes = classes[1:]
            # for sub_class in sub_classes:
            #    print(dir(sub_class))

            # print(main_class, sub_classes)
            # test_suite.addTest()
            # .get_test_cases()
            # and Path(suite_name).stem.lower() in ele.lower()

        return test_suite

if __name__ == '__main__':
    TM = TestManager()
    print(TM.controller_suites())
    # unittest.main(argv=TM.get_test_suites())
