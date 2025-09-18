#!/usr/bin/env python3
# scripts/check_snippets.py

import sys
import re

# Regex to find snippet tags like '# [START hello]' or '# [END world]'
SNIPPET_RE = re.compile(r'#\s*\[(START|END)\s+([^\]]+)\]')

def validate_file(filepath):
    """
    Validates snippet tags in a file, reporting all errors in a single-line format.

    Returns:
        bool: True if errors were found, False otherwise.
    """
    tag_stack = []
    file_has_errors = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            match = SNIPPET_RE.search(line)
            if not match:
                continue

            action, name = match.groups()
            name = name.strip()

            if action == 'START':
                if tag_stack:
                    open_tag = tag_stack[-1]
                    print(
                        f"ERROR in {filepath} on line {i}: Cannot '[START {name}]' because '[START {open_tag}]' is still open.",
                        file=sys.stderr
                    )
                    file_has_errors = True
                    continue
                tag_stack.append(name)

            elif action == 'END':
                if not tag_stack:
                    print(
                        f"ERROR in {filepath} on line {i}: Found '[END {name}]' with no matching START tag.",
                        file=sys.stderr
                    )
                    file_has_errors = True
                    continue

                expected_name = tag_stack.pop()
                if name != expected_name:
                    print(
                        f"ERROR in {filepath} on line {i}: Found '[END {name}]' but expected '[END {expected_name}]'.",
                        file=sys.stderr
                    )
                    file_has_errors = True

        if tag_stack:
            open_tag = tag_stack[-1]
            print(
                f"ERROR in {filepath}: File ended but '[START {open_tag}]' was never closed.",
                file=sys.stderr
            )
            file_has_errors = True

    except Exception as e:
        print(f"ERROR: Could not process file {filepath}: {e}", file=sys.stderr)
        file_has_errors = True

    return file_has_errors

def main():
    files_to_check = sys.argv[1:]

    if not files_to_check:
        return 0 # Success

    overall_has_errors = False
    for f in files_to_check:
        if validate_file(f):
            overall_has_errors = True

    if overall_has_errors:
        return 1 # Failure

    return 0 # Success

if __name__ == '__main__':
    raise SystemExit(main())
