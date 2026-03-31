# AiiDA-FANS-tutorial

[![Open in molab][molab-badge]][molab-link]

Learn how to use AiiDA-FANS in this [marimo][marimo-link]-powered tutorial subpackage.

## Installation

The recommended way to run this tutorial is to clone the AiiDA-FANS repository, then use [Pixi][Pixi-link] to install the proper environment and run marimo.

```sh
git clone https://github.com/DataAnalyticsEngineering/AiiDA-FANS
cd AiiDA-FANS
```

The project has been configured to make the next step extremely simple. Once you are in the root directory of the repository, running the tutorial with Pixi is as simple as:

```sh
pixi run tutorial
```

This command moves the working directory to `tutorial/` and spins up the marimo notebook server on a localhost port. Pixi automatically installs all the dependencies, including FANS, in an isolated environment (*./.pixi/envs/tutorial*).

Your browser should open to display the notebook. Otherwise, find the URL in marimo's terminal output.


<!-- URLs -->
[molab-badge]: https://marimo.io/molab-shield.svg
[molab-link]: https://molab.marimo.io/github/DataAnalyticsEngineering/AiiDA-FANS/blob/dev/tutorial/tutorial.py
[marimo-link]: https://marimo.io/
[Pixi-link]: https://pixi.sh/latest/
