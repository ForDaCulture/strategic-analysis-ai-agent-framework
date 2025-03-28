#!/usr/bin/env python3
import unittest
import os
import sys
import importlib.util

# Get the absolute path to the test file
current_dir = os.path.dirname(os.path.abspath(__file__))
test_file_path = os.path.join(current_dir, 'tests', 'test_bpm_principles.py')

# Load the test module
spec = importlib.util.spec_from_file_location("test_bpm_principles", test_file_path)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

# Run the tests
if __name__ == '__main__':
    # Create a test suite with all tests from the TestBPMPrinciples class
    suite = unittest.TestLoader().loadTestsFromTestCase(test_module.TestBPMPrinciples)
    
    # Run the tests with verbose output
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Print a summary
    print("\nTest Summary:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())