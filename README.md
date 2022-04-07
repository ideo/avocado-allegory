# avocado-allegory

This simulation was inspired by a story shared by IDEOer Jenna Fizel and the guacamole contest that their partner had helped organize. The contest had a simple problem: too many people wanted to participate in the contest by tasting and voting, but there just wouldn't have been enough guacamole to go around. The solution was quite clever. With some non-traditional methods of vote counting, it's not necessary for each voter to try each guacamole in the contest. That method allows more people to particiapte, both as guac-chegs and guac-critis.

Many exisiting voting simulation are civics-orientied, e.g. the presidential election. This simulation differs in that we delibrately limit voters to a subset of candidates. Obvisouly, that would never fly in a governmental election; we could never say, "Hey, 13 candidates are in this primary, but we're only going to let you voice your opinion on 3 of them." But a guacamole contest is a useful metaphor for competitions in the arts. For example, maybe we want to consider 50 movies for Best Picture at the Oscars next year. It would liekly be too burdensome to ask the Academy's voters to watch all 50 movies and fairly critique each one. But these simulations show that randomly assigning 5 different movies to each voter will make it feasible to have that many candidates for Best Picture and still have a fair outcome. It also opens the door to include more voters, as doing so only makes the election more robust and watching only 5 movies is not too much to ask of someone.

While the story that inspired this work relied on one particular voting method, this simulation has been designed to test whatever methods we are curious about. To join in on the fun, see below!


### Running the App
This project relies on Poetry and Streamlit. To start the app, run:
```bash
poetry run streamlit run app.py
```

`app.py` contains our current work in progress story and simulation. The intent is to publish this as a blog post once it is further along. The current draft was very much a build-to-think product. It explores useful story metaphors and interactive widgets but still lacks a clear articulation of what problem needs to be solved.

More useful at this stage will be:
```bash
poetry run streamlit run sandbox_app.py
```

The `sandbox_app.py` has been set up to explore different voting methods, consistency of outcomes, and help craft the specifc simulation set ups we'll want to inculde in the story. This is where we are currenlty spending our time.


### The Code
- `simuation.py`
- `townspeople.py`
- each voting method class


### Version Control
Streamlit will let you develop locally with the latest python (3.9.x) but can only host up to python 3.7.12. The latest pandas has moved on from python 3.7. All this is to say, please don't change the python and pandas versions specified in `pyproject.toml`.


### Testing
Run the unit tests from the command line with 
```bash
poetry run python -m unittest test.test_simulation
poetry run python -m unittest test.test_condorcet_method
```

If you add a new voting method class, please also add tests to `tests/` to verify it. You can use the existing tests as templates.