import streamlit as st

THUMBNAIL_LINK = (
    "https://raw.githubusercontent.com/theNicelander/ck3_blood_mage/main/thumbnail.jpg"
)


def render_front_page():
    st.title("CK3 blood Mage mod")
    st.write("Welcome to the official webpage for the CK3 mod - Blood Mage")

    st.write("Please, select one of the visualisation from the right")

    st.image(THUMBNAIL_LINK)
