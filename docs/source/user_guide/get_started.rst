===============
Getting started
===============

This page should contain a short guide on what the plugin does and
a short example on how to use the plugin.

Installation
++++++++++++

Use the following commands to install the plugin::

    git clone https://github.com/ethan-shanahan/aiida-fans .
    cd aiida-fans
    pip install -e .  # also installs aiida, if missing (but not postgres)
    #pip install -e .[pre-commit,testing] # install extras for more features
    verdi quicksetup  # better to set up a new profile
    verdi plugin list aiida.calculations  # should now show your calculation plugins

Then use ``verdi code setup`` with the ``fans`` input plugin
to set up an AiiDA code for aiida-fans.

Usage
+++++

A quick demo of how to submit a calculation::

    verdi daemon start         # make sure the daemon is running
    cd examples
    verdi run test_submit.py        # submit test calculation
    verdi calculation list -a  # check status of calculation

If you have already set up your own aiida_fans code using
``verdi code setup``, you may want to try the following command::

    fans-submit  # uses aiida_fans.cli

Available calculations
++++++++++++++++++++++

``aiida-calcjob:: FansCalculation``
