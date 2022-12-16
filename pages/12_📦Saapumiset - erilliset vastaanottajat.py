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
from PIL import Image

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
st.header("Kannaattaako useamman hyllyttäjän käsitellä samaa lähetystä?")

grafiikka = Image.open("data/saapumiset grafiikka v2.png")


textcol1, textcol2 = st.columns([1,1])

with textcol1:
    st.write("Tutkitaan, kuinka moni erillinen vastaanottaja on hyllyttänyt yhtä alueelle saapunutta lähetystä ja miten tämä vaikuttaa saapumisen eri vaiheisiin.")
    st.write("""Aluekohtaisessa näkymässä jokaisen kaavion pisteen kohdalle on merkitty yksittäisten havaintopisteiden määrä eli kuinka montaa kertaa on ollut tilanne, 
    jossa lähetystä käsittelee x määrä vastaanottajia.""")

with textcol2:
    st.image(grafiikka)

st.write("---")


col1, col2, col3 = st.columns([30, 1, 20])

### haetaan data
saapumiset3 = pd.read_excel("data/saapumiset3_df.xlsx")
# saapumiset3 = saapumiset3[saapumiset3["aluecount"]<4]
alueet = saapumiset3["alue"].astype(str).sort_values().unique()


### filtterit
with col3:
    alueview = st.radio(label="**Näkymä:**", 
        options=["Kaikki alueet yhteensä", "Tarkastele alueita erikseen"], 
        key="alueview3",
        index=0
        )

if alueview =="Kaikki alueet yhteensä":
    kaikkiyht = True
else:
    kaikkiyht = False


### aluefiltteri
subcol1, subcol2, subcol3 = st.columns([1, 2, 5])

with col1:
    container = st.container()
    if kaikkiyht:
        all = st.checkbox("Valitse kaikki", disabled=True, value=True)
    else:
        all = st.checkbox("Valitse kaikki", value=True)

if all and not kaikkiyht:
    help = 'Jos haluat muuttaa aluevalintaa, poista valinta kohdasta "Valitse kaikki".'
else:
    help = ""

with col1:
    if all or kaikkiyht:
        alsel_2 = container.multiselect("**Valitse alueet**", options=alueet, default=alueet, key="idp12_1", disabled=True,
        help=help
        )
    else:
        alsel_2 = container.multiselect("**Valitse alueet**", options=alueet, default=alueet, key="idp12_2")


### dataframet
if kaikkiyht:
    koktime_df = saapumiset3.groupby("hlöcount")["koktime"].mean().reset_index()
    waittime_df = saapumiset3.groupby("hlöcount")["waittime"].mean().reset_index()
    hyltime_df = saapumiset3.groupby("hlöcount")["hyltime"].mean().reset_index()
else:
    koktime_df = saapumiset3.groupby(["hlöcount", "alue"]).agg({"hyltime":"mean", "mon":"count"}).reset_index()
    koktime_df.rename(columns={"mon":"count"}, inplace=True)

    waittime_df = saapumiset3.groupby(["hlöcount", "alue"]).agg({"waittime":"mean", "mon":"count"}).reset_index()
    waittime_df.rename(columns={"mon":"count"}, inplace=True)

    hyltime_df = saapumiset3.groupby(["hlöcount", "alue"]).agg({"hyltime":"mean", "mon":"count"}).reset_index()
    hyltime_df.rename(columns={"mon":"count"}, inplace=True)

# st.write(saapumiset3)

### kaavioden luominen!
def luo_kaavio(df, ylabel, trendline):

    y=df.columns[1]
    df[y] = df[y].round(1)

    fig = px.scatter(df, x="hlöcount", y=y, height=450, trendline=trendline, title=ylabel,
    labels={y:ylabel, "hlöcount":"Erillisten henkilöiden määrä"})

    fig.update_traces(line_color="red")
    fig.update_xaxes(matches=None)
    fig.update_yaxes(matches=None)
    fig.update_layout(font_size=15)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_layout(showlegend=False)
    fig.update_layout(template="plotly")

    st.plotly_chart(fig, use_container_width=True)


def luo_facetkaavio(df, ylabel):

    n = len(alsel_2)
    rows = math.ceil(n/6)

    if rows > 1:
        h = 165*(rows)+200
    else:
        h = -87.5*n+875

    frs = -0.0225*rows+0.125

    df["alue"] = df["alue"].astype(str)
    df = df[df["alue"].isin(alsel_2)]
    y=df.columns[2]
    df[y] = df[y].round(1)

    fig = px.scatter(df, x="hlöcount", y=y,facet_col="alue", title="<b>"+ylabel, facet_col_wrap=6, 
    facet_row_spacing=frs, height=h, labels={y:ylabel, "hlöcount":"Hlö määrä", "count":"havaintopisteitä"},
    trendline="ols", hover_data={"count":True, "alue":False})

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
    fig.update_traces(line_color="red")
    fig.update_xaxes(matches=None)
    fig.update_yaxes(matches=None)
    fig.update_layout(font_size=15)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_layout(showlegend=False)
    fig.update_layout(template="plotly")

    st.plotly_chart(fig, use_container_width=True)


###
if kaikkiyht:
    c1, c2, c3 = st.columns([1,1,1])

    with c1:
        luo_kaavio(koktime_df, "Kokonaisaika", "ols")

    with c2:
        luo_kaavio(waittime_df, "Odotusaika", "lowess")

    with c3:
        luo_kaavio(hyltime_df, "Hyllytysaika", "ols")
else:
    luo_facetkaavio(koktime_df, "Kokonaisaika")
    luo_facetkaavio(waittime_df, "Odotusaika")
    luo_facetkaavio(hyltime_df, "Hyllytysaika")



st.write("")
st.subheader("Huomataan, että")
st.write("- Mitä useampi vastaanottaja purkaa samaa erää, sitä kauemmin koko prosessissa kestää.")
st.write("- Korrelaatio näkyy aikalailla kaikkien alueiden kohdalla.")


