# BPM Principles Tests

This directory contains unit tests for the BPM principles JSON data.

## Running the Tests

You can run the tests using the provided `run_tests.py` script:

```bash
python run_tests.py
```

Or you can use the standard unittest module:

```bash
python -m unittest discover
```

To run a specific test, you can use the `run_single_test.py` script (modify it to specify which test to run):

```bash
python run_single_test.py
```

## Test Coverage

The tests validate:

1. **JSON Structure**: Ensures the JSON has all expected top-level keys
2. **Core Principles**: Validates the structure and content of core principles
3. **Methodologies**: Checks the structure and content of methodologies
4. **Frameworks**: Verifies the structure and content of frameworks
5. **Maturity Models**: Ensures maturity models have the correct structure
6. **Performance Metrics**: Validates the structure of performance metrics
7. **Implementation Best Practices**: Checks the structure of implementation best practices
8. **Common Challenges**: Verifies the structure of common challenges
9. **Technology Enablers**: Ensures technology enablers have the correct structure
10. **JSON Validity**: Checks that the JSON is properly formatted
11. **Cross References**: Ensures there are no duplicate names within each category

## Notes on Maturity Models

The test for maturity models accommodates different structures:
- Some models (like CMMI and BPMM) have levels with both 'level' and 'name' fields
- Other models (like PEMM) have levels with only a 'level' field and no 'name' field
- The test validates that either 'level' or 'name' is present, but doesn't require both

## Adding New Tests

To add new tests, create a new test file with the prefix `test_` or add methods to the existing test file. All test methods should start with `test_`.