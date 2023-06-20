import pandas as pd
import requests
from constants import *
from tqdm import tqdm

merged = None
for state_abbreviation in tqdm(list(MAP_ABBREV_TO_STATE.keys())):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id={state_abbreviation}POP&scale=left&cosd=1900-01-01&coed=2022-01-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-06-02&revision_date=2023-06-02&nd=1900-01-01"
    data = requests.get(url)
    with open("tmp.csv", "w") as f:
        f.write(data.text)
    df = pd.read_csv("tmp.csv")
    merged = df if merged is None else merged.merge(df, on="DATE")

merged["YEAR"] = merged["DATE"].apply(lambda x: x[:4])
# Remove the POP from each column name
merged.columns = [col[:-3] if col.endswith("POP") else col for col in merged.columns]
merged.to_csv("data/state_pop_by_year.csv", index=False)
