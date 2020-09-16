import pandas as pd
import streamlit as st

import flowserv.util as util


def show_image(filename, spec):
    st.image(filename, caption=spec.get('caption'))


def show_json(filename, spec):
    if 'caption' in spec:
        st.write(spec['caption'])
    st.write(util.read_object(filename, format=util.FORMAT_JSON))


def show_table(filename, spec):
    df = pd.read_csv(filename)
    if 'caption' in spec:
        st.write(spec['caption'])
    st.table(df)


def show_text(filename, spec):
    if 'caption' in spec:
        st.write(spec['caption'])
    for line in util.read_text(filename).strip().split('\n'):
        st.write(line)
