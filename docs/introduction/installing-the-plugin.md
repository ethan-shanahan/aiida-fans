# Installing the Plugin

You will need to install the plugin before you can create the code node on your AiiDA profile. AiiDA-FANS is available on the conda-forge package channel. Our recommended method of installing AiiDA-FANS is to use the [Pixi](https://pixi.sh/latest/) package manager, in which case `pixi add aiida-fans` will add the plugin to your project manifest (i.e. a pyproject.toml or pixi.toml file). This way, the plugin and its dependencies (aiida-core and h5py) will be installed in an isolated environment.

!!! note
    Even if you install AiiDA in an isolated environment, it will, by default, continue to use your home directory to manage profiles, thus sharing the same space as any other installation of AiiDA you may have on your system.
