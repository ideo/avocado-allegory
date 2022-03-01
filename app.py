import streamlit as st

from src.story import STORY
import src.logic as lg


st.set_page_config(
    page_title="Guacamole Contest",
    page_icon="img/avocado-emoji.png")


# SIDEBAR
# No sidebar to begin. We fix the parameters first, then provide a sandbox later.


# MAIN PAGE
st.title("Working Title")

st.subheader("Welcome to [Town Name]")
for paragraph in STORY["introduction"]:
    st.write(paragraph)

st.subheader("Let’s Play Guac God")
for paragraph in STORY["Guac God"]:
    st.write(paragraph)


st.text("Objectively, how do the guacs measure up?")
lg.objective_ratings()

