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
st.header("Työtuntien määrän vaikutus nopeuteen")

st.write("Katsotaan miten vastaanottajan työtuntien määrä vaikuttaa hyllytysnopeuteen. Nopeuden yksikkönä riviä/tunti.")
st.write("Nopeus ja käytetty aika laskettu päiväkohtaisesti.")

### valinnat
col1, col2 = st.columns([2, 1])

with col1:
    alueview = st.radio(label="**Näkymä:**", 
        options=["Kaikki alueet yhteensä", "Tarkastele alueita erikseen"], 
        key="alueview5",
        index=0
        )

if alueview =="Kaikki alueet yhteensä":
    kaikkiyht = True
else:
    kaikkiyht = False


### yakseli filtteri
with col2:
    st.write("")
    st.write("")
    if not kaikkiyht:
        yax_4 = st.checkbox("Vapauta akselit", key="yax_7", value=True)
    else:
        yax_4 = st.checkbox("Vapauta akselit", value=True, disabled=True, key="yax_8")

### haetaan data
df4 = pd.read_excel("./rivispeed2.xlsx")

df4["cumtotal"] = df4["cumtotal"].round(1)

if kaikkiyht:
    df4 = df4.groupby("cumtotal")["speed"].mean().reset_index()
else:
    df4 = df4.groupby(["alue", "cumtotal"])["speed"].mean().reset_index()

df4 = df4[df4["cumtotal"]>0.1][df4["speed"]<70]
df4["speed"] = df4["speed"].round(1)


### kaaviot

if kaikkiyht:
    c0, c1, c2 = st.columns([1,2.8,1])
    with c1:
        fig1 = px.scatter(df4, x="cumtotal", y="speed", height=650, trendline="lowess",
        labels={"speed":"Nopeus", "cumtotal":"Käytetty aika (h)"})

        fig1.update_traces(line_color="red")
        fig1.update_xaxes(matches=None)
        fig1.update_yaxes(matches=None)
        fig1.update_layout(font_size=16)
        fig1.update_xaxes(fixedrange=True)
        fig1.update_yaxes(fixedrange=True)
        fig1.update_layout(showlegend=False)
        fig1.update_layout(template="plotly")
        fig1.update_layout(margin=dict(
            b=50,
            # r=50,
            # l=50,
            t=50
        ))

        st.plotly_chart(fig1, use_container_width=True)

else:
    # c0, c1, c2 = st.columns([1,8,1])
    # with c1:
        fig1 = px.scatter(df4, x="cumtotal", y="speed", facet_col="alue", facet_col_wrap=6,
        height=900, trendline="lowess", facet_row_spacing=0.05, hover_data={"alue":False},
        labels={"speed":"Nopeus", "cumtotal":"Käytetty aika (h)"})

        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig1.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
        fig1.update_traces(line_color="red")
        fig1.update_layout(font_size=14)
        fig1.update_xaxes(fixedrange=True)
        fig1.update_yaxes(fixedrange=True)
        fig1.update_layout(showlegend=False)
        fig1.update_layout(template="plotly")
        fig1.update_layout(margin=dict(
            b=50,
            # r=50,
            # l=50,
            t=50
        ))

        if yax_4:
            fig1.update_xaxes(matches=None)
            fig1.update_yaxes(matches=None)            

        st.plotly_chart(fig1, use_container_width=True)


st.write("")
st.subheader("Huomataan, että")

tc1, tc2 = st.columns([2,1])

with tc1:
    st.write("- Kun vastaanottaja hyllyttää suuremman osan työpäivästä, päivän nopeus heikkenee.")
    st.write("- Korrelaatio on voimassa pääosin vain kun käytetty aika on alle neljä tuntia. Tämän jälkeen nopeuden ja käytetyn ajan välillä ei ole huomattavaa yhteyttä.")
    st.write("- Alueiden välillä ei ole erityisen suurta vaihtelua.")







##################################################################################################################################

##################################################################################################################################

##################################################################################################################################










st.write("---")

st.subheader("Tarkastellaan vielä työtuntien kehitystä vuoden ajalta.")

### valinnat
col1, col2, col25, col3 = st.columns([1, 1, 0.2, 1])

with col1:
    alueview2 = st.radio(label="**Näkymä:**", 
        options=["Kaikki alueet yhteensä", "Tarkastele alueita erikseen"], 
        key="alueview52",
        index=0
        )

if alueview2 =="Kaikki alueet yhteensä":
    kaikkiyht2 = True
else:
    kaikkiyht2 = False

### liukuva keskiarvo
with col2:
    ma_52 = st.slider("**Liukuva keskiarvo:**", 0, 100, 20, 5)

### yakseli filtteri
with col3:
    st.write("")
    st.write("")
    if not kaikkiyht2:
        yax_52 = st.checkbox("Vapauta y-akselit", key="yax_52", value=True)
    else:
        yax_52 = st.checkbox("Vapauta y-akselit", value=True, disabled=True, key="yax_52")

### haetaan data
trend_df = pd.read_excel("./rivispeed2.xlsx")
trend_df = trend_df[trend_df["day"]!="La"][trend_df["day"]!="Su"]

if ma_52 == 0:
    ma_52_2 = 1
else:
    ma_52_2 = ma_52

if kaikkiyht2:
    trend_df = trend_df.groupby("date")["cumtotal"].mean().reset_index()
else:
    trend_df = trend_df.groupby(["alue", "date"])["cumtotal"].mean().reset_index()   

trend_df["ma"] = trend_df.cumtotal.rolling(ma_52_2).mean()


if not kaikkiyht2:
    alueet = trend_df["alue"].unique()


trend_df["pvm"] = trend_df["date"].dt.strftime("%d.%m.%Y")
trend_df["ma"] = trend_df["ma"].round(3)



###

def common_member(a, b):
    result = [i for i in a if i in b]
    return result

def uncommon_member(a, b):
    temp3 = []
    for element in a:
        if element not in b:
            temp3.append(element)
    return temp3


### kaaviot

if kaikkiyht2:
    c0, c1, c2 = st.columns([1,3.5,1])
    with c1:
        fig12 = px.line(trend_df, x="date", y="ma", height=600, hover_data={"date":False, "pvm":True},
        labels={"ma":"Käytetty aika (h)", "date":"Päivä", "pvm":"Päivä"}, title="Työntekijän hyllytykseen käyttämä aika päivässä keskimäärin")

        fig12.update_xaxes(matches=None)
        fig12.update_yaxes(matches=None)
        fig12.update_layout(font_size=16)
        fig12.update_xaxes(fixedrange=True)
        fig12.update_yaxes(fixedrange=True)
        fig12.update_layout(showlegend=False)
        fig12.update_xaxes(tickformat="%m/%Y")
        fig12.update_layout(template="plotly")

        st.plotly_chart(fig12, use_container_width=True)

else:
    n = len(alueet)
    rows = math.ceil(n/5)
    if rows > 1:
        h = 220*(rows)+40
    else:
        h = -113*n+913

    if kaikkiyht2 or rows==1 and n==1:
        h=750

    fig22 = px.line(trend_df, x="date", y="ma", facet_col="alue", facet_col_wrap=5, facet_row_spacing=0.035,
    height=h, hover_data={"date":False, "pvm":True, "alue":False}, title="Työntekijän hyllytykseen käyttämä aika päivässä keskimäärin",
    labels={"ma":"Käytetty aika (h)", "date":"Päivä", "pvm":"Päivä", "alue":"Alue"})

    fig22.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig22.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
    fig22.update_layout(font_size=14)
    fig22.add_trace(go.Scatter(x=[dt.datetime(2022,1,1)], y=[trend_df["ma"].mean()], mode="markers", marker=dict(opacity=0)))
    fig22.update_xaxes(fixedrange=True)
    fig22.update_yaxes(fixedrange=True)
    fig22.update_layout(showlegend=False)
    fig22.update_xaxes(tickformat="%m/%Y")
    fig22.update_layout(template="plotly")

    if yax_52:
        fig22.update_yaxes(matches=None)

    st.plotly_chart(fig22, use_container_width=True)


st.write("")
st.subheader("Huomataan, että")
st.write("- Hyllytykseen käytetyssä ajassa nähtiin pudotus syksyllä. Muuten pysynyt melko tasaisena.")
st.write("- Alueiden välillä on jonkin verran vaihtelevuutta.")
st.write("- Pudotus hyllytykseen käytetyssä ajassa saattaa viestiä kiireestä muualla varastolla.")