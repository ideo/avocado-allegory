import streamlit as st
import pandas as pd

from src.story import STORY
import src.logic as lg
from src.simulation import Simulation
from src.simulation_unknown_best import Simulation_unknown_best
from src.tuning import tune_simulation


st.set_page_config(
    page_title="Guacamole Contest",
    page_icon="img/avocado-emoji.png")


# SIDEBAR
# No sidebar to begin. We fix the parameters first, then provide a sandbox later.


# MAIN PAGE
st.title("The Allegory of the Avocados")
# st.write("""
# Here is the link to our 
# [Google Doc](https://docs.google.com/document/d/1CA9NXp8I9b6ds16khcJLrY1ZL7ZBABK6KRu9SvBL5JI/edit?usp=sharing) 
# where we're developing and commenting on the story.""")
st.write("(We're tabling the story for now while we work on the math.)")

# st.subheader("Welcome to [Town Name]")
# for paragraph in STORY["introduction"]:
#     st.write(paragraph)


# st.subheader("Let’s Play Guac God")
# for paragraph in STORY["Guac God"]:
#     st.write(paragraph)

st.text("Objectively, how do the guacs measure up, relative to each other?")
guac_df = lg.objective_ratings()

tune_simulation(guac_df)


st.subheader("1. Everybody Tries all the Guacs")
num_townspeople, st_dev = lg.simulation_parameters()
sim1 = Simulation(guac_df, num_townspeople, st_dev)
# start = st.button("Simulate")
# if start:
sim1.simulate()

# if sim.results_df is not None:
st.text("Let's see what the townspeople thought!")
chosen_method = lg.tally_votes(sim1, key="sim1")
lg.declare_a_winner(sim1, chosen_method)


st.markdown("---")
st.subheader("2. Not enough guac to go around")
# num_townspeople, st_dev = lg.simulation_parameters()
guac_limit = st.slider("How many guacs do we limit people to?",
    value=3, min_value=1, max_value=20)
sim2 = Simulation(guac_df, num_townspeople, st_dev, num_guac_per_person=guac_limit)
sim2.simulate()
st.text("Let's see what the townspeople thought!")
chosen_method = lg.tally_votes(sim2, key="sim2")
lg.declare_a_winner(sim2, chosen_method)



# st.subheader("A Fair Voting Process")
# for paragraph in STORY["Voting"]:
#     st.write(paragraph)


st.markdown("---")
st.subheader("3. Different Types of Voters")
# for paragraph in STORY["Voter Types"]:
#     st.write(paragraph)

perc_pepe, perc_fra, _ = lg.types_of_voters()
print(perc_pepe, perc_fra)
sim3 = Simulation(guac_df, num_townspeople, st_dev, num_guac_per_person=guac_limit, perc_pepe=perc_pepe, perc_fra=perc_fra)
sim3.simulate()
chosen_method = lg.tally_votes(sim3, key="sim3")
lg.declare_a_winner(sim3, chosen_method)



## FRA WIP BELOW
num_guacs = 20

# Allow abstinence?
st.subheader("What if We Don't Know Whose Guac is Best?")
for paragraph in STORY["Unknown Best"]:
    st.write(paragraph)


st.subheader("1. All Guacs are Relatively Good")
col1, _, col2 = st.columns([4, 4, 4])

with col1:
    num_townspeople = lg.num_people_slider("How many townspeople showed up?")
    sim_day1 = Simulation_unknown_best(num_townspeople, num_guacs, num_guacs)
    sim_day1.simulate()
    lg.plot_votes(sim_day1, 1)

with col2:
    num_guac_per_person = lg.num_guac_per_person_slider("How many guacs can everyone try?")
    sim_day2 = Simulation_unknown_best(num_townspeople, num_guacs, num_guac_per_person)
    sim_day2.simulate(sim_day1.results_df)
    lg.plot_votes(sim_day2, 2)


for paragraph in STORY["Conclusion 1"]:
    st.write(paragraph)


st.subheader("2. Some Guacs Have Better Ingredients")
col1, _, col2 = st.columns([4, 4, 4])

with col1:
    num_townspeople = lg.num_people_slider("How many townspeople showed up? ")
    has_different_ingredients = True
    sim_day1 = Simulation_unknown_best(num_townspeople, num_guacs, num_guacs, has_different_ingredients)
    sim_day1.simulate()
    lg.plot_votes(sim_day1, 1)

with col2:
    num_guac_per_person = lg.num_guac_per_person_slider("How many guacs can everyone try? ")
    sim_day2 = Simulation_unknown_best(num_townspeople, num_guacs, num_guac_per_person)
    sim_day2.simulate(sim_day1.results_df)
    lg.plot_votes(sim_day2, 2)

for paragraph in STORY["Conclusion 2"]:
    st.write(paragraph)

# 

# sim_base = Simulation_unknown_best(num_townspeople, num_guacs, num_guacs, has_different_ingredients)
# sim_base.simulate()
# lg.plot_votes(sim_base)

# # num_guac_per_person = lg.num_guac_per_person_slider()
# sim_has_ingredients = Simulation_unknown_best(num_townspeople, num_guacs, num_guac_per_person)
# sim_has_ingredients.simulate(sim_base.results_df)
# lg.plot_votes(sim_has_ingredients)

# for paragraph in STORY["Conclusion 2"]:
#     st.write(paragraph)


