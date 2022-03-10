import streamlit as st
import pandas as pd

from src.story import STORY
import src.logic as lg
from src.simulation import Simulation
from src.simulation_unknown_best import Simulation_unknown_best
# from src.tuning import tune_simulation, create_histogram


st.set_page_config(
    page_title="Guacamole Contest",
    page_icon="img/avocado-emoji.png",
    initial_sidebar_state="collapsed")

lg.initialize_session_state()
num_townspeople, st_dev, fullness_factor = lg.sidebar()


st.title("The Allegory of the Avocados")
st.write("""
Here is the link to our 
[Google Doc](https://docs.google.com/document/d/1CA9NXp8I9b6ds16khcJLrY1ZL7ZBABK6KRu9SvBL5JI/edit?usp=sharing) 
where we're developing and commenting on the story.""")

st.subheader("Welcome to Sunnyvale")
lg.write_story("Introduction")

st.subheader("Let’s Play Guac God")
lg.write_story("Guac God")
guac_df = lg.choose_scenario()

# create_histogram(guac_df)
st.subheader("Let's Taste and Vote!")
lg.write_story("Voting")
sim1 = Simulation(guac_df, num_townspeople, st_dev, fullness_factor=fullness_factor)
sim1.simulate()
lg.animate_results(sim1, key="simulation_1")
print(st.session_state)

# chosen_method = lg.tally_votes(sim1, key="sim1")
# lg.declare_a_winner(sim1, chosen_method)


st.markdown("---")
st.subheader("2. Not enough guac to go around")
# num_townspeople, st_dev = lg.simulation_parameters()
guac_limit = st.slider("How many guacs do we limit people to?",
    value=3, min_value=1, max_value=20)



# sim2 = Simulation(guac_df, num_townspeople, st_dev, assigned_guacs=guac_limit)
# sim2.simulate()
# lg.animate_results(sim2, key="simulation_2")
# # st.text("Let's see what the townspeople thought!")
# # chosen_method = lg.tally_votes(sim2, key="sim2")
# # lg.declare_a_winner(sim2, chosen_method)



# # st.subheader("A Fair Voting Process")
# # for paragraph in STORY["Voting"]:
# #     st.write(paragraph)


