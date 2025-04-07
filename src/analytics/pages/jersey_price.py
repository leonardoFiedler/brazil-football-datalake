import streamlit as st
import duckdb
import altair as alt
from menu import menu_options

locale_fun, lang_opts = menu_options()

st.title(":tshirt: Jerseys Price Analysis")