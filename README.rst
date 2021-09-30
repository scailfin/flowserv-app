====================================
FlowServ Demo App Using Streamlit.io
====================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://github.com/scailfin/flowserv-app/blob/master/LICENSE



About
=====

*Depreciation*: The **flowserv-app** code has been integrated in `flowserv-core <https://github.com/scailfin/flowserv-core>`_ starting with version 0.9.0. This repository is therefore no longer maintained.


This package allows to run `flowServ <https://github.com/scailfin/flowserv-core>`_ workflow templates as `streamlit.io <streamlit.io>`_ applications.



Installation
============

The app currently has to be installed from GitHub directly. It is recommended that you use a virtual environment for all the following commands.

Install the ``flowapp`` package:

.. code-block:: bash

    pip install git+https://github.com/scailfin/flowserv-app.git


To configure the app make sure to set the environment variables *FLOWSERV_BACKEND_CLASS* and *FLOWSERV_BACKEND_MODULE*. These environment variables determine the backend that is used to run workflows. See the `flowServ documentation for more details <https://github.com/scailfin/flowserv-core/blob/master/docs/configuration.rst>`_.

The repository contains a default configuration file `env.config <https://github.com/scailfin/flowserv-app/blob/master/config/env.config>`_. You can use this default configuration (e.g., by running `source env.config`) to define the default multi-process workflow engine as the backend.


Running the Application
=======================

The command to run a **flowServ** workflow as a streamlit web application is:

.. code-block:: bash

    streamlit run flowapp/app.py [ --
        [-w | --source=] <workflow-identifier or workflow-template-folder>
        [-s | --specfile=] <filename>  # Optional path to workflow specification file.
        [-m | --manifest=] <filename>  # Optional path to workflow manifest file.
        [-n | --name=] <name>          # Optional application title.
    ]


The ``__source`` references the workflow that is being run. This can either be the identifier of a template from the flowServ Workflow Repository or the path to a local folder containing a workflow template.

As an example, to run the *Hello World Demo* use the following command:

.. code-block:: bash

    streamlit run flowapp/app.py -- --source=helloworld
