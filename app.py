import streamlit as st

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
        "erros",
        "alerts and errors",
    ]
    filter = st.selectbox(
        'Select a filter',
        available_filters
    )


search = st.button('Search', type='primary')

