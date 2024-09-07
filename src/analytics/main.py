import streamlit as st
import duckdb
import altair as alt

import gettext
_ = gettext.gettext

language = st.sidebar.selectbox(_("Language"), ['en', 'pt'])

localizator = gettext.translation('messages', localedir='locales', languages=[language])
localizator.install()
_ = localizator.gettext 

st.title(_("Analysis of Santa Catarina teams"))

con = duckdb.connect("../main.db", read_only=True)

qt_clubs = con.execute("SELECT COUNT(1) FROM main.teams WHERE state = 'sc'").fetchone()[0]
oldest_team_name, oldest_team_found_date, oldest_team_age = con.execute("""
    SELECT team_name, foundation_date, date_sub('year', foundation_date, CURRENT_DATE) AS age FROM main.teams 
    WHERE state = 'sc'
    ORDER BY foundation_date ASC
    LIMIT 1;
""").fetchone()

youngest_team_name, youngest_team_found_date, youngest_team_age = con.execute("""
    SELECT team_name, foundation_date, date_sub('year', foundation_date, CURRENT_DATE) AS age FROM main.teams 
    WHERE state = 'sc'
    ORDER BY foundation_date DESC
    LIMIT 1;
""").fetchone()

clubs_by_decade_df = con.execute(
    """
    SELECT
        COUNT(1) AS ctn,
        case 
            when YEAR(foundation_date) < 1940 then 0
            when YEAR(foundation_date) BETWEEN 1940 AND 1949 then 1
            when YEAR(foundation_date) BETWEEN 1950 AND 1959 then 2
            when YEAR(foundation_date) BETWEEN 1960 AND 1969 then 3
            when YEAR(foundation_date) BETWEEN 1970 AND 1979 then 4
            when YEAR(foundation_date) BETWEEN 1980 AND 1989 then 5
            when YEAR(foundation_date) BETWEEN 1990 AND 1999 then 6
            when YEAR(foundation_date) BETWEEN 2000 AND 2010 then 7
            ELSE 8
        END as decades
    FROM main.teams
    GROUP BY decades
    order by decades
    """
).fetch_df()

clubs_by_decade_df['decades'] = clubs_by_decade_df['decades'].map(
    {0: _('Pre 1940'), 1: _("40's"), 2: _("50's"), 3: _("60's"),
     4: _("70's"), 5: _("80's"), 6: _("90's"), 7: _("2000s"), 8: _("Post 2010")}
)

st.write(_("Quantity SC Clubs").format(qt_clubs))

st.write(_("Oldest SC Club").format(oldest_team_name.title(), oldest_team_age, oldest_team_found_date))

st.write(_("Youngest SC Club").format(youngest_team_name.title(), youngest_team_age, youngest_team_found_date))

title = alt.TitleParams(_('Clubs Founded By Decade'), anchor='middle')
st.write(alt.Chart(clubs_by_decade_df, width=600, height=400, title=title).mark_bar(color="#1A43BF").encode(
    x=alt.X('decades', sort=None, title=_("Decades")),
    y=alt.Y('ctn', title=_("Quantity")),
))

con.close()