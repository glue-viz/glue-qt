# Full changelog

## v0.3.3 - 2025-02-27

<!-- Release notes generated using configuration in .github/release.yml at main -->
### What's Changed

#### Bug Fixes

* Fix import and segfault in test suite by @astrofrog in https://github.com/glue-viz/glue-qt/pull/25

#### Other Changes

* Pin pytest to <8.3.3 as the test suite currently segfaults with 8.3.3 by @astrofrog in https://github.com/glue-viz/glue-qt/pull/24
* Add glue-core to dev-deps and Python 3.13 envs to CI; compatibility with glue 1.22 BaseViewer by @dhomeier in https://github.com/glue-viz/glue-qt/pull/26

**Full Changelog**: https://github.com/glue-viz/glue-qt/compare/v0.3.2...v0.3.3

## v0.3.2 - 2024-08-19

<!-- Release notes generated using configuration in .github/release.yml at main -->
### What's Changed

#### Bug Fixes

* Improve tables for incompatible subsets by @jfoster17 in https://github.com/glue-viz/glue-qt/pull/12

#### Other Changes

* Update `ptp` call for numpy 2 by @Carifio24 in https://github.com/glue-viz/glue-qt/pull/19
* Update links for standalone app to 2024.03.1 by @astrofrog in https://github.com/glue-viz/glue-qt/pull/20
* Fix test suite by @astrofrog in https://github.com/glue-viz/glue-qt/pull/21
* Don't apply color to existing datasets by default by @Carifio24 in https://github.com/glue-viz/glue-qt/pull/18
* Add CI envs for PyQt 6.5-6.7, PySide 6.5-6.7 & Python 3.12; fix Readthedocs and matplotlib 3.9, Qt6 failures by @dhomeier in https://github.com/glue-viz/glue-qt/pull/17
* Add full implementation of `__gluestate__` and `__setgluestate__` for application by @astrofrog in https://github.com/glue-viz/glue-qt/pull/22

### New Contributors

* @Carifio24 made their first contribution in https://github.com/glue-viz/glue-qt/pull/19
* @dhomeier made their first contribution in https://github.com/glue-viz/glue-qt/pull/17

**Full Changelog**: https://github.com/glue-viz/glue-qt/compare/v0.3.1...v0.3.2

## v0.3.1 - 2024-03-01

<!-- Release notes generated using configuration in .github/release.yml at main -->
### What's Changed

#### Bug Fixes

* Added fix for using WebEngine and OpenGL in same glue session with Qt6 by @astrofrog in https://github.com/glue-viz/glue-qt/pull/15

**Full Changelog**: https://github.com/glue-viz/glue-qt/compare/v0.3.0...v0.3.1

## v0.3.0 - 2023-11-15

<!-- Release notes generated using configuration in .github/release.yml at main -->
### What's Changed

#### New Features

- Support regions in image viewer by @jfoster17 in https://github.com/glue-viz/glue-qt/pull/10

#### Bug Fixes

- Update splash screen path by @jfoster17 in https://github.com/glue-viz/glue-qt/pull/8
- Refresh table sorting when data changes by @jfoster17 in https://github.com/glue-viz/glue-qt/pull/9

#### Other Changes

- Updated/simplified installation instructions by @astrofrog in https://github.com/glue-viz/glue-qt/pull/7

### New Contributors

- @jfoster17 made their first contribution in https://github.com/glue-viz/glue-qt/pull/8

**Full Changelog**: https://github.com/glue-viz/glue-qt/compare/v0.2.0...v0.3.0

## v0.2.0 - 2023-08-21

<!-- Release notes generated using configuration in .github/release.yml at main -->
### What's Changed

#### Bug Fixes

- Fix imports of parse_data and parse_links by @astrofrog in https://github.com/glue-viz/glue-qt/pull/4
- Fixed bug that caused plugins to be loaded twice by @astrofrog in https://github.com/glue-viz/glue-qt/pull/6

#### Documentation

- Fix documentation warnings by @astrofrog in https://github.com/glue-viz/glue-qt/pull/2
- Sphinx book theme by @astrofrog in https://github.com/glue-viz/glue-qt/pull/5

#### Other Changes

- Improve compatibility with PySide by @astrofrog in https://github.com/glue-viz/glue-qt/pull/3

**Full Changelog**: https://github.com/glue-viz/glue-qt/compare/v0.1.0...v0.2.0

## v0.1.0 - 2023-08-15

<!-- Release notes generated using configuration in .github/release.yml at main -->
### What's Changed

Set up initial glue-qt package by extracting Qt-related functionality from glue-core in https://github.com/glue-viz/glue-qt/pull/1

### New Contributors

- @astrofrog made their first contribution in https://github.com/glue-viz/glue-qt/pull/1

**Full Changelog**: https://github.com/glue-viz/glue-qt/commits/v0.1.0
