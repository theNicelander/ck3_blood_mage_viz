import streamlit as st

THUMBNAIL_LINK = (
    "https://raw.githubusercontent.com/theNicelander/ck3_blood_mage/main/thumbnail.jpg"
)


def render_line():
    st.sidebar.write("---------------------------")


def sidebar_footer():
    render_line()
    st.sidebar.write(
        "STEAM PAGE: https://steamcommunity.com/sharedfiles/filedetails/?id=2737082376"
    )

    st.sidebar.write("Consider buying be a coffee to support my work.")
    st.sidebar.write("https://www.buymeacoffee.com/TheNicelander")
