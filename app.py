import streamlit as st

from src import STORY
from src import logic as lg
from src import Simulation


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
guac_df, scenario = lg.choose_scenario()

lg.write_story("demo_voting")
lg.demo_contest(scenario, st_dev)
st.write("""
    Takeaway: When it's clearly good or bad, there's a lot more agreement. 
    Agreement is trickier when something is just average, not compelling in 
    either way""")
# st.image("img/holy_guacamole.jpeg", width=400, caption="This is you, the Guacamole Goddess.")


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

lg.animate_results(sim2, key=section_title)
if st.session_state[f"{section_title}_keep_chart_visible"]:
    lg.success_message(section_title, sim2.success, guac_limit2)

st.write("")
st.write("")
lg.write_story("simulation_2_a")
lg.animate_results_of_100_runs(sim2, scenario, section_title)


st.markdown("---")
lg.write_story("transition_2_to_3")
st.subheader("Different People, Different Tastes")
section_title = "simulation_3"
lg.write_story(section_title)
st.text("")
lg.write_instructions(section_title+"_a")
pepe, fra, carlos = lg.types_of_voters(section_title)
col1, col2 = st.columns(2)
lg.write_instructions(section_title+"_b", col1)
guac_limit3 = col2.slider(
    "How many guacamoles does each voter get to try?",
    value=15, 
    min_value=1, 
    max_value=20,
    key=section_title)

sim3 = Simulation(guac_df, num_townspeople, st_dev, 
    assigned_guacs=guac_limit3,
    perc_fra=fra,
    perc_pepe=pepe,
    perc_carlos=carlos)
sim3.simulate()
lg.animate_results(sim3, key=section_title)
lg.success_message(section_title, sim3.success)

num_cronies = sum(townie.carlos_crony for townie in sim3.townspeople)
num_effective_cronies = sum(townie.voted_for_our_boy for townie in sim3.townspeople)
st.caption(f"Also, {num_cronies} of Carlos's cronies voted in the contest and {num_effective_cronies} were able to vote for him.")


st.markdown("---")
st.subheader("A New Idea")
section_title = "condorcet"
lg.write_story(section_title + "_1")
st.image("img/napkin_ballot.jpg", width=400)
lg.write_story(section_title + "_2")

st.text("")
st.text("")
lg.write_instructions(section_title)
pepe_4, fra_4, carlos_4 = lg.types_of_voters(section_title, pepe, fra, carlos)
col1, col2 = st.columns(2)
guac_limit4 = col1.slider(
    "How many guacamoles does each voter get to try?",
    value=guac_limit3, 
    min_value=1, 
    max_value=20,
    key=section_title)
num_townspeople4 = col2.slider(
    "How many townspeople vote in the contest?",
    value=num_townspeople,
    min_value=10,
    max_value=500,
    step=10,
    key=section_title)

sim4 = Simulation(guac_df, num_townspeople4, st_dev, 
    assigned_guacs=guac_limit4,
    perc_fra=fra,
    perc_pepe=pepe,
    perc_carlos=carlos,
    method="condorcet")
sim4.simulate()
lg.animate_results(sim4, key=section_title)
lg.success_message(section_title, sim4.success)

num_cronies = sum(townie.carlos_crony for townie in sim4.townspeople)
num_effective_cronies = sum(townie.voted_for_our_boy for townie in sim4.townspeople)
st.caption(f"Also, {num_cronies} of Carlos's cronies voted in the contest and {num_effective_cronies} were able to vote for him.")


st.markdown("---")
st.subheader("Out in the Real World")
lg.write_story("conclusion")


st.markdown("---")
st.subheader("Sandbox")
section_title = "sandbox"
lg.write_story(section_title)
sandbox_df, sandbox_scenario = lg.choose_scenario(key=section_title)
pepe_sb, fra_sb, carlos_sb = lg.types_of_voters(section_title, pepe, fra, carlos)
col1, col2 = st.columns(2)
guac_limit_sb = col1.slider(
    "How many guacamoles does each voter get to try?",
    value=guac_limit3, 
    min_value=1, 
    max_value=20,
    key=section_title)
num_townspeople_sb = col2.slider(
    "How many townspeople vote in the contest?",
    value=num_townspeople,
    min_value=10,
    max_value=500,
    step=10,
    key=section_title)

method_chosen = st.selectbox("How should we tally the votes?",
    options=["Summing the Scores", "Tallying Implicit Rankings"])
method_sb = "sum" if method_chosen == "Summing the Scores" else "condorcet"

sandbox_sim = Simulation(sandbox_df, num_townspeople_sb, st_dev, 
    assigned_guacs=guac_limit_sb,
    perc_fra=fra_sb,
    perc_pepe=pepe_sb,
    perc_carlos=carlos_sb,
    method=method_sb)
sandbox_sim.simulate()
lg.animate_results(sandbox_sim, key=section_title)
lg.success_message(section_title, sandbox_sim.success)