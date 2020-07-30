import argparse
import streamlit as st
import sys

from flowapp.forms import show_form
from flowserv.app import App

import flowserv.config.app as config
import flowserv.model.workflow.state as state


@st.cache(allow_output_mutation=True)
def get_app(app_key):
    """Get the application handle."""
    return App(key=app_key)


def main(app_key):
    """Run application that is identified by the given key."""
    app = get_app(app_key)
    # Show application title, description, and instructions.
    st.title(app.name())
    st.header(app.description())
    st.markdown(app.instructions())
    # Render the main input form.
    submit, arguments = show_form(app.parameters())
    if submit:
        with st.spinner('Running ...'):
            r = app.run(arguments)
        if r['state'] == state.STATE_ERROR:
            st.error('\n'.join(r['messages']))
        else:
            run_id = r['id']
            for obj in r['files']:
                filename, mimetype = app.get_file(run_id, file_id=obj['id'])
                if mimetype == 'text/plain':
                    st.subheader(obj['name'])
                    with open(filename, 'r') as f:
                        for line in f:
                            st.write(line.strip())
        if st.button('clear', key='clear'):
            submit = False


if __name__ == '__main__':
    # Parse command line args to get the optional application key.
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--key", type=str, default=None, required=False)
    parsed_args = parser.parse_args(args)
    app_key = config.APP_KEY(parsed_args.key)
    # Run the main application.
    main(app_key)
