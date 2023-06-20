from constants import *
import pandas as pd
import requests

merged = None
for abbrev, state in MAP_ABBREV_TO_STATE.items():
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=MEHOINUS{abbrev}A672N&scale=left&cosd=1984-01-01&coed=2021-01-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-06-03&revision_date=2023-06-03&nd=1984-01-01"
    data = requests.get(url)
    with open(f"tmp.csv", "w") as f:
        f.write(data.text)
    df = pd.read_csv(f"tmp.csv")
    df["YEAR"] = df["DATE"].apply(lambda x: x[:4])
    df.rename(columns={f"MEHOINUS{abbrev}A672N": abbrev}, inplace=True)
    df = df[["YEAR", abbrev]]
    merged = df if merged is None else merged.merge(df, on="YEAR")

merged.to_csv("data/state_median_income_by_year.csv", index=False)
