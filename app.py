import streamlit as st
import pandas as pd

from src.story import STORY
import src.logic as lg
from src.simulation import Simulation
from src.simulation_unknown_best import Simulation_unknown_best
# from src.tuning import tune_simulation, wrap_my_head_around_it


# wrap_my_head_around_it()

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
lg.write_instructions("Guac God")
guac_df = lg.choose_scenario()
st.image("img/holy_guacamole.jpeg", width=400, caption="This is you, the Guacamole Goddess.")


st.markdown("---")
st.subheader("Let's Taste and Vote!")
section_title = "simulation_1"
lg.write_story(section_title)
lg.write_instructions(section_title)
sim1 = Simulation(guac_df, num_townspeople, st_dev, fullness_factor=fullness_factor)
sim1.simulate()
lg.animate_results(sim1, key=section_title)
if st.session_state[f"{section_title}_keep_chart_visible"]:
    lg.success_message(section_title, sim1.success)


st.markdown("---")
lg.write_story("transition_1_to_2")
st.subheader("Not Enough Guac to Go Around")
section_title = "simulation_2"
lg.write_story(section_title)

col1, col2 = st.columns(2)
lg.write_instructions(section_title, col1)
guac_limit2 = col2.slider(
    "How many guacs will tasters try? Start by just removing a couple and then push it from there.",
    value=18, 
    min_value=1, 
    max_value=20)

sim2 = Simulation(guac_df, num_townspeople, st_dev, assigned_guacs=guac_limit2)
sim2.simulate()
# lg.animate_results(sim2, key=section_title)

# lg.get_winner_image(sim2, key=section_title)
# if st.session_state[f"{section_title}_keep_chart_visible"]:
#     lg.success_message(section_title, sim2.success, guac_limit)
lg.animate_results(sim2, key=section_title)
if st.session_state[f"{section_title}_keep_chart_visible"]:
    lg.success_message(section_title, sim2.success, guac_limit2)


st.markdown("---")
lg.write_story("transition_2_to_3")
st.subheader("Different People, Different Tastes")
section_title = "simulation_3"
lg.write_story(section_title)
st.text("")
lg.write_instructions(section_title+"_a")
pepe, fra, carlos = lg.types_of_voters()
col1, col2 = st.columns(2)
lg.write_instructions(section_title+"_b", col1)
guac_limit3 = col2.slider(
    "How many guacamoles does each voter get to try?",
    value=15, 
    min_value=1, 
    max_value=20)

sim3 = Simulation(guac_df, num_townspeople, st_dev, 
    assigned_guacs=guac_limit3,
    perc_fra=fra,
    perc_pepe=pepe,
    perc_carlos=carlos)
sim3.simulate()
lg.animate_results(sim3, key=section_title)
# lg.success_message(sim3)


st.markdown("---")