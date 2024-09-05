import streamlit as st
import duckdb

import gettext
_ = gettext.gettext

language = st.sidebar.selectbox(_("Language"), ['en', 'pt'])

localizator = gettext.translation('messages', localedir='locales', languages=[language])
localizator.install()
_ = localizator.gettext 


# conn = duckdb.connect("../main.db")

st.title(_("Hello, world!"))


# conn.close()