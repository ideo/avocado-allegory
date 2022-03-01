import streamlit as st

from src.story import STORY
import src.logic as lg


st.set_page_config(
    page_title="Guacamole Contest",
    page_icon="img/avocado-emoji.png")


# SIDEBAR
# No sidebar to begin. We fix the parameters first, then provide a sandbox later.


# MAIN PAGE
st.title("The Allegory of the Avocados (Working Title)")
st.write("""
Here is the link to our 
[Google Doc](https://docs.google.com/document/d/1CA9NXp8I9b6ds16khcJLrY1ZL7ZBABK6KRu9SvBL5JI/edit?usp=sharing) 
where we're developing and commenting on the story.""")

st.subheader("Welcome to [Town Name]")
for paragraph in STORY["introduction"]:
    st.write(paragraph)

st.subheader("Let’s Play Guac God")
for paragraph in STORY["Guac God"]:
    st.write(paragraph)

st.text("Objectively, how do the guacs measure up relative to each other?")
lg.objective_ratings()

st.subheader("A Fair Voting Process")
for paragraph in STORY["Voting"]:
    st.write(paragraph)

st.subheader("Different Types of Voters")
for paragraph in STORY["Voter Types"]:
    st.write(paragraph)

lg.types_of_voters()
