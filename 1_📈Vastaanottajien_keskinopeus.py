import streamlit as st
import pandas as pd
import datetime as dt
from datetime import time, date
from datetime import datetime
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import math

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
st.header("Vastaanottajien keskinopeus")

st.write("Aloitetaan tarkastelemalla vastaanottajien nopeutta. Mittarina käytetään sitä, kuinka monta riviä vastaanottaja kuittaa tunnissa.")
st.write("""Voit tarkastella alueita joko erikseen tai yhteenlaskettuna aggregaattina. Voit lisäksi valita näkymään vain tietyt alueet helpompaa vertailua varten.
Huomaa myös, että datapisteiden arvot saattavat vaihdella rajusti päivästä päivään, jolloin liukuvan keskiarvon avulla saadaan laskettua pehmeämpi trendikäyrä datalle. """)
st.write("Alueiden välisen vertailun helpottamiseksi voit vapauttaa y-akselit, jolloin kaavioiden y-akselien asteikot eivät ole enää keskenään lukittuja.")

st.info("Huom! Jos sivun fontti tuntuu liian pieneltä, voit suurentaa sivua esimerkiksi painamalla näppäimistöstä Ctrl ja +.")
st.info("Huom! Jos et nää sivun vasemmassa reunassa navigointipalkkia, saat sen näkyviin sivun vasemmassa yläkulmassa olevasta nuolesta.")

st.write("---")

col1, col2, col3 = st.columns([2, 1, 1])

### haetaan data
rivispeed2 = pd.read_excel("data/rivispeed2.xlsx")
df1 = rivispeed2[rivispeed2["cumtotal"]>0.5].groupby(["alue", "date"]).agg({"speed":"mean", "Hlö":"count"}).reset_index()
df1 = df1[df1["speed"]<100]
df1 = df1.sort_values(by=["alue", "date"])

### filtterit: ma ja y-akseli
with col2:
    ma_1 = st.slider("**Liukuva keskiarvo:**", 0, 100, 20, 5)

df1_2 = df1.copy()

### ma luominen count rajausta varten
if ma_1 > 0:
    df1["ma"] = df1.groupby(["alue"])["speed"].transform(lambda x: x.rolling(ma_1).mean())
    df1["ma"] = df1["ma"].round(1)
else:
   df1["ma"] = df1["speed"].copy()
df1.dropna(inplace=True)

### aluerajaus countin mukaan
alueet2 = df1.groupby("alue")["ma"].count().reset_index(name="count")
alueet2 = alueet2[alueet2["count"]>5]
alueet2 = alueet2["alue"].values.tolist()
# alueet2.sort_values(by="alue")
# st.write(alueet2)
### aluefilter
alueet = df1_2["alue"].unique()

subcol1, subcol2, subcol3 = st.columns([1, 5, 2])

with col3:
    alueview = st.radio(label="**Näkymä:**", 
        options=["Kaikki alueet yhteensä", "Tarkastele alueita erikseen"], 
        key="alueview",
        index=1
        )

if alueview =="Kaikki alueet yhteensä":
    kaikkiyht = True
else:
    kaikkiyht = False


with col1:
    container = st.container()

with subcol1:
    container2 = st.container()


if kaikkiyht:
    all = container2.checkbox("Valitse kaikki", value=True, disabled=True)
else:
    all = container2.checkbox("Valitse kaikki", value=True)


with col1:
    if all or kaikkiyht:
        alsel_1 = container.multiselect("**Valitse alueet**", options=alueet, default=alueet, key="id2", disabled=True)
    else:
        alsel_1 = container.multiselect("**Valitse alueet**", options=alueet, default=alueet, key="id1")

### yakseli filtteri
with subcol3:
    if not kaikkiyht:
        yax_1 = st.checkbox("Vapauta y-akselit", key="yax_1")
    else:
        yax_1 = st.checkbox("Vapauta y-akselit", value=False, disabled=True, key="yax_2")

### ma luominen
if ma_1 > 0:
    df1_2["ma"] = df1_2.groupby(["alue"])["speed"].transform(lambda x: x.rolling(ma_1).mean())
    df1_2["ma"] = df1_2["ma"].round(1)
else:
   df1_2["ma"] = df1_2["speed"].copy().round(1)
df1_2.dropna(inplace=True)

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

###

if not kaikkiyht:
    df1_2 = df1_2[df1_2["alue"].isin(alsel_1)]
    df1_2 = df1_2[df1_2["alue"].isin(common_member(alueet2, alsel_1))]
else:
    df1_2 = rivispeed2[rivispeed2["cumtotal"]>0.5].groupby("date")["speed"].mean().reset_index()
    df1_2 = df1_2.sort_values(by="date")
    df1_2["ma"] = df1_2.speed.rolling(ma_1).mean()
    df1_2["alue"] = "Kaikki yhteensä"
    if ma_1 == 0:
        df1_2["ma"] = df1_2["speed"].copy()

# st.write(df1_2)


### kaavion luominen
n = len(common_member(alueet2, alsel_1))
rows = math.ceil(n/5)
if rows > 1:
    h = 166*(rows)+183
else:
    h = -113*n+913

if kaikkiyht or rows==1 and n==1:
    h=700


df1_2["pvm"] = df1_2["date"].dt.strftime("%d.%m.%Y")
# st.write(df1_2)

try:
    fig1 = px.line(df1_2, x="date", y="ma", facet_col="alue", height=h, labels={"ma":"Nopeus", "alue":"Alue", "date":"päivä", "pvm":"Päivä"},
    facet_col_wrap=5, facet_row_spacing=0.035, hover_data={"alue":False, "date":False, "pvm":True}
    # range_x=[dt.datetime(2022,1,1), dt.datetime(2022,11,14)]
    )
except:
    st.text("Valitse alue!")

try:
    fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig1.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
    fig1.update_layout(font_size=14)
    fig1.update_layout(margin=dict(b=0))
    fig1.add_trace(go.Scatter(x=[dt.datetime(2022,1,1)], y=[df1_2["ma"].mean()], mode="markers", marker=dict(opacity=0)))
    fig1.update_layout(showlegend=False)
    fig1.update_xaxes(tickformat="%m/%Y")
    fig1.update_xaxes(fixedrange=True)
    fig1.update_yaxes(fixedrange=True)
    fig1.update_layout(template="plotly")
    
    if kaikkiyht or rows==1 and n==1:
        fig1.update_layout(margin=dict(
            b=0,
            l=200,
            r=200
            )
            )

    if yax_1 == True:
        fig1.update_yaxes(matches=None)


    st.plotly_chart(fig1, use_container_width=True)
except:
    st.text("")

if not kaikkiyht:
    if len(uncommon_member(alsel_1, alueet2)) > 0:
        wch_colour_box = (256,0,0)
        wch_colour_font = (256,256,256)
        fontsize = 14
        text = "-- " + "Seuraavista alueista ei voitu tulostaa kuviota, koska niistä oli liian vähän dataa: [" + ", ".join(uncommon_member(alsel_1, alueet2))+ "]. Koita säätää liukuva keskiarvo pienemmäksi. --"
        iconname = "fas fa-asterisk"

        htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                    {wch_colour_box[1]}, 
                                                    {wch_colour_box[2]}); 
                                color: rgb({wch_colour_font[0]}, 
                                        {wch_colour_font[1]}, 
                                        {wch_colour_font[2]}); 
                                font-size: {fontsize}px; 
                                font-family: "Source Code Pro;
                                <i class='{iconname} fa-xs'></i> {text}"""

        # st.markdown(htmlstr, unsafe_allow_html=True)
        st.error("-- " + "Seuraavista alueista ei voitu tulostaa kuviota, koska niistä oli liian vähän dataa: [" + ", ".join(uncommon_member(alsel_1, alueet2))+ "]. Koita säätää liukuva keskiarvo pienemmäksi. --")
        # st.text("-- Koita säätää liukuva keskiarvo pienemmäksi --")
        st.write("")

st.write("")
st.subheader("**Huomataan, että**")
st.write("- monilla alueilla (esim. 1, 2 ja H) hyllytysnopeus on hidastunut vuoden myötä")
st.write("- erityisen suuri pudotus nopeudessa on tapahtunut kesä-heinäkuun tienoilla")
st.write("- muutamilla alueilla (esim. J ja P) nopeus on parantunut") 

# st.markdown("""
# <style>
# .big-font {
#     font-size:20px !important;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown('<p class="big-font">Hello World !!</p>', unsafe_allow_html=True)


