import streamlit as st
import json
import os

APP_NAME = 'Quark Log Analysis'

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧊",
    # layout='wide'
 )

st.title(APP_NAME)


col1, col2 = st.columns(2)


with col1:
    available_log_files = [
        "",
        "cdc-logs-9-22.txt",
        "cdc-logs-9-23.txt",
        "cdc-logs-9-24.txt",
        "cdc-logs-9-25.txt",
        "cdc-logs-9-26.txt",
        "dfw-mcc-5d.txt",
        "edc-logs-9-22.txt",
        "edc-logs-9-23.txt",
        "edc-logs-9-24.txt",
        "edc-logs-9-25.txt",
        "edc-logs-9-26.txt",
        "mce-mcw-5d.txt",
        "ndc-logs-9-22.txt",
        "ndc-logs-9-23.txt",
        "ndc-logs-9-24.txt",
        "ndc-logs-9-25.txt",
        "ndc-logs-9-26.txt",
        "wan_ecx_09222023.txt",
        "wan_ecx_09232023.txt",
        "wan_ecx_09242023.txt",
        "wan_ecx_09252023.txt",
        "wan_ecx_09262023.txt",
        "wan_ecx_09272023.txt",
    ]
    log_file = st.selectbox(
        'Select a log file',
        available_log_files
    )


with col2:
    available_filters = [
        "",
        "alerts",
        "errors",
        "alerts and errors",
    ]
    levelfilter = st.selectbox(
        'Select a filter',
        available_filters
    )


@st.cache_data
def load_data(log_file, errorlevel):
    with open('data/' + log_file + '_.json') as json_file:
        json_data = json.load(json_file)
    log_data = []
    for item in json_data:
        log_message = item['logmessage']
        try:
            gpt = item['gpt']
        except:
            return log_file
        log_data.append([gpt, log_message])

    return log_data
search = st.button('Search', type='primary')
if search:
    if not os.path.isfile('data/' + log_file + '_.json'):
        st.write("ERROR: could not find log file")
    else:
        log_data = load_data(log_file, levelfilter)
        for item in log_data:
            markdown_str = '<div><p>' + item[0] + '<br/>' + '<ul style="list-style: none;"><li>' + item[1] + '</li></ul></p></div>'
            st.markdown(markdown_str, unsafe_allow_html=True)

