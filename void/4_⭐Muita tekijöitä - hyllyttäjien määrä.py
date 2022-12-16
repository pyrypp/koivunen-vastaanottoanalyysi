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
st.header("Hyllyttäjien määrän vaikutus nopeuteen")

st.write("Tutkitaan kuinka nopeasti alueen vastaanottajat keskimäärin hyllyttävät, kun alueella on samanaikasesti x määrä vastaanottajia hyllyttämässä.")
st.write("Nopeuden yksikkö riviä/tunti.")

### valinnat
col1, col2 = st.columns([2, 1])

with col1:
    alueview = st.radio(label="**Näkymä:**", 
        options=["Kaikki alueet yhteensä", "Tarkastele alueita erikseen"], 
        key="alueview4",
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
        yax_3 = st.checkbox("Vapauta akselit", key="yax_5", value=True)
    else:
        yax_3 = st.checkbox("Vapauta akselit", value=True, disabled=True, key="yax_6")

### haetaan data
df3 = pd.read_excel("./vamäärä_hylspeed.xlsx")

df3 = df3.groupby(["alue", "date", "Hlöcount"])["speed"].mean().reset_index()
df3 = df3.groupby(["alue", "Hlöcount"])["speed"].mean().reset_index()

if kaikkiyht:
    df3 = df3.groupby(["Hlöcount"])["speed"].mean().reset_index()

df3["speed"] = df3["speed"].round(1)


if not yax_3:
    df3 = df3[df3["speed"]<100]

### kaaviot

if kaikkiyht:
    c0, c1, c2 = st.columns([1,2.8,1])
    with c1:
        fig1 = px.scatter(df3, x="Hlöcount", y="speed", height=650, trendline="ols",
        labels={"speed":"Nopeus", "Hlöcount":"Alueella olevien hyllyttäjien määrä"})

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
        fig1 = px.scatter(df3, x="Hlöcount", y="speed", facet_col="alue", facet_col_wrap=6,
        height=900, trendline="ols", facet_row_spacing=0.05, hover_data={"alue":False},
        labels={"speed":"Nopeus", "Hlöcount":"Hyllyttäjien määrä"})

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

        if yax_3:
            fig1.update_xaxes(matches=None)
            fig1.update_yaxes(matches=None)            

        st.plotly_chart(fig1, use_container_width=True)


st.write("")
st.subheader("Huomataan, että")
st.write("- Pääosin suurempi määrä vastaanottajia johtaa parempaan työtehokkuuteen.")
st.write("- Alueiden välillä on tosin vaihtelua.")