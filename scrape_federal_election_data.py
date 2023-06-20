import requests
import pandas as pd
from bs4 import BeautifulSoup
from constants import *

merged = None
for state in STATES:
    url = f"https://www.270towin.com/states/{state.replace(' ', '_')}"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    # get table with id "recent_elections"
    table = soup.find("table", {"id": "recent_elections"})

    # for each tr
    state_political_party_history = []
    cur_result = []
    is_year_td = True
    for tr in table.find_all("tr"):
        # the year is the text of the first td
        if is_year_td:
            text = tr.find_all("td")[0].text
            cur_result.append(int(text))
            is_year_td = False
        else:
            dem = float(tr.find_all("td")[0].text.replace("%", ""))
            rep = float(tr.find_all("td")[2].text.replace("%", ""))
            cur_result.extend([dem > rep, dem, rep])
            state_political_party_history.append(tuple(cur_result))
            cur_result = []
            is_year_td = True

    state_political_party_history = sorted(
        state_political_party_history, key=lambda x: x[0]
    )
    full_state_political_party_history = []
    begin_year = 1976
    for i in range(begin_year, 2023):
        for j, (year, is_democrat, dem, rep) in enumerate(
            state_political_party_history
        ):
            if year == i:
                full_state_political_party_history.append((year, is_democrat, dem, rep))
                break
            elif year > i:
                full_state_political_party_history.append(
                    (
                        i,
                        state_political_party_history[j - 1][1],
                        state_political_party_history[j - 1][2],
                        state_political_party_history[j - 1][3],
                    )
                )
                break
            elif j == len(state_political_party_history) - 1:
                full_state_political_party_history.append((i, is_democrat, dem, rep))

    full_state_political_party_history = pd.DataFrame(
        [
            {
                "state": state,
                "year": year,
                "is_democrat": is_democrat,
                "dem": dem,
                "rep": rep,
            }
            for year, is_democrat, dem, rep in full_state_political_party_history
        ]
    )

    merged = (
        full_state_political_party_history
        if merged is None
        else pd.concat([full_state_political_party_history, merged])
    )
    print(merged)

merged.to_csv("data/state_political_party_history.csv", index=False)
