# Tests for Car Insights Dashboard

This directory contains tests for the Car Insights Dashboard project.

## Test Structure

The tests are organized by component:

- `webmotors/`: Tests for the Webmotors API client and collector
  - `test_client.py`: Tests for the Webmotors API client
  - `test_collector.py`: Tests for the Webmotors collector
  - `test_check_env.py`: Tests for the environment variable checker

## Running Tests

To run all tests:

```bash
pytest
```

To run tests for a specific component:

```bash
pytest tests/webmotors/
```

To run a specific test file:

```bash
pytest tests/webmotors/test_client.py
```

To run a specific test function:

```bash
pytest tests/webmotors/test_client.py::test_authenticate_success
```

## Test Configuration

The test configuration is defined in `pytest.ini`. This file specifies:

- Test discovery patterns
- Test output format
- Test markers

## Test Fixtures

The tests use pytest fixtures to set up test data and mock objects. These fixtures are defined in the test files and can be reused across multiple tests.

## Mocking

The tests use the `unittest.mock` module to mock external dependencies, such as the Webmotors API. This allows the tests to run without making actual API calls.

## Environment Variables

Some tests use the `monkeypatch` fixture to set and unset environment variables. This allows the tests to run in a controlled environment without affecting the actual environment variables. 