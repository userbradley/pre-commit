# setup.py
from setuptools import find_packages, setup

setup(
    name="bradley_hooks",
    version="0.0.4",  # Major version bump for the new structure
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "check-snippets = bradley_hooks.check_snippets:main",
        ],
    },
)
