import streamlit as st
import pandas as pd
import datetime as dt
from datetime import time, date
from datetime import datetime
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import math
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


st.header("Saapuvan tavaran käsittelyaikoja")

grafiikka = Image.open("./saapumiset grafiikka v2.png")


textcol1, textcol2 = st.columns([1,1])

with textcol1:
    st.write("Saapuvan tavaran osalta aineistossa tarjottiin kolmea keskeistä päivämäärää: saapumispäivä, hyllytyksen aloittamispäivä ja hyllytyksen lopettamispäivä.")
    # st.write("- Saapumispäivä")
    # st.write("- Hyllytyksen aloittamispäivä")
    # st.write("- Hyllytyksen lopettamispäivä")
    st.write("Analyysissä käytetään käsitteitä kokonaisaika, odotusaika ja hyllytysaika. Oheisessa grafiikassa on esitetty käsitteiden merkitys.")
    st.write("""Tutkitaan näillä mittareilla, miten saapuvan tavaran käsittelynopeus on kehittynyt. 
    X-akselilla esitetty päivämäärä on hyllytyksen lopettamispäivä.""")

with textcol2:
    st.image(grafiikka)

# st.write("")
# st.write("")
# st.markdown("#")

st.write("---")

col1, col2, col3 = st.columns([2, 1, 1])

### haetaan data
saapumiset_df = pd.read_excel("./saapumiset_df.xlsx")
saapumiset_df["alue"] = saapumiset_df["alue"].astype(str)

koktime_df = saapumiset_df.groupby(["alue","hyllytys_end_dt"])["koktime"].mean().reset_index().sort_values(by=["alue","hyllytys_end_dt"])
waittime_df = saapumiset_df.groupby(["alue","hyllytys_end_dt"])["waittime"].mean().reset_index().sort_values(by=["alue","hyllytys_end_dt"])
hyltime_df = saapumiset_df.groupby(["alue","hyllytys_end_dt"])["hyltime"].mean().reset_index().sort_values(by=["alue","hyllytys_end_dt"])


### filtterit: ma ja y-akseli
with col2:
    ma_1 = st.slider("**Liukuva keskiarvo:**", 0, 100, 20, 5)

koktime_df_2 = koktime_df.copy()
waittime_df_2 = waittime_df.copy()
hyltime_df_2 = hyltime_df.copy()

### ma luominen count rajausta varten
if ma_1 > 0:
    koktime_df["ma"] = koktime_df.groupby(["alue"])["koktime"].transform(lambda x: x.rolling(ma_1).mean())
    koktime_df["ma"] = koktime_df["ma"].round(1)

    waittime_df["ma"] = waittime_df.groupby(["alue"])["waittime"].transform(lambda x: x.rolling(ma_1).mean())
    waittime_df["ma"] = waittime_df["ma"].round(1)

    hyltime_df["ma"] = hyltime_df.groupby(["alue"])["hyltime"].transform(lambda x: x.rolling(ma_1).mean())
    hyltime_df["ma"] = hyltime_df["ma"].round(1)
else:
   koktime_df["ma"] = koktime_df["koktime"].copy()
   waittime_df["ma"] = waittime_df["waittime"].copy()
   hyltime_df["ma"] = hyltime_df["hyltime"].copy()

koktime_df.dropna(inplace=True)
waittime_df.dropna(inplace=True)
hyltime_df.dropna(inplace=True)

### aluerajaus countin mukaan
alueet2_koktime = koktime_df.groupby("alue")["ma"].count().reset_index(name="count")
alueet2_koktime = alueet2_koktime[alueet2_koktime["count"]>5]
alueet2_koktime = alueet2_koktime["alue"].values.tolist()

alueet2_waittime = waittime_df.groupby("alue")["ma"].count().reset_index(name="count")
alueet2_waittime = alueet2_waittime[alueet2_waittime["count"]>5]
alueet2_waittime = alueet2_waittime["alue"].values.tolist()

alueet2_hyltime = hyltime_df.groupby("alue")["ma"].count().reset_index(name="count")
alueet2_hyltime = alueet2_hyltime[alueet2_hyltime["count"]>5]
alueet2_hyltime = alueet2_hyltime["alue"].values.tolist()

### aluefilter
alueet = koktime_df_2["alue"].unique()

subcol1, subcol2, subcol3 = st.columns([1, 5, 2])

with col3:
    alueview = st.radio(label="**Näkymä:**", 
        options=["Kaikki alueet yhteensä", "Tarkastele alueita erikseen"], 
        key="alueview",
        index=0
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
        alsel_1 = container.multiselect("**Valitse alueet**", options=alueet, default=alueet, key="id71", disabled=True)
    else:
        alsel_1 = container.multiselect("**Valitse alueet**", options=alueet, default=alueet, key="id72")

### yakseli filtteri
with subcol3:
    # if not kaikkiyht:
        yax_1 = st.checkbox("Vapauta y-akselit", key="yax_71")
    # else:
    #     yax_1 = st.checkbox("Vapauta y-akselit", key="yax_71", value=True, disabled=True)

### ma luominen

if ma_1 > 0:
    koktime_df_2["ma"] = koktime_df_2.groupby(["alue"])["koktime"].transform(lambda x: x.rolling(ma_1).mean())
    koktime_df_2["ma"] = koktime_df_2["ma"].round(1)

    waittime_df_2["ma"] = waittime_df_2.groupby(["alue"])["waittime"].transform(lambda x: x.rolling(ma_1).mean())
    waittime_df_2["ma"] = waittime_df_2["ma"].round(1)

    hyltime_df_2["ma"] = hyltime_df_2.groupby(["alue"])["hyltime"].transform(lambda x: x.rolling(ma_1).mean())
    hyltime_df_2["ma"] = hyltime_df_2["ma"].round(1)
else:
   koktime_df_2["ma"] = koktime_df_2["koktime"].copy()
   waittime_df_2["ma"] = waittime_df_2["waittime"].copy()
   hyltime_df_2["ma"] = hyltime_df_2["hyltime"].copy()

koktime_df_2.dropna(inplace=True)
waittime_df_2.dropna(inplace=True)
hyltime_df_2.dropna(inplace=True)

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


### alueselect
if not kaikkiyht:
    koktime_df_2 = koktime_df_2[koktime_df_2["alue"].isin(alsel_1)]
    koktime_df_2 = koktime_df_2[koktime_df_2["alue"].isin(common_member(alueet2_koktime, alsel_1))]

    waittime_df_2 = waittime_df_2[waittime_df_2["alue"].isin(alsel_1)]
    waittime_df_2 = waittime_df_2[waittime_df_2["alue"].isin(common_member(alueet2_waittime, alsel_1))]

    hyltime_df_2 = hyltime_df_2[hyltime_df_2["alue"].isin(alsel_1)]
    hyltime_df_2 = hyltime_df_2[hyltime_df_2["alue"].isin(common_member(alueet2_hyltime, alsel_1))]
else:
    koktime_df_2 = saapumiset_df.groupby("hyllytys_end_dt")["koktime"].mean().reset_index().sort_values(by="hyllytys_end_dt")
    koktime_df_2["ma"] = koktime_df_2.koktime.rolling(ma_1).mean()
    koktime_df_2["alue"] = "Kaikki yhteensä"

    waittime_df_2 = saapumiset_df.groupby("hyllytys_end_dt")["waittime"].mean().reset_index().sort_values(by="hyllytys_end_dt")
    waittime_df_2["ma"] = waittime_df_2.waittime.rolling(ma_1).mean()
    waittime_df_2["alue"] = "Kaikki yhteensä"

    hyltime_df_2 = saapumiset_df.groupby("hyllytys_end_dt")["hyltime"].mean().reset_index().sort_values(by="hyllytys_end_dt")
    hyltime_df_2["ma"] = hyltime_df_2.hyltime.rolling(ma_1).mean()
    hyltime_df_2["alue"] = "Kaikki yhteensä"
    if ma_1 == 0:
        koktime_df_2["ma"] = koktime_df_2["koktime"].copy()
        waittime_df_2["ma"] = waittime_df_2["waittime"].copy()
        hyltime_df_2["ma"] = hyltime_df_2["hyltime"].copy()


### chartin y_range
allvalues = list(koktime_df_2["ma"].dropna()) + list(waittime_df_2["ma"].dropna()) + list(hyltime_df_2["ma"].dropna())

if kaikkiyht:
    if min(allvalues) == 0:
        ylim = [0, max(allvalues)*1.05]
    else:
        ylim = [min(allvalues)*0.5, max(allvalues)*1.05]


### facetkaavion luominen
def luo_facetkaavio(df, alueet2, ma_label, title):
    n = len(common_member(alueet2, alsel_1))
    rows = math.ceil(n/5)
    if rows > 1:
        h = 166*(rows)+183
    else:
        h = -113*n+913

    if kaikkiyht or rows==1 and n==1:
        h=700


    df["pvm"] = df["hyllytys_end_dt"].dt.strftime("%d.%m.%Y")

    try:
        fig1 = px.line(df, x="hyllytys_end_dt", y="ma", facet_col="alue", height=h, 
        labels={"ma":ma_label + " (päivää)", "alue":"Alue", "hyllytys_end_dt":"päivä", "pvm":"Päivä"},
        facet_col_wrap=5, facet_row_spacing=0.035, hover_data={"alue":False, "hyllytys_end_dt":False, "pvm":True},
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

    # if not kaikkiyht:
    #     if len(uncommon_member(alsel_1, alueet2)) > 0:
    #         st.error("-- Seuraavista alueista ei voitu tulostaa kuviota, koska niistä oli liian vähän dataa: [" + ", ".join(uncommon_member(alsel_1, alueet2))+ "]. Koita säätää liukuva keskiarvo pienemmäksi. --")
    #         st.write("")

### kaavion luominen
def luo_kaavio(df, alueet2, ma_label, title):

    df["pvm"] = df["hyllytys_end_dt"].dt.strftime("%d.%m.%Y")

    try:
        fig1 = px.line(df, x="hyllytys_end_dt", y="ma", height=520, labels={"ma":ma_label + " (päivää)", "hyllytys_end_dt":"päivä", "pvm":"Päivä"},
        hover_data={"alue":False, "hyllytys_end_dt":False, "pvm":True},
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
        
        fig1.update_layout(margin=dict(
            # b=50,
            l=50,
            r=50
            )
            )

        if yax_1 == True:
            fig1.update_yaxes(matches=None)
        else:
            fig1.update_yaxes(range=[ylim[0],ylim[1]])

        st.plotly_chart(fig1, use_container_width=True)
    except:
        st.text("")



### tulosta kaaviot

def remove_list_duplicates(x):
  return list(dict.fromkeys(x))

if not kaikkiyht:
    luo_facetkaavio(koktime_df_2, alueet2_koktime, "Kokonaisaika", "Kokonaisajan kehitys")
    luo_facetkaavio(waittime_df_2, alueet2_waittime, "Odotusaika", "Odotusajan kehitys")
    luo_facetkaavio(hyltime_df_2, alueet2_hyltime, "Hyllytysaika", "Hyllytysajan kehitys")

    tulostetut_alueet = alueet2_koktime + alueet2_waittime + alueet2_hyltime
    tulostetut_alueet = remove_list_duplicates(tulostetut_alueet)

    if len(uncommon_member(alsel_1, tulostetut_alueet)) > 0:
        st.error("-- Seuraavista alueista ei voitu tulostaa kuviota, koska niistä oli liian vähän dataa: [" + ", ".join(uncommon_member(alsel_1, tulostetut_alueet))+ "]. Koita säätää liukuva keskiarvo pienemmäksi. --")
        st.write("")
else:
    c0, cbox_c1, cbox_c2, c4 = st.columns([1, 4, 4, 1])
    with cbox_c1:
        luo_kaavio(koktime_df_2, alueet2_koktime, "Kokonaisaika", "Kokonaisajan kehitys")
        luo_kaavio(hyltime_df_2, alueet2_hyltime, "Hyllytysaika", "Hyllytysajan kehitys")

    with cbox_c2:
        luo_kaavio(waittime_df_2, alueet2_waittime, "Odotusaika", "Odotusajan kehitys")


st.write("")
st.subheader("Huomataan, että")
st.write("- Saapuvan tavaran purkamisprosessi on hidastunut vuoden mittaan huomattavasti.")
st.write("- Pääosin tämä johtuu odotusajan noususta. Tavaraa siis kasaantuu varastolle entistä enemmän.")
st.write("- Suurin huippu nähtiin elokuussa.")
st.write("- Myös hyllytysaika on kasvanut noin kahdesta päivästä pahimmillaan jopa neljään päivään.")