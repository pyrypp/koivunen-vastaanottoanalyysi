import streamlit as st
import pandas as pd
import datetime as dt
from datetime import time, date
from datetime import datetime
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import math
from streamlit_option_menu import option_menu

# st.set_page_config(layout="wide")
st.markdown(
        f"""
<style>
    .appview-container .main .block-container{{
        max-width: {1450}px;
        padding-left: {2}rem;
        paddint-right: {2}rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


st.sidebar.subheader("Navigoi sivujen välillä yllä olevan valikon avulla!")


st.header("Kellonajan ja viikonpäivän vaikutus nopeuteen")

tc1, tc2 = st.columns([2,1])
with tc1:
    st.write("Tutkitaan, miten kellonaika ja viikonpäivä vaikuttavat hyllytysnopeuteen.")
    st.write("""Nopeuden yksikkönä riviä/tunti. Datasta on koitettu suodattaa kahvi- ja lounastauot pois, 
    jolloin jokaisen päivän tunnin kohdalta laskettu nopeus olisi mahdollisimman luotettava ja vertailukelpoinen.""")

st.write("---")


### valinnat
col1, col2 = st.columns([2, 1])

with col1:
    alueview = st.radio(label="**Näkymä:**", 
        options=["Kaikki alueet yhteensä", "Tarkastele alueita erikseen"], 
        key="alueview6",
        index=0
        )


if alueview =="Kaikki alueet yhteensä":
    kaikkiyht6 = True
else:
    kaikkiyht6 = False


### yakseli filtteri
with col2:
    st.write("")
    st.write("")
    if not kaikkiyht6:
        yax_5 = st.checkbox("Vapauta akselit", key="yax_9", value=True)
    else:
        yax_5 = st.checkbox("Vapauta akselit", value=True, disabled=True, key="yax_10")

### haetaan data
df5day = pd.read_excel("data/rivispeed2.xlsx")

if kaikkiyht6:
    df5 = pd.read_excel("data/dayspeed_h.xlsx")
    df5day_cut = df5day[df5day["cumtotal"]>4].groupby("day")["speed"].mean().reset_index()
    df5day = df5day[df5day["cumtotal"]>0.5].groupby("day")["speed"].mean().reset_index()
else:
    df5 = pd.read_excel("data/dayspeed_h_a.xlsx")
    df5day_cut = df5day[df5day["cumtotal"]>4].groupby(["day", "alue"])["speed"].mean().reset_index()
    df5day = df5day[df5day["cumtotal"]>0.5].groupby(["day", "alue"])["speed"].mean().reset_index()

df5["speed"] = df5["speed"].round(1)
df5day["speed"] = df5day["speed"].round(1)
df5day_cut["speed"] = df5day_cut["speed"].round(1)



### kaaviot

if kaikkiyht6==True:
    h=580
    c0, c1, c2, c4 = st.columns([1, 6, 6, 1])
    with c1:
        fig1 = px.scatter(df5, x="h", y="speed", height=h, trendline="lowess",
        labels={"speed":"Nopeus", "h":"Kellonaika (tunti)"}, title="<b>Nopeus päivän sisällä")

        fig1.update_traces(line_color="red")
        fig1.update_xaxes(matches=None)
        fig1.update_yaxes(matches=None)
        fig1.update_layout(font_size=16)
        fig1.update_xaxes(fixedrange=True)
        fig1.update_yaxes(fixedrange=True)
        fig1.update_layout(showlegend=False)
        fig1.update_layout(template="plotly")
        # fig1.update_layout(margin=dict(
        #     # b=50,
        #     r=50,
        #     l=50,
        #     t=50
        # ))


        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig1date = px.bar(df5day, x="day", y="speed", height=h, category_orders={"day":["Ma","Ti","Ke","To","Pe","La","Su"]}, 
        title="<b>Nopeus viikonpäivän mukaan", color="day",
        color_discrete_sequence=["#636EFA", "#636EFA", "#636EFA", "#636EFA", "#636EFA", "#EF553B", "#EF553B"],
        labels={"speed":"Nopeus", "day":"Päivä"})

        fig1date.update_yaxes(matches=None)
        fig1date.update_layout(font_size=16)
        fig1date.update_xaxes(fixedrange=True)
        fig1date.update_yaxes(fixedrange=True)
        fig1date.update_layout(showlegend=False)
        fig1date.update_layout(template="plotly")
        # fig1date.update_layout(margin=dict(
        #     # b=50,
        #     r=50,
        #     l=50,
        #     t=50
        # ))

        st.plotly_chart(fig1date, use_container_width=True)

else:
    fig2 = px.scatter(df5, x="h", y="speed", facet_col="alue", facet_col_wrap=6,
    height=970, trendline="lowess", facet_row_spacing=0.05, hover_data={"alue":False},
    labels={"speed":"Nopeus", "h":"Kellonaika (tunti)"}, title="<b>Nopeus päivän sisällä")

    fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig2.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
    fig2.update_traces(line_color="red")
    fig2.update_layout(font_size=14)
    fig2.update_xaxes(fixedrange=True)
    fig2.update_yaxes(fixedrange=True)
    fig2.update_layout(showlegend=False)
    fig2.update_layout(template="plotly")
    fig2.update_layout(margin=dict(
        b=50,
        # r=50,
        # l=50,
        t=120
    ))

    if yax_5:
        fig2.update_xaxes(matches=None)
        fig2.update_yaxes(matches=None)            

    st.plotly_chart(fig2, use_container_width=True)
    st.write("")

    fig2date = px.bar(df5day, x="day", y="speed", height=970, category_orders={"day":["Ma","Ti","Ke","To","Pe","La","Su"]}, 
    title="<b>Nopeus viikonpäivän mukaan", color="day", facet_col="alue", facet_col_wrap=6, facet_row_spacing=0.05, hover_data={"alue":False},
    color_discrete_sequence=["#636EFA", "#636EFA", "#636EFA", "#636EFA", "#636EFA", "#EF553B", "#EF553B"],
    labels={"speed":"Nopeus", "day":"Päivä"})

    fig2date.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig2date.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
    fig2date.update_layout(font_size=16)
    fig2date.update_xaxes(fixedrange=True)
    fig2date.update_yaxes(fixedrange=True)
    fig2date.update_layout(showlegend=False)
    fig2date.update_layout(template="plotly")
    # fig1date.update_layout(margin=dict(
    #     # b=50,
    #     r=50,
    #     l=50,
    #     t=50
    # ))

    if yax_5:
        fig2date.update_yaxes(matches=None) 

    st.plotly_chart(fig2date, use_container_width=True)



st.write("")
st.subheader("Huomataan, että")

tcc1, tcc2 = st.columns([2, 1])

with tcc1:
    st.write("- Iltapäivällä hyllyttäjien nopeus on heikompi kuin aamulla. Iltaa kohden nopeus taas paranee. Syvemmän analyysin kautta huomattiin, että ilmiö näkyy erityisen vahvasti aamuvuorossa olevilla.")
    st.write("- Alueiden välillä on vaihtelua.")
    st.write("""- Viikonloppuisin nopeus vaikuttaisi olevan heikompi kuin arkipäivinä.
    Tämä saattaa tosin johtua siitä, että arkipäivisin hyllyttämiseen käytetään vähemmän työtunteja kuin lauantaina tai sunnuntaina.
    Ja kuten aikaisemmin huomattiin, suurempi määrä työtunteja korreloi hitaamman nopeuden kanssa.""")


st.write("---")

tc21, tc22 = st.columns([2,1])
with tc21:
    st.write("""Aikaisemmin huomattiin, että työtuntien määrän vaikutus nopeuteen häviää, kun työtunteja on enemmän kuin neljä.
    Suodatetaan dataa siis niin, että mukana on vain päivät, jolloin työntekijä on hyllyttänyt vähintään neljä tuntia.""")



### kaaviot

if kaikkiyht6==True:
    h=590
    c0, c1, c2, c4 = st.columns([1, 6, 6, 1])

    with c1:
        fig1date_cut = px.bar(df5day_cut, x="day", y="speed", height=h, category_orders={"day":["Ma","Ti","Ke","To","Pe","La","Su"]}, 
        title="<b>Nopeus viikonpäivän mukaan, <br>kun käytetty aika on vähintään 4 h", color="day",
        color_discrete_sequence=["#636EFA", "#636EFA", "#636EFA", "#636EFA", "#636EFA", "#EF553B", "#EF553B"],
        labels={"speed":"Nopeus", "day":"Päivä"})

        fig1date_cut.update_yaxes(matches=None)
        fig1date_cut.update_layout(font_size=16)
        fig1date_cut.update_xaxes(fixedrange=True)
        fig1date_cut.update_yaxes(fixedrange=True)
        fig1date_cut.update_layout(showlegend=False)
        fig1date_cut.update_layout(template="plotly")
        fig1date_cut.update_layout(margin=dict(t=125))

        st.plotly_chart(fig1date_cut, use_container_width=True)

else:
    c1, c2 = st.columns([2,1])
    df5day_cut = df5day_cut[~df5day_cut["alue"].isin(["A", "B", "K", "U", "S"])]

    with c1:
        fig2date_cut = px.bar(df5day_cut, x="day", y="speed", height=940, category_orders={"day":["Ma","Ti","Ke","To","Pe","La","Su"]}, 
        title="<b>Nopeus viikonpäivän mukaan, kun käytetty aika on vähintään 4 h", color="day", facet_col="alue", facet_col_wrap=4, facet_row_spacing=0.05, hover_data={"alue":False},
        color_discrete_sequence=["#636EFA", "#636EFA", "#636EFA", "#636EFA", "#636EFA", "#EF553B", "#EF553B"],
        labels={"speed":"Nopeus", "day":"Päivä"})

        fig2date_cut.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig2date_cut.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
        fig2date_cut.update_layout(font_size=16)
        fig2date_cut.update_xaxes(fixedrange=True)
        fig2date_cut.update_yaxes(fixedrange=True)
        fig2date_cut.update_layout(showlegend=False)
        fig2date_cut.update_layout(template="plotly")

        if yax_5:
            fig2date_cut.update_yaxes(matches=None) 

        st.plotly_chart(fig2date_cut, use_container_width=True)

with c2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Huomataan, että")
    st.write("- Viikonloppuna nopeus on pääosin sama kuin arkenakin.")
    st.write("- Alueiden välillä on tosin vaihtelua.")
    st.write("Huom! Alueista A, B, K, U ja S ei voitu tulostaa kuviota, koska niiltä oli liian vähän dataa.")


