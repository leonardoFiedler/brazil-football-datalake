import streamlit as st
import duckdb
import altair as alt
from menu import menu_options

locale_fun, lang_opts = menu_options()

col1, mid, col2 = st.columns([3, 1, 20])
with col1:
    st.image("src/analytics/assets/sc_flag.jpg", width=90)
with col2:
    st.markdown(
        f"<h2 style='text-align: left; padding: 0;'>{locale_fun('Analysis of Santa Catarina teams')}</h2>",
        unsafe_allow_html=True,
    )

con = duckdb.connect("src/main.db", read_only=True)

qt_clubs = con.execute("SELECT COUNT(1) FROM main.teams WHERE state = 'sc'").fetchone()[
    0
]
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

clubs_by_decade_df["decades"] = clubs_by_decade_df["decades"].map(
    {
        0: locale_fun("Pre 1940"),
        1: locale_fun("40's"),
        2: locale_fun("50's"),
        3: locale_fun("60's"),
        4: locale_fun("70's"),
        5: locale_fun("80's"),
        6: locale_fun("90's"),
        7: locale_fun("2000s"),
        8: locale_fun("Post 2010"),
    }
)

st.write(locale_fun("Quantity SC Clubs").format(qt_clubs))

st.write(
    locale_fun("Oldest SC Club").format(
        oldest_team_name.title(), oldest_team_age, oldest_team_found_date
    )
)

st.write(
    locale_fun("Youngest SC Club").format(
        youngest_team_name.title(), youngest_team_age, youngest_team_found_date
    )
)

title = alt.TitleParams(locale_fun("Clubs Founded By Decade"), anchor="middle")
st.write(
    alt.Chart(clubs_by_decade_df, width=600, height=400, title=title)
    .mark_bar(color="#1A43BF")
    .encode(
        x=alt.X("decades", sort=None, title=locale_fun("Decades")),
        y=alt.Y("ctn", title=locale_fun("Quantity")),
    )
)

con.close()
