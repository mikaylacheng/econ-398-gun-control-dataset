from constants import *
import pdb
from typing import List
import pandas as pd


def interpolate(ls: List[float], round_to=None) -> List[float]:
    # if numbers are not different for more than one year, interpolate
    # e.g. [12.2, 12.2, 12.2, 15.7] -> [12.2, 13.3, 14.4, 15.7]
    if len(ls) == 1:
        return ls

    i = 1
    start = ls[0]
    start_idx = 0
    while i < len(ls):
        if ls[i] != start:
            slope = (ls[i] - start) / (i - start_idx)
            for j in range(start_idx + 1, i):
                if round_to is not None:
                    ls[j] = round(ls[j - 1] + slope, 2)
                else:
                    ls[j] = ls[j - 1] + slope
            start = ls[i]
            start_idx = i
        i += 1
    return ls


def fill_in_copies(df: pd.DataFrame) -> pd.DataFrame:
    # if the year skips a value, fill in the value from the previous year
    new_df = []
    i = 0
    while i < len(df):
        if i == 0:
            new_df.append(df.iloc[i])
        else:
            if df.iloc[i]["year"] != df.iloc[i - 1]["year"] + 1:
                diff = df.iloc[i]["year"] - df.iloc[i - 1]["year"]
                for j in range(diff - 1):
                    new_row = df.iloc[i - 1].copy()
                    new_row["year"] += j + 1
                    new_df.append(new_row)
            new_df.append(df.iloc[i])
        i += 1

    new_df = pd.DataFrame(new_df)
    return new_df


dataset = []
state_pop_by_year = pd.read_csv("data/state_pop_by_year.csv")
state_pol_party_history = pd.read_csv("data/state_political_party_history.csv")
state_med_income_by_year = pd.read_csv("data/state_median_income_by_year.csv")
pub_mass_shooting_data = pd.read_csv("data/mass_shootings_wiki.csv")
michelle_updated_gun = pd.read_csv("controls/updated_gun.csv")
other_controls = fill_in_copies(pd.read_excel("controls/othercontrols.xlsx"))
for year in range(1984, 2022):
    for abbrev, state in MAP_ABBREV_TO_STATE.items():
        if state == "District of Columbia":
            continue
        relevant_pub_shootings = pub_mass_shooting_data[
            (pub_mass_shooting_data["year"] == year)
            & (pub_mass_shooting_data["state"] == state)
        ]
        relevant_pol_party_history = state_pol_party_history[
            (state_pol_party_history["year"] == year)
            & (state_pol_party_history["state"] == state)
        ]
        slice = other_controls[
            (other_controls["year"] == year) & (other_controls["statefip"] == state)
        ]["unemployed"]
        if len(slice) == 0:
            pdb.set_trace()

        dataset.append(
            {
                "state_year": f"{state}_{year}",
                "is_after_brady_bill_fed_check_law": int(year >= 1994),
                "has_universal_background_checks": int(
                    STATE_BG_CHECK_YEAR_ENACTED.get(abbrev, 9999) <= year
                ),
                "education_attainment": michelle_updated_gun[
                    michelle_updated_gun["state_year"] == f"{state}_{year}"
                ].iloc[0]["bachelors_and_above_perc"],
                "treatnew (21 states)": michelle_updated_gun[
                    michelle_updated_gun["state_year"] == f"{state}_{year}"
                ].iloc[0]["treatnew (21 states)"],
                "treatyearnew": michelle_updated_gun[
                    michelle_updated_gun["state_year"] == f"{state}_{year}"
                ].iloc[0]["treatyearnew"],
                "is_dem_majority": int(relevant_pol_party_history.iloc[0].is_democrat),
                "n_pub_mass_shooting_victims": relevant_pub_shootings["deaths"].sum()
                + relevant_pub_shootings["injuries"].sum(),
                "n_pub_mass_shootings": len(relevant_pub_shootings),
                "population": state_pop_by_year[state_pop_by_year["YEAR"] == year][
                    abbrev
                ].iloc[0]
                * 1000,
                "unemployed": other_controls[
                    (other_controls["year"] == year)
                    & (other_controls["statefip"] == state)
                ]["unemployed"].iloc[0],
                "p_white": other_controls[
                    (other_controls["year"] == year)
                    & (other_controls["statefip"] == state)
                ]["p_white"].iloc[0],
                "p_black": other_controls[
                    (other_controls["year"] == year)
                    & (other_controls["statefip"] == state)
                ]["p_black"].iloc[0],
                "p_asian": other_controls[
                    (other_controls["year"] == year)
                    & (other_controls["statefip"] == state)
                ]["p_asian"].iloc[0],
                "p_nativeamerican": other_controls[
                    (other_controls["year"] == year)
                    & (other_controls["statefip"] == state)
                ]["p_nativeamerican"].iloc[0],
                "p_nonwhite": other_controls[
                    (other_controls["year"] == year)
                    & (other_controls["statefip"] == state)
                ]["p_nonwhite"].iloc[0],
                "median_income": state_med_income_by_year[
                    state_med_income_by_year["YEAR"] == year
                ][abbrev].iloc[0],
            }
        )


master_df = pd.DataFrame(dataset)
master_df = master_df.sort_values(by=["state_year"])
# interpolate columns with repeated values
master_df["education_attainment"] = interpolate(
    master_df["education_attainment"].tolist(), round_to=2
)
# interpolate other controls
master_df["unemployed"] = interpolate(master_df["unemployed"].tolist())
master_df["p_white"] = interpolate(master_df["p_white"].tolist())
master_df["p_black"] = interpolate(master_df["p_black"].tolist())
master_df["p_asian"] = interpolate(master_df["p_asian"].tolist())
master_df["p_nativeamerican"] = interpolate(master_df["p_nativeamerican"].tolist())
master_df["p_nonwhite"] = interpolate(master_df["p_nonwhite"].tolist())

master_df.to_csv("data/econ_gun_dataset.csv", index=False)
