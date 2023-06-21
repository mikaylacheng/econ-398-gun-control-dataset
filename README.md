## Dataset

To create the full dataset from the data sources, run `python3 make_dataset.py`. This will create a file called `econ_gun_dataset.csv` in the `data` directory. The full dataset draws from many data sources which have been pre-assembled in the `data/` folder by running the associated scraping scripts.

## Data Sources
control data (educational attainment, race, and unemployment rate) - see attached .do files in the data folder for how to create them.

unemployment and race breakdown data: https://byu-my.sharepoint.com/personal/gwenlyn7_byu_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fgwenlyn7%5Fbyu%5Fedu%2FDocuments%2FSpring%202023%2Fresearch%20paper%2Dproject%2F1960%2D2021%20unemploy%20and%20race%2Fusa%5F00007%2Egz&parent=%2Fpersonal%2Fgwenlyn7%5Fbyu%5Fedu%2FDocuments%2FSpring%202023%2Fresearch%20paper%2Dproject%2F1960%2D2021%20unemploy%20and%20race&ga=1

state_n_mass_shootings.json from https://www.statista.com/statistics/811541/mass-shootings-in-the-us-by-state/ total from 1982 to 2023

state_gun_deaths from https://www.cdc.gov/nchs/pressroom/sosmap/firearm_mortality/firearm.htm

state, race, sex from https://www.census.gov/data/datasets/time-series/demo/popest/2020s-state-detail.html

income data per state from https://fred.stlouisfed.org

population data per state from https://fred.stlouisfed.org

state party from https://www.270towin.com/states/

state region from https://www2.census.gov/geo/pdfs/maps-data/maps/reference/us_regdiv.pdf

state pop totals from https://www2.census.gov/programs-surveys/popest/datasets/2020-2022/state/totals/

state political party from https://www.kff.org/other/state-indicator/state-political-parties/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D

state gun registration (2021) from https://www.statista.com/statistics/215655/number-of-registered-weapons-in-the-us-by-state/

mass shooting events https://www.gunviolencearchive.org/

## Making the Dataset

Create a python virtual environment:

```
python3 -m venv env
source env/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

Run make_dataset.py

```
python3 make_dataset.py
```

Check the data/ folder for the econ_gun_dataset.csv file.
