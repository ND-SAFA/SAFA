import os
import re
import sys
from functools import total_ordering
from typing import List, Union
from pathlib import Path

migration_regex = re.compile(r'V(\d+)(?:_(\d+))?__.+\.sql')
migration_folder = Path('src/main/resources/db/migration/')
ignore_filename_str = 'MIGRATION_CHECK_IGNORE_BAD_FILENAME'
ignore_version_str = 'MIGRATION_CHECK_IGNORE_OLD_VERSION'


@total_ordering
class Version:
    def __init__(self, major: Union[int, str], minor: Union[int, str]):
        self.major = int(major)
        self.minor = int(minor)

    def __eq__(self, other: 'Version'):
        return self.major == other.major and self.minor == other.minor

    def __lt__(self, other: 'Version'):
        return self.major < other.major or (self.major == other.major and self.minor < other.minor)

    def __repr__(self):
        return f'Version({self.major}, {self.minor})'

    def __str__(self):
        return f'{self.major}.{self.minor}'


def run_check(new_files: List[Path]) -> set[str]:
    errors_found = set()
    all_migrations = get_all_migrations()
    existing_migrations = list(set(all_migrations) - set(new_files))

    formatted_new_files = "\n".join([str(x) for x in new_files])
    formatted_old_files = "\n".join([str(x) for x in existing_migrations])
    print(f'::group::Added files:\n{formatted_new_files}\n::endgroup::')
    print(f'::group::Old files:\n{formatted_old_files}\n::endgroup::')

    latest_version = get_latest_version(existing_migrations, errors_found)
    check_new_file_versions(new_files, latest_version, errors_found)
    return errors_found


def check_new_file_versions(new_files: List[Path], latest_version: Version, errors_found: set[str]):
    for new_file in new_files:
        if migration_folder not in new_file.parents:
            continue

        version = get_version_number(new_file, errors_found, True)

        if not version > latest_version:
            add_error(new_file, errors_found, ignore_version_str,
                      f'Found a new migration whose version is not greater than the current latest version: {new_file}\n'
                      f'This could lead to this migration not being run. '
                      f'Latest version: {latest_version}, This file\'s version: {version}')


def get_all_migrations() -> List[Path]:
    return list(migration_folder.glob('*.sql'))


def get_latest_version(existing_migrations: List[Path], errors_found: set[str]) -> Version:
    versions = [get_version_number(migration, errors_found, False) for migration in existing_migrations]
    versions.sort()
    return versions[-1]


def get_version_number(migration: Path, errors_found: set[str], is_new: bool) -> Version:
    match = re.match(migration_regex, migration.name)
    if not match:
        add_error(migration, errors_found, ignore_filename_str,
                  f'Found migration with an invalid name: {migration}\n'
                  f'Must match pattern {migration_regex.pattern}')

        # if the file is new, we want a high version number, so it doesn't also get flagged as being a bad version
        # if the file is old, we want a low version number, so it doesn't cause other files to get flagged
        return Version(999_999_999 if is_new else 0, 0)

    major, minor = match.groups(0)
    return Version(major, minor)


def add_error(migration: Path, errors_found: set[str], ignore_str: str, message: str):
    try:
        contents = migration.read_text()
    except IOError:
        contents = ""

    if ignore_str in contents:
        print(f'Warning: Found error in {migration}, but it is marked as ignored.')
    else:
        errors_found.add(f'::group::Error: {message}\nInclude {ignore_str} in this file to ignore this message.\n::endgroup::')


if __name__ == '__main__':
    added_files = os.environ['ADDED_FILES']
    errors = run_check([Path(x) for x in added_files.split()])

    for error in errors:
        print()
        print(error)

    sys.exit(len(errors) > 0)
