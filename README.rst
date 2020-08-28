====================================
FlowServ Demo App Using Streamlit.io
====================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://github.com/scailfin/flowserv-app/blob/master/LICENSE



.. figure:: https://github.com/scailfin/flowserv-core/blob/master/docs/figures/logo.png
    :align: center
    :alt: flowServ Logo



About
=====

This is a test application that allows to run workflow templates as `streamlit.io <streamlit.io>`_ applications.


Installation
============

The app currently has to be installed from GitHub directly. It is recommended that you use a virtual environment for all the following commands.

Install the ``flowapp`` package:

.. code-block:: bash

    pip install git+https://github.com/scailfin/flowserv-app.git

To configure the app make sure to set the following two environment variables (see the `flowServ documentation for more details <https://github.com/scailfin/flowserv-core/blob/master/docs/configuration.rst>`_):

.. code-block:: bash

    export FLOWSERV_DATABASE=sqlite:////home/user/project/flowserv-app/db.sqlite
    export FLOWSERV_API_DIR=/home/user/project/flowserv-app/.flowserv


After setting the environment variables you need to create the flowServ database and install an example app (here we use the `ROB Hello World Demo <https://github.com/scailfin/rob-demo-hello-world>`_):

.. code-block:: bash

    flowserv init

    flowapp install helloworld


Running the Application
=======================

The `flowapp install command will output a string like `export FLOWSERV_APP=7d93c90963054dd7bac4f77fc2fad855`. Use this string to set the environment variable FLOWSERV_APP before you start the application.

.. code-block:: bash

    export FLOWSERV_APP=7d93c90963054dd7bac4f77fc2fad855
    streamlit run flowapp/app.py


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
