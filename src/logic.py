import streamlit as st
import pandas as pd
import time
import inflect

from .story import STORY, INSTRUCTIONS, SUCCESS_MESSAGES
from .config import COLORS, ENTRANTS, DEMO_CONTEST
from .simulation import Simulation


import warnings
warnings.simplefilter(action='ignore', category=UserWarning)


p = inflect.engine()


def initialize_session_state():
    initial_values = {
        "simulation_1_keep_chart_visible":  False,
        "simulation_2_keep_chart_visible":  False,
        "simulation_3_keep_chart_visible":  False,
        "condorcet_keep_chart_visible":     False,
        "sandbox_keep_chart_visible":       False,
        "entrant_num":                      0,
        "N":                                5,
    }

    for key, value in initial_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_visuals():
    for key in st.session_state:
        if "_keep_chart_visible" in key:
            st.session_state[key] = False


def write_story(section_title):
    for paragraph in STORY[section_title]:
        st.write(paragraph)


def write_instructions(section_title, st_col=None):
    for paragraph in INSTRUCTIONS[section_title]:
        if st_col is not None:
            st_col.caption(paragraph)
        else:
            st.caption(paragraph)


def success_message(section_key, success, guac_limit=None, name=None, percent=None):
    for paragraph in SUCCESS_MESSAGES[section_key][success]:
        if guac_limit is not None:
            st.caption(paragraph.replace("GUAC_LIMIT", str(guac_limit)).replace("MISSING_GUACS", str(20-guac_limit)))
        if name is not None:
            st.caption(paragraph.replace("NAME", name).replace("PERCENT", percent))
        else:
            st.caption(paragraph)


def sidebar():
    """
    Let's put all the sidebar controls here!
    """
    st.sidebar.subheader("Simulation Parameters")
    keep_out = """
        HEY! What are you doing it here? This area is off limits! Only Fra and 
        Joe are allowed in here! Get outta here ya meddling kids!
    """
    st.sidebar.write(keep_out)
    num_townspeople = st.sidebar.slider("How many townspeople are there?", 
        value=200, 
        min_value=10, 
        max_value=500,
        step=10)
    st_dev = st.sidebar.number_input("What is the st. dev. of their randomly generated scores?",
        value=2.0,
        min_value=0.1,
        max_value=5.0,
        step=0.1
        )
    fullness_factor = st.sidebar.number_input("What is the mean offset of the fullness factor?",
        value=1.0,
        min_value=0.1,
        max_value=3.0,
        step=0.1
        )
    return num_townspeople, st_dev, fullness_factor


def choose_scenario(key="intro"):
    """
    The user selects a scenario, which determines the 'objective ratings' to be
    used in the simulation.
    """

    #define the structure of the entry as 2 columns
    col1, col2 = st.columns([2,5])

    #one column has a widget with 2 options
    options = list(ENTRANTS[0].keys())
    options.remove("ID")
    options.remove("Entrant")

    scenario = col1.radio(
        "Choose a scenario", 
        options=options,
        index=0,
        on_change=reset_visuals,
        key=key)
    df = get_scenario_dataframe(scenario)

    if key == "sandbox":
        num_guacs = col1.slider("How many contestants?",
            min_value=5,
            max_value=20,
            value=20,
            key="num_guacs")

        if num_guacs < 20:
            df = df.sample(n=num_guacs, random_state=42)
            df.sort_index(inplace=True)
            df = format_scenario_colors(df)
            df.index = list(range(df.shape[0]))

    winner = df["Objective Ratings"].idxmax()
    #draw the chart
    spec = {
        "height":   275,
        "mark": {"type": "bar"},
        "encoding": {
            "x":    {
                "field": "Entrant", "type": "nominal", "sort": "ID", 
                "axis": {"labelAngle": 45}
                },
            "y":    {"field": "Objective Ratings", "type": "quantitative"},
            "color":    {"field": "Color", "type": "nominal", "scale": None}
        },
        "title":    {
            "text": scenario, 
            "subtitle": f"The Best Guac is Guac No. {winner}"},   
    }

    col2.vega_lite_chart(df, spec)
    return df, scenario


def get_scenario_dataframe(scenario):
    df = pd.DataFrame(data=ENTRANTS)
    df["Objective Ratings"] = df[scenario].copy()
    # winning_score = df["Objective Ratings"].max()
    # df["Color"] = df["Objective Ratings"].apply(
    #     lambda x: COLORS["green"] if x==winning_score else COLORS["blue"])
    df = format_scenario_colors(df)
    return df


def format_scenario_colors(df):
    winning_score = df["Objective Ratings"].max()
    df["Color"] = df["Objective Ratings"].apply(
        lambda x: COLORS["green"] if x==winning_score else COLORS["blue"])
    return df


def animate_results(sim, key):
    """The one function to be called in app.py"""
    if sim.method == "sum":
        animate_summation_results(sim, key=key)
    elif sim.method == "condorcet":
        animate_condorcet_simulation(sim, key=key)
    elif sim.method == "rcv":
        show_rcv_rankings(sim)
    elif sim.method == "fptp":
        show_fptp_rankings(sim.rankings, sim.num_townspeople)     


def animate_summation_results(sim, key):
    """
    Creates the `Simulate` button, animated chart, and success/fail message
    """
    col1, col2 = st.columns([2,5])
    start_btn = col1.button("Simulate", key=key)

    results_df = sim.results_df.copy()
    results_df.drop(columns=["sum"], inplace=True)
    subtitle = "And the winner is... "
    y_max = int(sim.results_df["sum"].max())

    animation_duration = 1 #second
    time_per_frame = animation_duration / results_df.shape[0] / 20

    bar_chart = None
    if start_btn:
        st.session_state[f"{key}_keep_chart_visible"] = True
        for NN in range(results_df.shape[1]):
            chart_df, spec = format_spec(sim, subtitle, y_max, col_limit=NN)
            if bar_chart is not None:
                bar_chart.vega_lite_chart(chart_df, spec)
            else:
                bar_chart = col2.vega_lite_chart(chart_df, spec)

            # time.sleep(.01/2)
            time.sleep(time_per_frame)

    if st.session_state[f"{key}_keep_chart_visible"]:
        # Ensure the final chart stays visible
        chart_df, spec = format_spec(sim, subtitle, y_max)
        if bar_chart is not None:
            bar_chart.vega_lite_chart(chart_df, spec)
        else:
            bar_chart = col2.vega_lite_chart(chart_df, spec)

        # message_var = None
        # if sim.assigned_guacs < results_df.shape[0]:
        #     message_var = results_df.shape[0] - sim.assigned_guacs
        # success_message(key, sim.success, message_var)


#this is an experiment, to include an image with the winner        
def get_winner_image(sim, key):
    col1, col2 = st.columns([2,5])
    start_btn = col1.button("Simulate", key=key)

    if start_btn:
        col1, col2, col3 = st.columns(3)
        col2.image("img/badge2.png", width=100, caption="badge test.")


def format_spec(sim, subtitle, y_max, col_limit=None):
    """Format the chart to be shown in each frame of the animation"""

    if col_limit:
        chart_df = sim.results_df.iloc[:, :col_limit].copy()
        chart_df["sum"] = chart_df.sum(axis=1)
    else:
        chart_df = sim.results_df.copy()

    color_spec = None
    chart_df["Entrant"] = sim.guac_df["Entrant"]
    if col_limit is None:
        subtitle += f"Guacamole No. {sim.sum_winner}!"
        chart_df = format_bar_colors(chart_df, sim.objective_winner, sim.sum_winner)
        color_spec = {"field": "Color", "type": "nomical", "scale": None}

    spec = {
            "height":   275,
            "mark": {"type": "bar"},
            "encoding": {
                "x":    {
                    "field": "Entrant", "type": "nominal", "sort": "ID",
                    "axis": {"labelAngle": 45}},
                "y":    {
                    "field": "sum", "type": "quantitative", 
                    "scale": {"domain": [0, y_max]},
                    "title": "Vote Tallies"},
                "color":    color_spec,
            },
            "title":    {
                "text": f"Simulation Results",
                "subtitle": subtitle, 
            }  
        }
    return chart_df, spec


def format_bar_colors(chart_df, should_win, actually_won):
    chart_df["Color"] = pd.Series([COLORS["blue"]]*chart_df.shape[0], index=chart_df.index)
    chart_df.at[actually_won, "Color"] = COLORS["red"]
    chart_df.at[should_win, "Color"] = COLORS["green"]
    return chart_df


def animate_results_of_100_runs(sim, scenario, key):
    col1, col2 = st.columns([2,5])
    start_btn = col1.button("Simulate 100 Times", key=key)

    chart_df = get_row_and_format_dataframe(sim, scenario)
    spec = format_N_times_chart_spec(chart_df)
    bar_chart = col2.vega_lite_chart(chart_df, spec)

    list_who_else_won(chart_df, sim)


def get_row_and_format_dataframe(sim, scenario):
    df = pd.read_csv("data/simulate_100_times_sum.csv")
    df.drop(columns=["Unnamed: 0"], inplace=True)
    chart_df = df[
        (df["num_townspeople"] == sim.num_townspeople) & \
        (df["st_dev"] == sim.st_dev) & \
        (df["assigned_guacs"] == sim.assigned_guacs) & \
        (df["perc_fra"] == sim.perc_fra) & \
        (df["perc_pepe"] == sim.perc_pepe) & \
        (df["perc_carlos"] == sim.perc_carlos) & \
        (df["scenario"] == scenario)
    ]
    columns = [
        "num_townspeople",
        "st_dev",
        "assigned_guacs",
        "perc_fra",
        "perc_pepe",
        "perc_carlos",
        "scenario",
    ]
    should_win = {
        "One Clear Winner":     5,
        "A Close Call":         9,
        "A Lot of Contenders":  12,
    }

    chart_df.drop(columns=columns, inplace=True)
    chart_df.fillna(value=0.0, inplace=True)
    _index = chart_df.index[0]
    chart_df = chart_df.T
    chart_df.rename(columns={_index: "No Times Won"}, inplace=True)
    chart_df["No Times Won"] = chart_df["No Times Won"].astype(int)
    chart_df.index = chart_df.index.astype(int)
    chart_df = format_bar_colors(chart_df, should_win[scenario], chart_df["No Times Won"].idxmax())
    chart_df.index.name = "ID"
    chart_df.reset_index(inplace=True)
    chart_df.sort_values(by="ID", inplace=True)
    chart_df["Entrant"] = chart_df["ID"].apply(lambda x: [ent["Entrant"] for ent in ENTRANTS if ent["ID"]==x][0])
    return chart_df


def format_N_times_chart_spec(chart_df):
    spec = {
            "height":   250,
            "mark": {"type": "bar"},
            "encoding": {
                "x":    {
                    "field": "Entrant", "type": "nominal", "sort": "ID",
                    "axis": {"labelAngle": 45}},
                "y":    {
                    "field": "No Times Won", "type": "quantitative", 
                    "scale": {"domain": [0, 100]},
                    "title": "No. Times Won"},
                "color":    {
                    "field": "Color", 
                    "type": "nomical", 
                    "scale": None},
            },
            "title":    {
                "text": f"Simulating the Contest 100 Times",
                "subtitle": "How often was each person's guac voted best?", 
            }  
        }
    return spec


def list_who_else_won(df, sim):
    df = df[df["No Times Won"] > 0].copy()
    df.sort_values(by="No Times Won", ascending=False, inplace=True)
    
    name = df.iloc[0]["Entrant"]
    wins = df.iloc[0]["No Times Won"]
    success = wins > 50
    if success:
        percent = f"{wins}%"
    else:
        percent = f"{100 - wins}%"
    success_message("100_times", success, name=name, percent=percent)

    msg = f"**{p.plural('Result', df.shape[0])} of 100 Contests**"
    for ii in range(0, df.shape[0]):
        entrant = df.iloc[ii]["Entrant"]
        obj_score = sim.guac_df[sim.guac_df["Entrant"] == entrant]["Objective Ratings"].iloc[0]
        wins = df.iloc[ii]["No Times Won"]
        msg += f"\n- {entrant}, with an objective guac score of {obj_score}, won **{wins}** {p.plural('time', wins)}"

    st.markdown(msg)


def types_of_voters(key, pepe=None, fra=None, carlos=None):
    col1, col2, col3 = st.columns(3)
    pepe = col1.slider(
        """
        What percentage of people in town are like Perky Pepe, who loves 
        guacamole so much he'll have a hard time giving anyone a bad score?
        """,
        value=int(pepe*100) if pepe else 10,
        min_value=0,
        max_value=30,
        format="%g%%",
        key=key+"pepe")

    fra = col2.slider(
        """
        What percentage of people in town are like Finicky Francisca, who
        thinks all guacamole is basically mush and won't score any entry too high?
        """,
        value=int(fra*100) if fra else 8,
        min_value=0,
        max_value=30,
        format="%g%%",
        key=key+"fra")

    carlos = col3.slider(
        """
        What percentage of people in town are friends with Cliquey Carlos, and
        will score high guacamole as high as possible no matter what?
        """,
        value=int(carlos*100) if carlos else 12,
        min_value=0,
        max_value=30,
        format="%g%%",
        key=key+"carlos")

    pepe /= 100
    fra /= 100
    carlos /= 100
    return pepe, fra, carlos

    
def animate_condorcet_simulation(sim, key=None):
    col1, col2 = st.columns([2,5])
    start_btn = col1.button("Simulate", key=key)

    if start_btn:
        st.session_state[f"{key}_keep_chart_visible"] = True
        
    if st.session_state[f"{key}_keep_chart_visible"]:
        results_msg = format_condorcet_results(sim)
        col2.markdown(results_msg)


def format_condorcet_results(sim):
    if len(sim.condorcet_winners) > 1:
        msg = "And the winners are..."
        for ii, entrant_id in enumerate(sim.condorcet_winners):
            name = sim.guac_df["Entrant"].iloc[entrant_id]
            msg += f"\n - {ii}: Guacamole No. {entrant_id} by {name}!"
    
    else:
        entrant_id = sim.condorcet_winner
        name = sim.guac_df["Entrant"].iloc[entrant_id]
        msg = f"""
            And the winner is...
            1. Guacamole No. {entrant_id} by {name}!
        """
    return msg


def demo_contest(scenario, st_dev):
    """TKTK"""
    if scenario == "One Clear Winner":
        data = [ENTRANTS[5], ENTRANTS[11], ENTRANTS[12]]
    elif scenario == "A Close Call":
        data = [ENTRANTS[9], ENTRANTS[11], ENTRANTS[12]]
    elif scenario == "A Lot of Contenders":
        data = [ENTRANTS[12], ENTRANTS[0], ENTRANTS[9]]

    df = pd.DataFrame(data=data)
    df["ID"] = pd.Series([0, 1, 2])
    df.rename(columns={scenario: "Objective Ratings"}, inplace=True)
    df = df[["ID", "Entrant", "Objective Ratings"]].copy()

    sim = Simulation(df, 5, st_dev, 
        assigned_guacs=df.shape[0],
        fullness_factor=0,
        seed=42)
    sim.simulate()

    start_btn = next_contestant(sim)
    if start_btn:
        st.button("Next Contestant", on_click=increment_entrant_num)
    

def next_contestant(sim):
    col1, col2, col3 = st.columns(3)
    entrant_num = st.session_state["entrant_num"]
    col1.image(f"img/guac_icon_{entrant_num}.png", width=100)

    name =  sim.guac_df.loc[entrant_num]['Entrant']
    score = sim.guac_df.loc[entrant_num]['Objective Ratings']
    score = int(round(score))
    col2.markdown(f"**{name}'s Guacamole**")
    col2.metric("Your Assesment:", score)

    start_btn = col3.button("Taste and Score")

    if start_btn:
        columns = st.columns(5)
        for ii, col in enumerate(columns):
            person = sim.townspeople[ii]
            score = person.ballot.loc[entrant_num]["Subjective Ratings"]
            score = int(round(score))
            col.metric(f"Taster No. {person.number}", score)

    return start_btn


def increment_entrant_num():
    if st.session_state["entrant_num"] < 2:
        st.session_state["entrant_num"] += 1
    else:
        st.session_state["entrant_num"] = 0


def show_rcv_rankings(sim):
    rankings = sim.rankings
    winner = sim.rankings[0][0]

    msg = "Our winner is...  \n"
    winning_vote = rankings[0][1]
    perc = lambda vc: f"{int(round(vc/sim.num_townspeople*100, 0))}%"
    msg += f"> 1. **{winner}** with {winning_vote} votes! That's {perc(winning_vote)} of the vote.  \n"

    if sim.rcv.eliminations == 0:
        msg += f"""{winner} won an outright majority, with no need for 
            elimination rounds!  \n"""
    else:
        original_tally = int(sim.rcv.original_vote_counts.loc[winner, 1])
        msg += f"""{winner} had an original first-place-vote count of 
            {original_tally} votes (only {perc(original_tally)} of the vote), 
            but won a {sim.rcv.win_type} after {sim.rcv.eliminations} rounds of 
            elimination.  \n"""

    if len(rankings) > 1:
        msg += f"\nAnd our runners up are...  \n"
        for prsn in range(1, min(6, len(rankings))):
            msg += f"> {prsn+1}. {rankings[prsn][0]} with {rankings[prsn][1]} votes. That's {perc(rankings[prsn][1])} of the vote.  \n"
        st.markdown(msg)


def show_fptp_rankings(rankings, num_townspeople):
    msg = "Our winner is...  \n"
    winning_vote = rankings[0][1]
    perc = lambda vc: int(round(vc/num_townspeople*100, 0))

    msg += f"> 1. **{rankings[0][0]}** with {winning_vote} votes! That's {perc(winning_vote)}% of the vote.  \n"
    if len(rankings) > 1:
        msg += f"And our runners up are...  \n"
        for prsn in range(1, min(6, len(rankings))):
            msg += f"> {prsn+1}. {rankings[prsn][0]} with {rankings[prsn][1]} votes. That's {perc(rankings[prsn][1])}% of the vote.  \n"
        st.markdown(msg)


def print_params(sim):
    st.text("Parameter Summary:")
    tab_width = 6
    msg = "{\n"
    for k, v in sim.params.items():
        v = f"'{v}'" if isinstance(v, str) else v
        num_tabs = 3 - len(k)//tab_width
        tabs = "\t"*num_tabs
        msg += f"\t'{k}':{tabs}{v},\n"
    msg += "}"
    st.code(msg)