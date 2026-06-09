#!/usr/bin/env python3
"""
run_tests.py — Test runner for the TDD-with-LLM workflow.

Usage:
    python run_tests.py                        # Run all tests
    python run_tests.py --component <name>     # Run tests for one component
    python run_tests.py --verbose              # Run all tests with verbose output
    python run_tests.py --component <name> --verbose

Examples:
    python run_tests.py --component replay_buffer
    python run_tests.py --verbose
"""

import argparse
import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).parent / "tests"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run pytest tests for the project."
    )
    parser.add_argument(
        "--component",
        type=str,
        default=None,
        help="Name of the component to test (e.g. 'replay_buffer' runs 'tests/test_replay_buffer.py')",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Run pytest with verbose output (-v flag)",
    )
    return parser.parse_args()


def resolve_test_target(component: str | None) -> str:
    """Return the pytest target: a specific test file or the whole tests directory."""
    if component is None:
        return str(TESTS_DIR)

    test_file = TESTS_DIR / f"test_{component}.py"
    if not test_file.exists():
        print(f"Error: no test file found for component '{component}'.")
        print(f"Expected: {test_file}")
        sys.exit(1)

    return str(test_file)


def run(target: str, verbose: bool) -> int:
    cmd = ["pytest", target]
    if verbose:
        cmd.append("-v")

    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    args = parse_args()
    target = resolve_test_target(args.component)
    exit_code = run(target, args.verbose)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
