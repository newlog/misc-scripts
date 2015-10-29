#!/usr/bin/env python
import unittest

# The idea is to put the unittests in a 'test' directory in each project 
# folder, placing all the code in their parent folders.
# Given that the tests will be executed using the instruction from the 
# following lines it is required to dynamically import the modules from the
# parent folder
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# from module_to_test_in_parent_folder import something_to_test

# Execute 'python -m unittest discover -v' from project root
# to execute all tests from project

class TestCode(unittest.TestCase):

    def test_func_name__what_to_test(self):
        pass
        #self.assertEqual(var_from_function, 'expected_result')

if __name__ == '__main__':
    unittest.main()
