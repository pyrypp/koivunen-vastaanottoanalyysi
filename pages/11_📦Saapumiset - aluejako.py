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


st.header("Lähetysten jakaminen eri alueille")

st.write("Tutkitaan, kuinka monelle alueelle saapuvat lähetykset (erilliset saap.nro) on keskimäärin jaettu.")
st.write("Katsotaan myös aluekohtaisesti, kuinka usein alueelle tulevaa tavaraa joudutaan siirtämään vielä muille alueille tai päinvastoin.")
st.write("Lisäksi tarkastellaan tämän aluejaon vaikutusta saapumisen eri vaiheiden kestoon.")

st.write("---")

### ma-slider
col0, col1, col2 = st.columns([1,2,1])

with col1:
    ma_11_slider = st.slider("**Liukuva keskiarvo:**", 0, 100, 20, 5)


### haetaan data
aluecount_timeline = pd.read_excel("data/saapumiset_aluecount_time.xlsx")
jaettualue_pros = pd.read_excel("data/jaettualue_pros.xlsx")
saapumiset2 = pd.read_excel("data/saapumiset_aluejako_vaikutukset.xlsx")

df_koktime = saapumiset2.groupby("aluecount")["koktime"].mean().reset_index()
df_waittime = saapumiset2.groupby("aluecount")["waittime"].mean().reset_index()
df_hyltime = saapumiset2.groupby("aluecount")["hyltime"].mean().reset_index()

### ma
if ma_11_slider == 0:
    ma_11 = 1
else:
    ma_11 = ma_11_slider

aluecount_timeline["ma"] = aluecount_timeline.aluecount.rolling(ma_11).mean().round(3)

###
aluecount_timeline["pvm"] = aluecount_timeline["saap_dt"].dt.strftime("%d.%m.%Y")
aluecount_timeline = aluecount_timeline[aluecount_timeline["saap_dt"]<dt.datetime(2022,11,2)]

jaettualue_pros["pros"] = jaettualue_pros["pros"].round(3)



### kaaviot
c0, c1, c2 = st.columns([1,4,1])

with c1:
    h=650
    if ma_11 != 1:
        fig1 = px.line(aluecount_timeline, x="saap_dt", y="ma", height=h, hover_data={"saap_dt":False, "pvm":True},
        labels={"ma":"Aluetta/lähetys", "saap_dt":"Päivä", "pvm":"Päivä"}, 
        title="<b>Kuinka monelle alueelle lähetykset on keskimäärin jaettu?")
    else:
        fig1 = px.scatter(aluecount_timeline, x="saap_dt", y="ma", height=h, hover_data={"saap_dt":False, "pvm":True},
        labels={"ma":"Aluetta/lähetys", "saap_dt":"Päivä", "pvm":"Päivä"}, 
        title="<b>Kuinka monelle alueelle lähetykset on keskimäärin jaettu?", trendline="lowess")

        fig1.update_traces(line_color="red")

    fig1.update_xaxes(matches=None)
    fig1.update_yaxes(matches=None)
    fig1.update_layout(font_size=16)
    fig1.update_xaxes(fixedrange=True)
    fig1.update_yaxes(fixedrange=True)
    fig1.update_layout(showlegend=False)
    fig1.update_xaxes(tickformat="%m/%Y")
    fig1.update_layout(template="plotly")

    st.plotly_chart(fig1, use_container_width=True)


    fig2 = px.bar(jaettualue_pros, x="alue", y="pros", title="<b>Alueiden välillä jaettujen lähetysten osuus",
    height=600, labels={"pros":"Prostenttiosuus", "alue":"Alue"})

    fig2.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    fig2.update_layout(font_size=16)
    fig2.update_xaxes(fixedrange=True)
    fig2.update_yaxes(fixedrange=True, tickformat="~%")
    fig2.update_layout(template="plotly")

    st.plotly_chart(fig2, use_container_width=True)

st.write("---")

shcolm, shcol = st.columns([1,3.5])
with shcol:
    st.subheader("Eri alueille jakamisen vaikutuksia lähetyksen purkamisen kestoon")

###
labelsdict = {"koktime":"Aika (päivää)", "waittime":"Aika (päivää)", "hyltime":"Aika (päivää)", 
"aluecount":"Erillisiet alueet"}
###

def luo_kaavio(df, title):
    y = df.columns[1]
    fig = px.scatter(df, x="aluecount", y=y, height=440, trendline="ols", title=title,
    labels=labelsdict)
    fig.update_layout(font_size=16)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_layout(template="plotly", title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

###
m = 0.05
c0, c1, c2, c3, c04 = st.columns([m, 1, 1, 1, m])

with c1:
    luo_kaavio(df_koktime, "Kokonaisaika")

with c2:
    luo_kaavio(df_waittime, "Odotusaika")

with c3:
    luo_kaavio(df_hyltime, "Hyllytysaika")


st.subheader("Huomataan, että")
st.write("- Aluejaossa ei ole ajan suhteen vahvaa trendiä.")
st.write("- Mitä useammalle alueelle lähetys joudutaan jakamaan, sitä pidempään koko lähetyksen purkamisessa kestää.")
st.write("- Tosin useammalle alueelle jaettavien lähetysten hyllyttäminen aloitetaan aikaisemmin.")