import streamlit as st

from blood_mage_levelup import render_level_up
from trait_drain import render_trait_drain

st.sidebar.title("CK3 Blood mage mod")
what_to_render = st.sidebar.selectbox(
    "Select visualisation", ["Trait drain", "Blood Mage Level Up"]
)


if what_to_render == "Trait drain":
    render_trait_drain()
if what_to_render == "Blood Mage Level Up":
    render_level_up()

#
st.sidebar.write("---------------------------")
st.sidebar.image(
    "https://raw.githubusercontent.com/theNicelander/ck3_blood_mage/main/thumbnail.jpg"
)
st.sidebar.write("https://steamcommunity.com/sharedfiles/filedetails/?id=2737082376")
