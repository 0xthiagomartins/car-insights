#!/usr/bin/env python
"""
Script to run tests for the Car Insights Dashboard project.

This script provides a convenient way to run tests with different options.
"""

import argparse
import subprocess
import sys


def main():
    """Run the tests with the specified options."""
    parser = argparse.ArgumentParser(description="Run tests for the Car Insights Dashboard project")
    parser.add_argument(
        "test_path",
        nargs="?",
        default="tests",
        help="Path to the tests to run (default: tests)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Run tests in verbose mode",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        help="Only run tests matching the given keyword",
    )
    parser.add_argument(
        "-m",
        "--marker",
        help="Only run tests matching the given marker",
    )
    parser.add_argument(
        "--cov",
        action="store_true",
        help="Run tests with coverage reporting",
    )
    
    args = parser.parse_args()
    
    # Build the pytest command
    cmd = ["pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    if args.keyword:
        cmd.extend(["-k", args.keyword])
    
    if args.marker:
        cmd.extend(["-m", args.marker])
    
    if args.cov:
        cmd.extend(["--cov=src", "--cov-report=term"])
    
    cmd.append(args.test_path)
    
    # Run the tests
    result = subprocess.run(cmd)
    
    # Return the exit code
    return result.returncode


if __name__ == "__main__":
    sys.exit(main()) 