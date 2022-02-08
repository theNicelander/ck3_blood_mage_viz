import streamlit as st

from blood_mage.levelup_blood_mage_rank import render_level_up
from blood_mage.shared import sidebar_footer
from blood_mage.trait_drain import render_trait_drain
from blood_mage.front_page import render_front_page

st.sidebar.title("CK3 Blood mage mod")
what_to_render = st.sidebar.selectbox(
    "Select visualisation", ["--", "Trait drain", "Blood Mage Level Up"]
)

if what_to_render == "--":
    render_front_page()
if what_to_render == "Trait drain":
    render_trait_drain()
if what_to_render == "Blood Mage Level Up":
    render_level_up()

sidebar_footer()
