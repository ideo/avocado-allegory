# avocado-allegory


### Streamlit & Pandas Version Conflicts
Streamlit will let you develop locally with the latest python (3.9.x) but can only host up to python 3.7.12. The latest pandas has moved on from python 3.7. All this is to say, please don't change the python and pandas versions specified in `pyproject.toml`.


### Testing
Run the unit tests from the command line with 
```bash
poetry run python -m unittest test.test_simulation
poetry run python -m unittest test.test_condorcet_method
```