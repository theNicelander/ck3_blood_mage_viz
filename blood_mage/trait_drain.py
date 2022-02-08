import pandas as pd
import streamlit as st
from plotly import express as px

from blood_mage.shared import render_line


LEARNING_CHALLENGE = "Difference in Learning"

SUCCESS_CHANCE_BASE = 0
FAIL_CHANCE_BASE = 10
LEVEL_MULTIPLIER = 2
TRAIT_MALICE = 10

BM_BASE = {
    "Novice": 0,
    "Regular": 10,
    "Master": 30,
    "Arch": 90,
    "Supreme": 270,
}
BM_MULTIPLIER = {
    "Novice": 1,
    "Regular": 2,
    "Master": 4,
    "Arch": 7,
    "Supreme": 12,
}

BM_MALUS_LOOKUP = {
    "None": 0,
    "Quick": 1,
    "Intelligent": 2,
    "Genius": 3,
    "Hale": 1,
    "Robust": 2,
    "Heruclean/Amazonian": 3,
    "Comely": 1,
    "Pretty": 2,
    "Beautiful": 3,
}


@st.cache(allow_output_mutation=True)
def create_base_frame():
    learning_diff = [{LEARNING_CHALLENGE: int(diff)} for diff in range(-10, 50)]

    df = pd.DataFrame(learning_diff)
    df["SUCCESS_CHANCE_BASE"] = SUCCESS_CHANCE_BASE
    df["FAIL_CHANCE_BASE"] = FAIL_CHANCE_BASE

    # add base cols
    for lvl in BM_BASE.keys():
        df[f"{lvl.upper()}_BASE"] = BM_BASE[lvl]

    # add multiplier cols
    for lvl in BM_MULTIPLIER.keys():
        df[f"{lvl.upper()}_MULTIPLIER"] = BM_MULTIPLIER[lvl]
    return df


def render_optional_explanation():
    with st.expander("See explanation behind calculation"):
        st.write("Success formula:")
        ex_multip = BM_MULTIPLIER["Master"]
        ex_base = BM_BASE["Master"]
        st.markdown(
            """
        ```
        Positive  = Base success + (learning diff * Mage multiplier ) + Mage modifier
        Negative  = Base fail + total malus from traits
        Success % = Positive / ( Positive + Negative )
        ```
        """
        )
        st.write("Example:")
        st.markdown(
            f"""
        ```
        Player as master Blood Mage (rank 3) has 2 positive traits and 20 learning
        Target has 11 learning

        Positive  = {SUCCESS_CHANCE_BASE} + (20 - 11) * {ex_multip} + {ex_base} = 66
        Negative  = {FAIL_CHANCE_BASE} + 2 * {TRAIT_MALICE} = 20
        Success % = 66 / ( 66 + 20 ) = 76.7%
        ```
        """
        )
        st.write("-----------------------------------------")

        st.text(f"Base modifier of success: {SUCCESS_CHANCE_BASE}")
        st.text(f"Modifier multiplier for learning: {LEVEL_MULTIPLIER}")

        st.text(f"Base modifier of failure: {FAIL_CHANCE_BASE}")

        df_multi = pd.DataFrame([BM_BASE, BM_MULTIPLIER]).T.rename(
            {0: "Mage Modifier", 1: "Mage Multiplier"}, axis=1
        )
        st.dataframe(df_multi)


@st.cache(allow_output_mutation=True)
def get_key_cols():
    chance_cols = [lvl for lvl in BM_BASE]
    plotting_cols = chance_cols + [LEARNING_CHALLENGE]
    return chance_cols, plotting_cols


def plot_chance(selection_malus):
    # Get constants
    df = create_base_frame().copy()
    chance_cols, plotting_cols = get_key_cols()

    for lvl in BM_BASE.keys():
        # calc chance
        success_chance = (
            df["SUCCESS_CHANCE_BASE"]
            + df[LEARNING_CHALLENGE] * df[f"{lvl.upper()}_MULTIPLIER"]
            + df[f"{lvl.upper()}_BASE"]
        )
        fail_chance = df["FAIL_CHANCE_BASE"] + selection_malus

        df[lvl] = success_chance / (success_chance + fail_chance)
        # min/max
        df[lvl] = df[lvl].clip(lower=0, upper=1)

    fig = px.line(df[plotting_cols], x=LEARNING_CHALLENGE, y=chance_cols)
    fig.update_layout(
        title="Chance of successfully draining a trait",
        yaxis_title="Chance of success",
        legend_title="Blood Mage Level",
        yaxis_range=[0, 1],
    )

    st.plotly_chart(fig)

    with st.expander("See raw data"):
        st.dataframe(df)


def get_selection_malus():
    st.text(f"Which traits do you have? (Each adds -{TRAIT_MALICE} to success)")

    col1, col2, col3 = st.columns(3)
    with col1:
        intellect_level = st.selectbox(
            label="Intellect", options=["None", "Quick", "Intelligent", "Genius"]
        )

    with col2:
        physical_level = st.selectbox(
            label="Strength", options=["None", "Hale", "Robust", "Heruclean/Amazonian"]
        )

    with col3:
        beauty_level = st.selectbox(
            label="Beauty", options=["None", "Comely", "Pretty", "Beautiful"]
        )
    others = st.multiselect("Other traits", options=["Giant", "Fecund", "Pure Blood"])

    number_of_traits = (
        len(others)
        + BM_MALUS_LOOKUP[intellect_level]
        + BM_MALUS_LOOKUP[physical_level]
        + BM_MALUS_LOOKUP[beauty_level]
    )
    total_malus = number_of_traits * TRAIT_MALICE

    st.write(f"Total Malus: {total_malus}")

    return total_malus


def trait_drain_sidebar_explanations():
    render_line()
    st.sidebar.write("Trait drain is a way for a blood mage to drain a positive trait from their target")
    st.sidebar.write("- The more `positive traits` you already have, the less successful you will be")
    st.sidebar.write("- The higher your `learning` and `blood mage trait` are, the more successful you'll be")


def render_trait_drain():
    trait_drain_sidebar_explanations()
    selection_malus = get_selection_malus()

    plot_chance(selection_malus)
    render_optional_explanation()
