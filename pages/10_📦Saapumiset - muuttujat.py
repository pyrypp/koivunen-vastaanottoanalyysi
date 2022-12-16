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


st.header("Muuttujien vaikutus eri vaiheisiin")

grafiikka = Image.open("./saapumiset grafiikka v2.png")


textcol1, textcol2 = st.columns([1,1])

with textcol1:
    st.write("Tarkastellaan, miten saapuvan erän rivimäärä ja paino vaikuttavat saapumisen eri vaiheiden pituuteen.")
    st.write("Aluetarkastelua ei ole saatavilla.")


with textcol2:
    st.image(grafiikka)

# st.write("")
# st.write("")
# st.markdown("#")

st.write("---")

### haetaan data
saapumiset_df = pd.read_excel("./saapumiset_df.xlsx")
saapumiset_df["alue"] = saapumiset_df["alue"].astype(str)

rivit_koktime = saapumiset_df.groupby("RIVIMÄÄRÄ")["koktime"].mean().reset_index()
rivit_waittime = saapumiset_df.groupby("RIVIMÄÄRÄ")["waittime"].mean().reset_index()
rivit_hyltime = saapumiset_df.groupby("RIVIMÄÄRÄ")["hyltime"].mean().reset_index()

paino_koktime = saapumiset_df.groupby("paino_bin")["koktime"].mean().reset_index()
paino_waittime = saapumiset_df.groupby("paino_bin")["waittime"].mean().reset_index()
paino_hyltime = saapumiset_df.groupby("paino_bin")["hyltime"].mean().reset_index()

###
labelsdict = {"koktime":"Kokonaisaika (päivää)", "waittime":"Odotusaika (päivää)", "hyltime":"Hyllytysaika (päivää)",
    "RIVIMÄÄRÄ":"Rivimäärä", "paino_bin":"Paino (kg)"
}


### kaaviot
def luo_kaavio(df, title):
    x = df.columns[0]
    y = df.columns[1]

    df = df[df[y]<50]

    fig1 = px.scatter(df, x=x, y=y, trendline="lowess",
    height=520, title="<b>" + title, labels=labelsdict)

    # fig1.update_traces(marker=dict(color="green"))
    fig1.update_traces(line_color="red")
    fig1.update_xaxes(matches=None)
    fig1.update_yaxes(matches=None)
    fig1.update_layout(font_size=15)
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

coll, col1, colc, col2, colr = st.columns([0.1, 1, 0.2, 1, 0.1])

with col1:
    luo_kaavio(rivit_koktime, "Rivimäärä x kokonaisaika")
    luo_kaavio(rivit_waittime, "Rivimäärä x odotusaika")
    luo_kaavio(rivit_hyltime, "Rivimäärä x hyllytysaika")

with col2:
    luo_kaavio(paino_koktime, "Paino x kokonaisaika")
    luo_kaavio(paino_waittime, "Paino x odotusaika")
    luo_kaavio(paino_hyltime, "Paino x hyllytysaika")


st.subheader("Huomataan, että")
st.write("- Suuremman rivimäärän erien hyllytys aloitetaan nopeammin.")
st.write("- Suuremmat rivimäärät hyllytetään nopeammin.")
st.write("- Painavampien erien hyllyttämisessä kestää kauemmin.")
