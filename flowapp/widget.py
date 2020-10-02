# This file is part of the Reproducible and Reusable Data Analysis Workflow
# Server (flowServ).
#
# Copyright (C) 2019-2020 NYU.
#
# flowServ is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Simple widgets to display different types of result files from a successful
workflow run.
"""

import json
import pandas as pd
import streamlit as st

from typing import Dict, IO

from flowserv.app.result import RunResult


def display_runfiles(run: RunResult):
    """Display all result files for a given workflow run.

    Parameters
    ----------
    run: flowserv.app.result.RunResult
        Run result handle.
    """
    for _, key, obj in run.files():
        ftype = obj.get('format', {}).get('type')
        file = run.open(key)
        if 'title' in obj:
            st.subheader(obj['title'])
        if ftype == 'csv':
            show_table(file, spec=obj)
        elif ftype == 'image':
            show_image(file, spec=obj)
        elif ftype == 'json':
            show_json(file, spec=obj)
        elif ftype == 'plaintext':
            show_text(file, spec=obj)


# -- Helper methods to display different file types. --------------------------

def show_image(file: IO, spec: Dict):
    """Display an image.

    Parameters
    ----------
    file: io.BytesIO
        IO buffer containing the file content.
    spec: dict
        File output format specification.
    """
    st.image(file, caption=spec.get('caption'))


def show_json(file: IO, spec: Dict):
    """Display a JSON object.

    Parameters
    ----------
    file: io.BytesIO
        IO buffer containing the file content.
    spec: dict
        File output format specification.
    """
    if 'caption' in spec:
        st.write(spec['caption'])
    st.write(json.load(file))


def show_table(file: IO, spec: Dict):
    """Display the contents of a CSV file as a pandas DataFrame.

    Parameters
    ----------
    file: io.BytesIO
        IO buffer containing the file content.
    spec: dict
        File output format specification.
    """
    format = spec.get('format', {})
    if not format.get('header', True) and format.get('columns'):
        df = pd.read_csv(file, header=None, names=format.get('columns'))
    else:
        df = pd.read_csv(file)
    if 'caption' in spec:
        st.write(spec['caption'])
    st.table(df)


def show_text(file: IO, spec: Dict):
    """Display the lines in a text file.

    Parameters
    ----------
    file: io.BytesIO
        IO buffer containing the file content.
    spec: dict
        File output format specification.
    """
    if 'caption' in spec:
        st.write(spec['caption'])
    for line in file:
        st.text(line.decode('utf-8'))
