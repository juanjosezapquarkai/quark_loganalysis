import streamlit as st
import json
import os

APP_NAME = 'Quark Log Analysis'

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧊",
    # layout='wide'
 )

#st.title(APP_NAME)
header = f"""<header style="background-color:rgb(30, 136, 229);box-shadow: rgba(0, 0, 0, 0.2) 0px 2px 4px -1px, rgba(0, 0, 0, 0.14) 0px 4px 5px 0px, rgba(0, 0, 0, 0.12) 0px 1px 10px 0px;"><img src="data:image/png;base64,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" alt="Quark.ai" style="height: 45px; margin-left: 40px; margin-top: 8px;"></header>"""

st.markdown(header, unsafe_allow_html=True)

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
        if not ((errorlevel == 'alerts' and item['errorlevel'] == 'alert') or errorlevel == 'errors' and item['errorlevel'] == 'error') and not errorlevel == 'alerts and errors':
            continue
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
        if len(log_data) == 0:
            st.write('No ' + levelfilter + ' found in file ' + log_file)
        else:
            for item in log_data:
                markdown_str = '<div><p>' + item[0] + '<br/>' + '<ul style="list-style: none;"><li>' + item[1] + '</li></ul></p></div>'
                st.markdown(markdown_str, unsafe_allow_html=True)

