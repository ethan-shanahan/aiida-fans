###################################
 The aiida-fans plugin for `AiiDA`
###################################

.. attention::

   This project is under active development! Breaking changes can and will occur.

This is a plugin for AiiDA that facilitates the use of FANS. FANS is an 
FFT-based homogenisation solver for microscale and multiphysics problems. 
It is an open-source project under active development at the Institute of 
Applied Mechanics, University of Stuttgart. This plugin aims to bring the full 
value of provenance tracking and database integration to the results produced by
FANS.

The design goals of this plugin are primarily to provide as simplistic a user 
experience as is reasonably possible. Secondarily, more featureful additions 
will be made to extend the users' options for queryability and optimisation.


``aiida-fans`` is released under the :doc:`GNU General Public License v3 </development/license>`.
Please contact ethan.shanahan@gmail.com for information concerning ``aiida-fans``
and the `AiiDA mailing list <http://www.aiida.net/mailing-list/>`_ for questions
concerning ``AiiDA``.

--------------------------------------------------------------------------------

See below for how to navigate this plugin's documentation.

*****************
 Getting Started 
*****************

Here is what you need to know to get started. We focus on simply installing this
plugin under the assumption that you already have and know how to use both
aiida-core and FANS. However, in the later case, we point you in the right
direction to learn more. Once installed, we explain how to confirm that the
three applications are working in unison.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   orientation/landing
   orientation/installation
   orientation/fundamentals
   AiiDA Documentation <https://aiida.readthedocs.io>

*******
 Usage
*******

Once you have successfully installed this plugin, you can begin using it. This
section begins by describing most of the plugin's functionality and how to avail
of it. Following that is a step-by-step demonstration of the plugin in use that
may be very helpful to quickly learn from. Finally, a comprehensive API is
detailed using automatically generated documentation straight from the source
code. 

.. toctree::
   :maxdepth: 2
   :caption: Usage

   usage/landing
   usage/tutorial
   usage/API

*************
 Development
*************

This section is for developers intending to contribute to this plugin or use it
to create their own tooling. Information on the developement pipeline and
guidelines can be found. Additionally, the changelog is accessible here and the
project's license is presented in full.

.. toctree::
   :maxdepth: 2
   :caption: Development

   development/landing
   development/changelog
   development/license

--------------------------------------------------------------------------------

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. 
   Directives...

.. _AiiDA: http://www.aiida.net

.. role:: python(code)
   :language: python

.. meta::
   :description: The aiida-fans plugin for using FANS with AiiDA.
   :keywords: AiiDA, FANS, plugin
