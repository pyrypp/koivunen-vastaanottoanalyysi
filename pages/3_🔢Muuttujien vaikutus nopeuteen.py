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
st.header("Muuttujien vaikutus hyllytysnopeuteen")

tcol11, tcol12 = st.columns([3,1])
with tcol11:
    st.write("""Tarkastellaan, miten hyllytetty paino, kappalemäärä ja rivimäärä vaikuttavat vastaanottajan nopeuteen.
    Yksikkönä käytetään hyllytettyjä rivejä per tunti. Nopeus sekä hyllytetty paino, kappalemäärä ja rivimäärä on laskettu vastaanottajan koko päivän summasta.""")

    st.write("Huomaa kilo- ja kappalemäärän logaritmiset asteikot.")


col1, col2, col3 = st.columns([30, 1, 20])

### haetaan data
rivispeed2 = pd.read_excel("./rivispeed2.xlsx")
alueet = rivispeed2["alue"].unique()
df2 = rivispeed2.copy()
df2 = df2[df2["speed"]<100]

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
        alsel_2 = container.multiselect("**Valitse alueet**", options=alueet, default=alueet, key="id2", disabled=True,
        help=help
        )
    else:
        alsel_2 = container.multiselect("**Valitse alueet**", options=alueet, default=alueet, key="id1")

### dataframet
df2["alue"] = df2["alue"].astype(str)
df2["netpainosum"] = df2["netpainosum"].round(0)
df2["rivicount"] = df2["rivicount"].round(0)
df2["Kplsum"] = df2["Kplsum"].round(0)
df2 = df2[df2["netpainosum"]>0]
df2 = df2[df2["rivicount"]>0]
df2 = df2[df2["Kplsum"]>0]
df2 = df2[df2["alue"].str.len()==1]

bins = np.arange(0, 10000, 10)

if kaikkiyht:
    df_paino = df2.groupby(pd.cut(df2["netpainosum"], bins=bins, labels=bins[:-1]))["speed"].mean().reset_index().dropna()
    df_rivi = df2.groupby(pd.cut(df2["rivicount"], bins=bins, labels=bins[:-1]))["speed"].mean().reset_index().dropna()
    df_kpl = df2.groupby(pd.cut(df2["Kplsum"], bins=bins, labels=bins[:-1]))["speed"].mean().reset_index().dropna()

    df_paino["netpainosum"] = df_paino["netpainosum"].astype(int)
    df_rivi["rivicount"] = df_rivi["rivicount"].astype(int)
    df_kpl["Kplsum"] = df_kpl["Kplsum"].astype(int)
else:
    df2 = df2[df2["alue"].isin(alsel_2)]
    df_paino = df2.groupby(["alue", pd.cut(df2["netpainosum"], bins=bins, labels=bins[:-1])]).agg({"speed":"mean"}).reset_index()
    df_paino["netpainosum"] = df_paino["netpainosum"].astype(int)
    df_paino.dropna(inplace=True)

    df_rivi = df2.groupby(["alue", pd.cut(df2["rivicount"], bins=bins, labels=bins[:-1])]).agg({"speed":"mean"}).reset_index()
    df_rivi["rivicount"] = df_rivi["rivicount"].astype(int)
    df_rivi.dropna(inplace=True)

    df_kpl = df2.groupby(["alue", pd.cut(df2["Kplsum"], bins=bins, labels=bins[:-1])]).agg({"speed":"mean"}).reset_index()
    df_kpl["Kplsum"] = df_kpl["Kplsum"].astype(int)
    df_kpl.dropna(inplace=True)

df_paino["speed"] = df_paino["speed"].round(1)
df_rivi["speed"] = df_rivi["speed"].round(1)
df_kpl["speed"] = df_kpl["speed"].round(1)

###

def power(x, a, b):
    return a*x**b
    
t = np.linspace(1, 10000, 10000)

###

n2 = len(alsel_2)
rows2 = math.ceil(n2/6)

if rows2 > 1:
    h2 = 165*(rows2)+200
else:
    h2 = -87.5*n2+875

frs = -0.0225*rows2+0.125


### kaavioden luominen!
if kaikkiyht:
    c0, cbox_c1r1, cbox_c2r1, c4 = st.columns([1, 4, 4, 1])
    h=520
    fs=15

    with cbox_c1r1:
        fig1 = px.scatter(df_paino, x="netpainosum", y="speed", log_x=True, log_y=True, range_x=[1,10000], range_y=[1,100],
        height=h, title="Paino x nopeus", labels={"speed":"Nopeus", "netpainosum":"Paino (kg)"})

        fig1.add_trace(go.Scatter(x=t, y=power(t, 67.595, -0.232), line=dict(dash="dash", width=3), name="suuntaviiva"))

        fig1.update_traces(line_color="red")
        fig1.update_xaxes(matches=None)
        fig1.update_yaxes(matches=None)
        fig1.update_layout(font_size=fs)
        fig1.update_xaxes(fixedrange=True)
        fig1.update_yaxes(fixedrange=True)
        fig1.update_layout(showlegend=False)
        fig1.update_layout(template="plotly")
        fig1.update_layout(margin=dict(
            # b=20,
            r=50,
            l=50,
            t=50
        ))

        st.plotly_chart(fig1, use_container_width=True)

    with cbox_c2r1:
        fig2 = px.scatter(df_kpl, x="Kplsum", y="speed", log_x=True, log_y=True, range_x=[1,10000], range_y=[1,100],
        height=h, title="Kappalemäärä x nopeus", labels={"speed":"Nopeus", "Kplsum":"Kpl"})

        fig2.add_trace(go.Scatter(x=t, y=power(t, 31.092, -0.096), line=dict(dash="dash", width=3), name="suuntaviiva"))

        fig2.update_traces(line_color="red")
        fig2.update_xaxes(matches=None)
        fig2.update_yaxes(matches=None)
        fig2.update_layout(font_size=fs)
        fig2.update_xaxes(fixedrange=True)
        fig2.update_yaxes(fixedrange=True)
        fig2.update_layout(showlegend=False)
        fig2.update_layout(template="plotly")
        fig2.update_layout(margin=dict(
            # b=20,
            r=50,
            l=50,
            t=50
        ))

        st.plotly_chart(fig2, use_container_width=True)

    with cbox_c1r1:
        fig3 = px.scatter(df_rivi, x="rivicount", y="speed", trendline="ols",
        height=h, title="Rivimäärä x nopeus", labels={"speed":"Nopeus", "rivicount":"Rivimäärä"})

        # fig3.add_trace(go.Scatter(x=t, y=power(t, 67.595, -0.232), line=dict(dash="dash", width=3)))

        fig3.update_traces(line=dict(dash="dash", width=3, color="red"))
        fig3.update_xaxes(matches=None)
        fig3.update_yaxes(matches=None)
        fig3.update_layout(font_size=fs)
        fig3.update_xaxes(fixedrange=True)
        fig3.update_yaxes(fixedrange=True)
        fig3.update_layout(showlegend=False)
        fig3.update_layout(template="plotly")
        fig3.update_layout(margin=dict(
            # b=50,
            r=50,
            l=50,
            t=50
        ))

        st.plotly_chart(fig3, use_container_width=True)



### kaavioiden luominen facet

try:
    if not kaikkiyht:
        fig1 = px.scatter(df_paino, x="netpainosum", y="speed", facet_col="alue", facet_col_wrap=6, facet_row_spacing=frs,
        log_x=True, log_y=True, hover_data={"alue":False},
        height=h2, title="<b>Paino x nopeus", labels={"speed":"Nopeus", "netpainosum":"Paino (kg)"}, trendline="lowess")

        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig1.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
        fig1.update_traces(line_color="red")
        fig1.update_xaxes(matches=None)
        fig1.update_yaxes(matches=None)
        fig1.update_layout(font_size=14)
        fig1.update_xaxes(fixedrange=True)
        fig1.update_yaxes(fixedrange=True)
        fig1.update_layout(showlegend=False)
        fig1.update_layout(template="plotly")

        st.plotly_chart(fig1, use_container_width=True)

        #

        fig2 = px.scatter(df_kpl, x="Kplsum", y="speed", facet_col="alue", facet_col_wrap=6, facet_row_spacing=frs,
        log_x=True, log_y=True, hover_data={"alue":False},
        height=h2, title="<b>Kappalemäärä x nopeus", labels={"speed":"Nopeus", "Kplsum":"Kappalemäärä"}, trendline="lowess")

        fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig2.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
        fig2.update_traces(line_color="red")
        fig2.update_xaxes(matches=None)
        fig2.update_yaxes(matches=None)
        fig2.update_layout(font_size=14)
        fig2.update_xaxes(fixedrange=True)
        fig2.update_yaxes(fixedrange=True)
        fig2.update_layout(showlegend=False)
        fig2.update_layout(template="plotly")

        st.plotly_chart(fig2, use_container_width=True)

        #

        fig3 = px.scatter(df_rivi, x="rivicount", y="speed", facet_col="alue", facet_col_wrap=6, facet_row_spacing=frs,
        hover_data={"alue":False},
        # log_x=True, log_y=True, 
        height=h2, title="<b>Rivimäärä x nopeus", labels={"speed":"Nopeus", "rivicount":"Rivimäärä"}, trendline="ols")

        fig3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig3.for_each_annotation(lambda a: a.update(text="Alue: <b>" + a["text"]))
        fig3.update_traces(line_color="red")
        fig3.update_xaxes(matches=None)
        fig3.update_yaxes(matches=None)
        fig3.update_layout(font_size=14)
        fig3.update_xaxes(fixedrange=True)
        fig3.update_yaxes(fixedrange=True)
        fig3.update_layout(showlegend=False)
        fig3.update_layout(template="plotly")

        st.plotly_chart(fig3, use_container_width=True)
except:
    st.text("Valitse alue!")

tcol1, tcol2 = st.columns([2,1])
st.write("")

with tcol1:
    st.subheader("**Huomataan, että**")
    st.write("- Suuremmat kilo- ja kappalemäärät on hitaampi hyllyttää. Efekti on vahvempi painon kohdalla.")
    st.write("- Painon ja kappalemäärän merkitys näkyy erityisesti esim. 1-, 2-, H- ja V-alueilla. Vaikutukset tosin vaihtelevat. Joillain alueilla korostuu painon merkitys ja toisilla taas kappalemäärän. ")
    st.write("- Päivän aikana hyllytetyt suuremmat rivimäärät sen sijaan vaikuttavat nopeuttavan hyllytysprosessia. Alueiden välillä ei ole erityisen suurta vaihtelua.")



