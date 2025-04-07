from dataclasses import dataclass
import streamlit as st
import gettext


@dataclass
class LanguageOptions:
    dt_format: str


def menu_options():
    locale_fun = gettext.gettext
    language = st.sidebar.selectbox(locale_fun("Language"), ["en", "pt"])

    localizator = gettext.translation(
        "messages", localedir="src/analytics/locales", languages=[language]
    )
    localizator.install()

    locale_fun = localizator.gettext
    dt_format = "%d/%M/%Y" if language == "pt" else "%Y/%M/%d"

    st.sidebar.page_link("main.py", label=locale_fun("Home"))
    st.sidebar.page_link(
        "pages/analysis_sc_teams.py",
        label=locale_fun("Analysis of Santa Catarina teams"),
    )
    st.sidebar.page_link(
        "pages/jersey_price.py",
        label="Jerseys Price Analysis",
    )

    return locale_fun, LanguageOptions(dt_format)
