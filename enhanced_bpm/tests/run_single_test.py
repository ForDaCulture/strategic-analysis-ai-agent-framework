#!/usr/bin/env python3
import unittest
import os
import sys

# Add the parent directory to the path so we can import modules from there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the test class
from test_bpm_principles import TestBPMPrinciples

# Run only the maturity models test
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestBPMPrinciples('test_maturity_models'))
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())