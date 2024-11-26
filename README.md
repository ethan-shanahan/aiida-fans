# aiida-fans

<!-- [![PyPI Package][pypi-badge]][pypi-link] -->
[![GitHub Release][release-badge]][release-link]
[![Build Status][ci-badge]][ci-link]
[![Coverage Status][cov-badge]][cov-link]
[![Docs Status][docs-badge]][docs-link]

This is a plugin for [AiiDA][aiida-link] that facilitates the use of [FANS][FANS-link]. FANS is an FFT-based homogenisation solver for microscale and multiphysics problems. It is an open-source project under active development at the Institute of Applied Mechanics, University of Stuttgart. This plugin aims to bring the full value of provenance tracking and database integration to the results produced by FANS.

The design goals of this plugin are primarily to provide as simplistic a user experience as is reasonably possible. Secondarily, more featureful additions will be made to extend the users' options for queryability and optimisation.

### Upcoming
**Please note:** This plugin is currently in the planning stage of development, with substantial contributions coming soon.

- basic functionality capable of completing the example simulations presented by FANS
- a start to the documentation
- publishing on PyPI

## Installation
The plugin is currently unavailable via PyPI at this stage in development, but it is intended to be published upon an upcoming functional release.

The package can always be installed by cloning this repository and installing it locally like so...

```bash
$ pip install ./aiida-fans
```

You must also ensure that FANS, AiiDA, and their various dependencies are installed. Please consult the [FANS repository][FANS-link] and the [AiiDA installation][aiida-install-link] guide for more information.

## Contact

You can contact ethan.shanahan@gmail.com with regard to this plugin specifically.

<!-- URLs -->
[pypi-badge]: https://badge.fury.io/py/aiida-fans.svg
[pypi-link]: https://badge.fury.io/py/aiida-fans
[release-badge]: https://img.shields.io/github/v/release/ethan-shanahan/aiida-fans?include_prereleases
[release-link]: https://github.com/ethan-shanahan/aiida-fans/releases
[ci-badge]: https://github.com/ethan-shanahan/aiida-fans/actions/workflows/ci.yml/badge.svg?branch=main
[ci-link]: https://github.com/ethan-shanahan/aiida-fans/actions
[cov-badge]: https://coveralls.io/repos/github/ethan-shanahan/aiida-fans/badge.svg?branch=main
[cov-link]: https://coveralls.io/github/ethan-shanahan/aiida-fans?branch=main
[docs-badge]: https://readthedocs.org/projects/aiida-fans/badge
[docs-link]: http://aiida-fans.readthedocs.io/

[aiida-link]: https://www.aiida.net/
[aiida-install-link]: https://aiida.readthedocs.io/projects/aiida-core/en/latest/installation/index.html
[FANS-link]: https://github.com/DataAnalyticsEngineering/FANS
