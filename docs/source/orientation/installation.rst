.. highlight:: bash

Installation
============

aiida-fans
----------

Here, we install the plugin from the `Python Package Index <https://pypi.org/project/aiida-fans/>`_.
We recommended you use a virtual environment to do this, so as to encapsulate
your AiiDA installation along with the plugin. There are many ways to produce
virtual environments, and `Pixi <https://pixi.sh/latest/>`_ is one such suggestion.

.. note::
    Currently, ``aiida-fans`` is only available via PyPI.
    We are working on making the plugin available through conda-forge.
    However, AiiDA recommends using pip to install plugins.

Once your virtual environment is active, you can add ``aiida-fans`` as a dependency
or simply install it like so::

   pip install aiida-fans

We assumed you have AiiDA and FANS installed, but if that's not the case, here
are some quick installation guides.

AiiDA
-----

AiiDA needs to be installed in your environment along with ``aiida-fans``. The
plugin does include ``aiida-core`` as a dependency, but you may be better off
installing it yourself as it comes with some options you should consider.

See the `AiiDA Installation Guide <https://aiida.readthedocs.io/projects/aiida-core/en/stable/installation/index.html>`_
for the full picture, or use the following to get started::

    pip install aiida-core

FANS
----

FANS is not included as a dependency of ``aiida-fans`` by default as it is only
required on the computer you plan to run it on. AiiDA allows you to run your jobs
on a remote computer. See the 
`FANS README on installation <https://github.com/DataAnalyticsEngineering/FANS/tree/main?tab=readme-ov-file#installing>`_
to learn more about how to install FANS from source, but to get started use::

    conda install -c conda-forge FANS

If you wish to install FANS along with this plugin, however, you can specify
the optional dependency like so::

    pip install aiida-fans[FANS]
