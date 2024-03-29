# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

_Note: 'Unreleased' section below is used for untagged changes that will be issued with the next version bump_

### [Unreleased] - 2022-00-00
#### Added
#### Changed
#### Deprecated
#### Removed
#### Fixed
#### Security
__BEGIN-CHANGELOG__

### [0.5.0] - 2023-11-12
#### Added
 - Py 3.11 support lol
#### Changed
 - Bumped tox and other test support tools by a major version. Updated related config files to support new versions.
#### Fixed
 - Tests were breaking due to messy handling of objects in a Flask environment. I'll be honest; no clue if these fixes are ideal, but they seem to take the Flask paradigm into account a bit better than the earlier routine.

### [0.4.2] - 2022-12-19
#### Changed
 - keygen endpoint now accepts url params
 - updated requirements

### [0.4.1] - 2022-11-18
#### Changed
 - path to hosts file
 - minor CSS tweaks

### [0.4.0] - 2022-11-18
#### Added
 - Date `/etc/hosts` file last changed as footer
 - `pre-commit` support
 - Makefile
#### Changed
 - New logo
 - Adjusted defaults for keygen
 - Code run through linters
 - Minor CSS tweaks

### [0.3.1] - 2022-06-24
#### Added
 - Darkmode style
#### Changed
 - Reload buttons moved out of main nav menu to pages
 - Shared methods for table rendering / copying data
#### Removed
 - Individual table templates

### [0.3.0] - 2022-04-29
#### Added
 - CHANGELOG
 - pyproject.toml
 - poetry.lock
#### Changed
 - Completed switch to poetry
 - Shifted to new PPM routine for package management
#### Deprecated
 - Versioneer
#### Removed
 - Lots of PPM-dependent files

__END-CHANGELOG__
