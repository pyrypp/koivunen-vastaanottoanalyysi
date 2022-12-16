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


st.header("Keskeneräiset erät")

tc1, tc2 = st.columns([2,1])

with tc1:
    st.write("""Tarkastellaan, kuinka monta keskeneräistä erää varastolla on ollut minäkin ajanhetkenä. Keskeneräinen erä on sellainen, 
    jonka hyllytystä ei ole vielä aloitettu tai jota ei ole vielä kokonaan hyllytetty.""")
    st.write("Koska dataa on vain vuodelta 2022, tieto keskeneräisistä eristä vuoden ensimmäisten kuukausien osalta ei ole täysin tarkka.")
    st.write("Kaavioissa on käytetty 10 päivän liukuvaa keskiarvoa.")

### valinnat
col1, col2 = st.columns([2, 1])

with col1:
    alueview = st.radio(label="**Näkymä:**", 
        options=["Kaikki alueet yhteensä", "Tarkastele alueita erikseen"], 
        key="alueview8",
        index=0
        )


if alueview =="Kaikki alueet yhteensä":
    kaikkiyht8 = True
else:
    kaikkiyht8 = False


### yakseli filtteri
with col2:
    st.write("")
    st.write("")
    yax_8 = st.checkbox("Vapauta y-akselit", key="yax_81")


### haetaan data
# df5day = pd.read_excel("data/rivispeed2.xlsx")

if kaikkiyht8:
    df_kaikki = pd.read_excel("data/keskeneräiset_kaikki.xlsx")
    df_odottavat = pd.read_excel("data/keskeneräiset_odottavat.xlsx")
    df_hyllytys = pd.read_excel("data/keskeneräiset_hyllytys.xlsx")
else:
    df_kaikki = pd.read_excel("data/keskeneräiset_kaikki_a.xlsx")
    df_odottavat = pd.read_excel("data/keskeneräiset_odottavat_a.xlsx")
    df_hyllytys = pd.read_excel("data/keskeneräiset_hyllytys_a.xlsx")


### chartin y_range
allvalues = list(df_kaikki["ma"].dropna()) + list(df_odottavat["ma"].dropna()) + list(df_hyllytys["ma"].dropna())

if kaikkiyht8:
    if min(allvalues) == 0:
        ylim = [0, max(allvalues)*1.05]
    else:
        ylim = [min(allvalues)*0.5, max(allvalues)*1.05]
    

### kaaviot
def luo_kaavio(df, title):

    df["pvm"] = df["dt"].dt.strftime("%d.%m.%Y")
    df["ma"] = df["ma"].round(1)

    try:
        fig1 = px.line(df, x="dt", y="ma", height=520, 
        hover_data={"dt":False, "pvm":True}, labels={"ma":"Erien määrä", "dt":"päivä", "pvm":"Päivä"},
        title="<b>" + title)
    except:
        st.text("Valitse alue!")

    try:
        fig1.update_layout(font_size=14)
        fig1.update_layout(margin=dict(b=0))
        fig1.add_trace(go.Scatter(x=[dt.datetime(2022,1,1)], y=[df["ma"].mean()], mode="markers", marker=dict(opacity=0)))
        fig1.update_layout(showlegend=False)
        fig1.update_xaxes(tickformat="%m/%Y")
        fig1.update_xaxes(fixedrange=True)
        fig1.update_yaxes(fixedrange=True)
        fig1.update_layout(template="plotly")
        
        fig1.update_layout(margin=dict(
            # b=50,
            l=50,
            r=50
            )
            )

        if yax_8 == True:
            fig1.update_yaxes(matches=None)
        else:
            fig1.update_yaxes(range=[ylim[0],ylim[1]])

        st.plotly_chart(fig1, use_container_width=True)
    except:
        st.text("")


### facetkaavion luominen
def luo_facetkaavio(df, title):

    df["pvm"] = df["dt"].dt.strftime("%d.%m.%Y")
    df["ma"] = df["ma"].round(1)
    df = df.dropna()
    df2 = df.groupby("alue")["ma"].count().reset_index(name="count")
    aluedel = df2[df2["count"]<12]["alue"]
    df = df[~df["alue"].isin(aluedel)]

    try:
        fig1 = px.line(df, x="dt", y="ma", facet_col="alue", height=820, 
        facet_col_wrap=5, facet_row_spacing=0.035, hover_data={"alue":False, "dt":False, "pvm":True},
        labels={"ma":"Erien määrä", "dt":"päivä", "pvm":"Päivä", "alue":"Alue"},
        title="<b>" + title)
    except:
        st.text("Valitse alue!")

    try:
        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig1.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
        fig1.update_layout(font_size=14)
        fig1.update_layout(margin=dict(b=0))
        fig1.add_trace(go.Scatter(x=[dt.datetime(2022,1,1)], y=[df["ma"].mean()], mode="markers", marker=dict(opacity=0)))
        fig1.update_layout(showlegend=False)
        fig1.update_xaxes(tickformat="%m/%Y")
        fig1.update_xaxes(fixedrange=True)
        fig1.update_yaxes(fixedrange=True)
        fig1.update_layout(template="plotly")
        
        if yax_8 == True:
            fig1.update_yaxes(matches=None)


        st.plotly_chart(fig1, use_container_width=True)
    except:
        st.text("")


### tulosta kaaviot
if kaikkiyht8:
    c0, cbox_c1, cbox_c2, c4 = st.columns([1, 4, 4, 1])
    with cbox_c1:
        luo_kaavio(df_kaikki, "Kaikki keskeneräiset erät")
        luo_kaavio(df_hyllytys, "Hyllytysvaiheessa olevat erät")

    with cbox_c2:
        luo_kaavio(df_odottavat, "Aloittamattomat erät")
else:
    luo_facetkaavio(df_kaikki, "Kaikki keskeneräiset erät")
    luo_facetkaavio(df_odottavat, "Aloittamattomat erät")
    luo_facetkaavio(df_hyllytys, "Hyllytysvaiheessa olevat erät")


st.subheader("Huomataan, että")
st.write("- Keskeneräisten lähetysten määrä varastolla on kasvanut vuoden myötä.")
st.write("- Aloittamattomia eriä on kasaantunut varastolle erityisesti heinäkuussa.")
st.write("- Määrällisesti ongelma korostuu 1-alueella.")