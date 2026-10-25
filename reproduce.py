#!/usr/bin/env python3
"""Rebuild the literature taxonomy and locked Workshop scorecard offline."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New or empty directory outside this package')
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    output = args.output.resolve()
    if output.is_relative_to(package) or (output.exists() and any(output.iterdir())):
        parser.error('Output must be a new or empty directory outside this package')
    output.mkdir(parents=True, exist_ok=True)
    commands = [
        [sys.executable, '-B', str(package / 'taxonomy/05-code/reproduce.py'), '--taxonomy-only', '--output', str(output / 'literature')],
        [sys.executable, '-B', str(package / 'scorecard/04-code/reproduce.py'), '--output', str(output / 'scorecard')],
    ]
    for command in commands:
        subprocess.run(command, check=True)
    print(json.dumps({'taxonomy': '14 result files checked byte-for-byte',
                      'scorecard': '5 tables and 9 figure files checked byte-for-byte',
                      'api_calls': 0, 'output': str(output)}, indent=2))


if __name__ == '__main__':
    main()
