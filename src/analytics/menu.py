from dataclasses import dataclass
import streamlit as st
import gettext

LANGUAGES_OPTIONS = ["en", "pt"]


@dataclass
class LanguageOptions:
    dt_format: str
    selected_lang_idx = 0


# Creates outside to keep it alive and don't restart
# The selectbox value
language_options = LanguageOptions(None)


def on_selectbox_language_change():
    language_options.selected_lang_idx = LANGUAGES_OPTIONS.index(
        st.session_state.selectbox_language_key
    )


def menu_options():
    locale_fun = gettext.gettext
    language = st.sidebar.selectbox(
        locale_fun("Language"),
        LANGUAGES_OPTIONS,
        key="selectbox_language_key",
        on_change=on_selectbox_language_change,
        index=language_options.selected_lang_idx,
    )

    localizator = gettext.translation(
        "messages", localedir="src/analytics/locales", languages=[language]
    )
    localizator.install()
    locale_fun = localizator.gettext
    language_options.dt_format = "%d/%M/%Y" if language == "pt" else "%Y/%M/%d"

    st.sidebar.page_link("main.py", label=locale_fun("Home"))
    st.sidebar.page_link(
        "pages/analysis_sc_teams.py",
        label=locale_fun("Analysis of Santa Catarina teams"),
    )
    st.sidebar.page_link(
        "pages/jersey_price.py",
        label="Jerseys Price Analysis",
    )

    return locale_fun, language_options
