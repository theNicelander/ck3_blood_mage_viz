import pandas as pd
import streamlit as st
from plotly import express as px

SUCCESS_CHANCE_BASE = 0
FAIL_CHANCE_BASE = 10
LEVEL_MULTIPLIER = 2

LEARNING = "Learning"
BM_LEVELS = {
    "Blood Mage Initiate": 0,
    "Blood Mage Disciple": 25,
    "Adept Blood Mage": 50,
    "Master Blood Mage": 75,
    "Grandmaster Blood Mage": 100,
    "Arch Blood Mage": 150,
    "The Exalted": 200,
    "The Supreme": 250,
    "The Divine": 300,
}
BM_MULTIPLIER = {
    "Blood Mage Initiate": 1,
    "Blood Mage Disciple": 3,
    "Adept Blood Mage": 5,
    "Master Blood Mage": 7,
    "Grandmaster Blood Mage": 9,
    "Arch Blood Mage": 11,
    "The Exalted": 13,
    "The Supreme": 16,
    "The Divine":21,
}



@st.cache(allow_output_mutation=True)
def create_base_frame():
    learning = [{LEARNING: int(diff)} for diff in range(0, 100)]

    df = pd.DataFrame(learning)
    df["SUCCESS_CHANCE_BASE"] = SUCCESS_CHANCE_BASE
    df["FAIL_CHANCE_BASE"] = FAIL_CHANCE_BASE
    for lvl in BM_MULTIPLIER.keys():
        df[f"{lvl.upper()}_MULTIPLIER"] = BM_MULTIPLIER[lvl]
    return df


@st.cache(allow_output_mutation=True)
def get_key_cols():
    chance_cols = [lvl for lvl in BM_LEVELS]
    plotting_cols = chance_cols + [LEARNING]
    return chance_cols, plotting_cols


def render_level_up():
    st.write("Chance to level up blood mage trait")
    df = create_base_frame().copy()
    chance_cols, plotting_cols = get_key_cols()

    for lvl in BM_LEVELS.keys():
        # calc chance
        success_chance = df["SUCCESS_CHANCE_BASE"] + df[LEARNING] * LEVEL_MULTIPLIER
        fail_chance = df["FAIL_CHANCE_BASE"] + BM_LEVELS[lvl]

        df[lvl] = success_chance / (success_chance + fail_chance)

        # min/max
        df[lvl] = df[lvl].clip(lower=0, upper=1)
    fig = px.line(df[plotting_cols], x=LEARNING, y=chance_cols)
    fig.update_layout(
        title="Chance of levelling up Blood Mage Trait",
        yaxis_title="Chance of success",
        legend_title="Rank",
        yaxis_range=[0, 1],
    )

    st.plotly_chart(fig)
