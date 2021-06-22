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


To configure the app make sure to set the environment variables *FLOWSERV_API_DIR* and *FLOWSERV_DATABASE*. These environment variables determine the database and the folder on the local file system where all workflow runs will be stored. You can use the environment variables *FLOWSERV_BACKEND_CLASS* and *FLOWSERV_BACKEND_MODULE* to configure the backend that is used to run workflows. See the `flowServ documentation for more details <https://github.com/scailfin/flowserv-core/blob/master/docs/configuration.rst>`_.

The repository contains a default configuration file `env.config <https://github.com/scailfin/flowserv-app/blob/master/env.config>`_:


.. code-block:: bash

    # Directory for all workflow files
    export FLOWSERV_API_DIR=$PWD/.flowapp

    # Use a multi-process backend
    export FLOWSERV_BACKEND_CLASS=SerialWorkflowEngine
    export FLOWSERV_BACKEND_MODULE=flowserv.controller.serial.engine

    # Alternative: Use a Docker backend
    # export FLOWSERV_BACKEND_MODULE=flowserv.controller.serial.docker
    # export FLOWSERV_BACKEND_CLASS=DockerWorkflowEngine


    # Use asynchronous workflow execution for the app.
    export FLOWSERV_ASYNCENGINE=False

    # Do not require user authentication
    export FLOWSERV_AUTH=open

    # Database (SQLLite)
    export FLOWSERV_DATABASE=sqlite:///$FLOWSERV_API_DIR/flowapp.db


You can use this default configuration (e.g., by running `source env.config`). This will (i) maintain all workflow files in a sub-folder `.flowapp` with the current working directory, (ii) use a SQLite database within the API base directory, and (iii) use the default multi-process workflow engine. To use a Docker engine instead change the respective lines for *FLOWSERV_BACKEND_CLASS* and *FLOWSERV_BACKEND_MODULE* in the configuration file before running `source`.



Create Database
---------------

After setting the environment variables you need to create the **flowServ** database:

.. code-block:: bash

    flowserv init


This will override any existing database referenced by the environment variable *FLOWSERV_DATABASE* and create a fresh (empty) database schema.



Install Demo Workflow
---------------------

Before running the application the workflow template that defines the application has to be installed (e.g. using `flowserv install`). Here we give an example that uses the `ROB Hello World Demo <https://github.com/scailfin/rob-demo-hello-world>`_:

.. code-block:: bash

    flowserv install helloworld -k helloworldapp -g


This will install the **Hello World! Demo** workflow. The workflow identifier (required when running the streamlit application is `helloworldapp`.


Running the Application
=======================

The command to run a **flowServ** workflow as a streamlit web application is:

.. code-block:: bash

    streamlit run flowapp/app.py [ -- [-a | --key=] <application-identifier>]


The application identifier references the workflow that is being run. If you run the application without providing the application identifier as a command-line argument the identifier is expected to be in the environment variable *FLOWSER_APP*, e.g.,:

.. code-block:: bash

    export FLOWSERV_APP=helloworldapp
    streamlit run flowapp/app.py



Run Docker  Demo
----------------

There is also a Docker container available that contains the *Hello World Demo* as well as the `PIE Colony Single-Image Analysis Workflow <https://github.com/scailfin/flowserv-PIE-workflows>`_. To run the demo application from the Docker container do the following:

.. code-block:: bash

    docker image pull heikomueller/flowappdemo:latest

    # Run the 'Hello World' Demo
    docker run \
        --rm \
        -p 8501:8501 \
        -e FLOWSERV_APP=7d93c90963054dd7bac4f77fc2fad855 \
        flowappdemo streamlit run /app/flowapp/app.py


    # Run the 'PIE Single-Image Analysis' Demo
    docker run \
        --rm \
        -p 8501:8501 \
        -e FLOWSERV_APP=1e5392ae6a7b4409893bb6b1a9f28c6e \
        flowappdemo streamlit run /app/flowapp/app.py

The application should then be available at Url `http://172.17.0.2:8501 <http://172.17.0.2:8501>`_.
