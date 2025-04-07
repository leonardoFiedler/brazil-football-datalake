import streamlit as st
from menu import menu_options

locale_fun, lang_opts = menu_options()

st.title(locale_fun(":soccer: Brazil Football Data Lake"))

st.header("Objetivo")

st.write(locale_fun("Welcome Message"))

st.header("Contribua")

st.header("Sobre Nós")