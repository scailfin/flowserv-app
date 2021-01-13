# This file is part of the Reproducible and Reusable Data Analysis Workflow
# Server (flowServ).
#
# Copyright (C) 2019-2020 NYU.
#
# flowServ is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Main routine to run the flowApp application from the command line. Use the
following command to run flowApp as a streamlit web application:

streamlit run flowapp/app.py [ -- [-a | --key=] <application-identifier>]

The application identifier references the workflow that is being run. This
workflow has to have been installed prior to running the app (e.g., using the
flowserv install CLI command). If you run the application without providing the
application identifier as a command-line argument the identifier is expected to
be in the environment variable FLOWSER_APP.
"""

import argparse
import streamlit as st
import sys

from typing import Optional

from flowserv.client.app.base import Flowserv
from flowserv.client.app.workflow import Workflow

from flowapp.forms import show_form
from flowapp.widget import display_runfiles

import flowserv.config as config


@st.cache(allow_output_mutation=True)
def get_app(app_key: Optional[str] = None) -> Workflow:
    """Get the application handle for the specified application identifier. If
    no application identifier is given it is expected in the environment
    variable FLOWSERV_APP.

    Parameters
    ----------
    app_key: string
        Unique identifier referencing the workflow that defines the application
        that is being run.

    Returns
    -------
    flowserv.client.app.workflow.Workflow
    """
    return Flowserv().open(identifier=app_key)


def main(app_key):
    """Run application that is identified by the given key."""
    st.set_option('deprecation.showfileUploaderEncoding', False)
    app = get_app(app_key)
    # Show application title, description, and instructions.
    st.title(app.name())
    st.header(app.description())
    st.markdown(app.instructions())
    # Render the main input form. The result is a boolean flag indicating if
    # the submit button was clicked and providing a mapping from template
    # parameter identifier to the submitted value in the respective input
    # form element.
    submit, arguments = show_form(app.parameters().sorted())
    if submit:
        # Run the workflow with the submitted parameter values. Show a spinner
        # while the workflow runs.
        with st.spinner('Running ...'):
            run = app.start_run(arguments, poll_interval=1)
        # Check if the workflow completed successfully or with errors.
        if run.is_error():
            # Display error messages.
            st.error('\n'.join(run.messages()))
        else:
            # Display run result files.
            st.header('Run Results')
            display_runfiles(run)
            postrun = app.get_postproc_results()
            if postrun:
                st.header('Post-Processing Results')
                display_runfiles(postrun)
        # Show a clear button that allows to remove displayed results from a
        # previous run.
        if st.button('clear', key='clear'):
            submit = False


if __name__ == '__main__':
    # Parse command line args to get the optional application key.
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--key", type=str, default=None, required=False)
    parsed_args = parser.parse_args(args)
    app_key = parsed_args.key if parsed_args.key is not None else config.APP()
    # Run the main application.
    main(app_key)
