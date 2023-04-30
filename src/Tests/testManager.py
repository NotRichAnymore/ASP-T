import unittest
import os
from pathlib import Path


class TestManager:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent


    def get_test_suites(self):
        scripts = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for file in filenames:
                if '\\src\\Tests\\' in dirpath and 'test' in file:
                    if os.path.exists(os.path.join(dirpath, file)):
                        continue
                    if '.py' == Path(file).suffix:
                        if os.path.join(dirpath, file) not in scripts:
                            scripts.append(os.path.join(dirpath, file))
        return scripts


if __name__ == '__main__':
    TM = TestManager()
    unittest.main(argv=TM.get_test_suites())
