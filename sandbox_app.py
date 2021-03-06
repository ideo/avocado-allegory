import streamlit as st

from src import logic as lg
from src import Simulation


st.set_page_config(
    page_title="Development Sandbox",
    page_icon="img/avocado-emoji.png",
    initial_sidebar_state="collapsed")


lg.initialize_session_state()

st.subheader("Sandbox")
section_title = "sandbox"
lg.write_story(section_title)

sandbox_df, sandbox_scenario = lg.choose_scenario(key=section_title)

pepe, fra, carlos = .10, .10, .15
pepe_sb, fra_sb, carlos_sb = lg.types_of_voters(section_title, pepe, fra, carlos)
col1, col2 = st.columns(2)

st_dev = col1.number_input("What is the st. dev. of their randomly generated scores?",
        value=2.0,
        min_value=0.1,
        max_value=5.0,
        step=0.1)
fullness_factor = col2.number_input("What is the mean offset of the fullness factor?",
        value=1.0,
        min_value=0.1,
        max_value=3.0,
        step=0.1)

num_townspeople_sb = col1.slider(
    "How many townspeople vote in the contest?",
    value=250,
    min_value=10,
    max_value=500,
    step=10,
    key=section_title)
guac_limit_sb = col2.slider(
    "How many guacamoles does each voter get to try?",
    value=sandbox_df.shape[0], 
    min_value=1, 
    max_value=sandbox_df.shape[0],
    key=section_title)


c1, c2 = st.columns([5,3])
methods = {
    "Summing the Scores":           "sum", 
    "Tallying Implicit Rankings":   "condorcet",
    "Ranked Choice Voting":         "rcv",
    "Pick Your One Favorite":       "fptp",
}
method_chosen = c1.selectbox("How should we tally the votes?",
    options=methods.keys())
method = methods[method_chosen]

N = min(st.session_state["N"], guac_limit_sb)
if method == "rcv":
    N = c2.number_input(f"Each voter ranks their top {N} guacamoles.",
        value=N,
        min_value=1,
        # max_value=sandbox_df.shape[0],
        max_value=guac_limit_sb,
        key="N")

sandbox_sim = Simulation(sandbox_df, num_townspeople_sb, st_dev, 
    assigned_guacs=guac_limit_sb,
    fullness_factor=fullness_factor,
    perc_fra=fra_sb,
    perc_pepe=pepe_sb,
    perc_carlos=carlos_sb,
    method=method,
    rank_limit=N)
sandbox_sim.simulate()

lg.success_message(section_title, sandbox_sim.success)
lg.animate_results(sandbox_sim, key=section_title)
lg.print_params(sandbox_sim)