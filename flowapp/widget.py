import json
import pandas as pd
import streamlit as st


def show_image(filename, spec):
    st.image(filename, caption=spec.get('caption'))


def show_json(filename, spec):
    if 'caption' in spec:
        st.write(spec['caption'])
    with open(filename, 'r') as f:
        obj = json.load(f)
    st.write(obj)


def show_table(filename, spec):
    df = pd.read_csv(filename)
    if 'caption' in spec:
        st.write(spec['caption'])
    st.table(df)


def show_text(filename, spec):
    if 'caption' in spec:
        st.write(spec['caption'])
    with open(filename, 'r') as f:
        for line in f:
            st.write(line.strip())
