import streamlit as st

from flowserv.model.parameter.boolean import PARA_BOOL
from flowserv.model.parameter.enum import PARA_ENUM
from flowserv.model.parameter.files import PARA_FILE
from flowserv.model.parameter.numeric import PARA_FLOAT, PARA_INT


@st.cache(allow_output_mutation=True)
def enum_options(values):
    """Enumerate optins for a select box."""
    options = list()
    index = 0
    mapping = dict()
    for i, obj in enumerate(values):
        identifier = obj['value']
        options.append(identifier)
        mapping[identifier] = obj['name']
        if obj.get('isDefault', False):
            index = i

    def mapfunc(value):
        return mapping[value]

    return options, index, mapfunc


def show_form(parameters):
    arguments = dict()
    for para in parameters:
        if para.type_id == PARA_BOOL:
            checked = para.default_value if para.default_value else False
            val = st.checkbox(label=para.name, value=checked)
        elif para.type_id == PARA_ENUM:
            options, index, mapfunc = enum_options(para.values)
            val = st.selectbox(
                label=para.name,
                options=options,
                index=index,
                format_func=mapfunc
            )
        elif para.type_id == PARA_FILE:
            val = st.file_uploader(label=para.name)
        elif para.type_id in [PARA_FLOAT, PARA_INT]:
            constraint = para.constraint
            default_value = para.default_value
            if constraint is not None and constraint.is_closed():
                if default_value is None:
                    default_value = constraint.min_value()
                val = st.slider(
                    label=para.name,
                    min_value=constraint.min_value(),
                    max_value=constraint.max_value(),
                    value=default_value
                )
            else:
                val = st.text_input(para.name, para.default_value)
        else:
            val = st.text_input(para.name, para.default_value)
        arguments[para.para_id] = val
    submit = st.button('Run')
    return submit, arguments
