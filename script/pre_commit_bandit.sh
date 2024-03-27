#!/usr/bin/env bash
###################################################################
# Run bandit on passed in files.
# Needed to ensure .config file is loaded
#
# Params
#   Files. path to one or more json files separated by spaces
###################################################################

# Stop on errors
set -e

echo "Running bandit pre-commit hook"
which python
which pip
which bandit
bandit --version
pip freeze
echo
echo

printf 'Running %s with args %s\n' "$0" "$*"

for i do
    if ! bandit --quiet --format=custom --configfile pyproject.toml "$i"; then
        echo "bandit failed."
        exit 1
    fi
done
