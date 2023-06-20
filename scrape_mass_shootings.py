import requests
import traceback
import pandas as pd
import json
import pdb
from constants import STATES
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd

"""
Scrape victim statistics from public and highly visible mass shootings
"""


def flat(ls):
    return [item for sublist in ls for item in sublist]


def find_th(element, val):
    return element.name == "th" and val in element.text


def parse_infobox(infobox):
    possible_labels = ["Deaths", "Death(s)", "Killed", "Victims"]
    for label in possible_labels:
        try:
            deaths = infobox.find(lambda x: find_th(x, label)).find_next("td").text
            break
        except:
            pass
    deaths = int(deaths.split("[")[0].split("(")[0].split(" ")[0])

    try:
        injuries = infobox.find(lambda x: find_th(x, "Injured")).find_next("td").text
    except:
        injuries = "-1"
    injuries = "".join(
        x for x in injuries if x.isdigit() or x == " " or x == "[" or x == "("
    ).strip()
    injuries = injuries.split("[")[0].split("(")[0].strip()
    injuries = int(injuries)

    date = infobox.find(lambda x: find_th(x, "Date")).find_next("td").text

    try:
        # find the td that goes with the th "Location"
        location = infobox.find(lambda x: find_th(x, "Location")).find_next("td").text
        state = next(s for s in STATES if s in location)
    except:
        # find the td that goes with the th "State"
        state = infobox.find(lambda x: find_th(x, "State(s)")).find_next("td").text

    return {
        "deaths": deaths,
        "injuries": injuries,
        "date": date,
        "state": state,
    }


def parse_page(url_path):
    if url_path == "/wiki/Darnell_Collins":
        return {
            "deaths": 7,
            "injuries": 3,
            "date": "June 1995",
            "state": "New Jersey",
        }
    elif url_path == "/wiki/Connecticut_Lottery_shooting":
        return {
            "deaths": 5,
            "injuries": 0,
            "date": "March 1998",
            "state": "Connecticut",
        }
    elif url_path == "/wiki/Trang_Dai_massacre":
        return {
            "deaths": 5,
            "injuries": 5,
            "date": "July 5, 1998",
            "state": "Washington",
        }
    elif url_path == "/wiki/Lex_Street_massacre":
        return {
            "deaths": 7,
            "injuries": 3,
            "date": "December 28, 2000",
            "state": "Pennsylvania",
        }
    elif url_path == "/wiki/Granite_Hills_High_School_shooting":
        return {
            "deaths": 0,
            "injuries": 5,
            "date": "March 22, 2001",
            "state": "California",
        }
    elif url_path == "/wiki/Superbike_murders":
        return {
            "deaths": 4,
            "injuries": 0,
            "date": "November 6, 2003",
            "state": "South Carolina",
        }
    elif url_path == "/wiki/Dunbar_Vocational_High_School_shooting":
        return {
            "deaths": 2,
            "injuries": 3,
            "date": "January 9, 2009",
            "state": "Illinois",
        }
    elif url_path == "/wiki/2009_Saipan_shootings":
        return None
    elif url_path == "/wiki/Doe_B":
        return {
            "deaths": 2,
            "injuries": 6,
            "date": "December 28, 2013",
            "state": "Alabama",
        }
    elif url_path == "/wiki/Killing_of_Nathaniel_Torres":
        return None
    elif url_path == "/wiki/Rosemary_Anderson_High_School_shooting":
        return {
            "deaths": 0,
            "injuries": 4,
            "date": "December 12, 2014",
            "state": "Oregon",
        }
    elif url_path == "/wiki/Charleston_church_shooting":
        return {
            "deaths": 9,
            "injuries": 1,
            "date": "June 17, 2015",
            "state": "South Carolina",
        }
    elif url_path == "/wiki/FreightCar_America_shooting":
        return {
            "deaths": 2,
            "injuries": 3,
            "date": "July 30, 2016",
            "state": "Virginia",
        }
    elif url_path == "/wiki/2016_Kansas%E2%80%93Missouri_murder_spree":
        return {"deaths": 5, "injuries": 0, "date": "March 2016", "state": "Kansas"}
    elif url_path == "/wiki/Madison_High_School_shooting":
        return {
            "deaths": 0,
            "injuries": 4,
            "date": "Feburary 29, 2016",
            "state": "Ohio",
        }
    elif url_path == "/wiki/Freeman_High_School_shooting":
        return {
            "deaths": 1,
            "injuries": 3,
            "date": "September 3, 2017",
            "state": "Washington",
        }
    elif url_path == "/wiki/Rolling_Oaks_Mall_shooting":
        return {
            "deaths": 1,
            "injuries": 7,
            "date": "January 22, 2017",
            "state": "Texas",
        }
    elif url_path == "/wiki/Fort_Gibson_Middle_School_shooting":
        return {
            "deaths": 0,
            "injuries": 4,
            "date": "December 6, 1999",
            "state": "Oklahoma",
        }
    elif url_path == "/wiki/Heritage_High_School_shooting":
        return {
            "deaths": 0,
            "injuries": 6,
            "date": "May 20, 1999",
            "state": "Georgia",
        }
    elif url_path == "/wiki/Cupertino_quarry_shooting":
        return {
            "deaths": 3,
            "injuries": 6,
            "date": "October 5, 2011",
            "state": "California",
        }
    elif url_path == "/wiki/2012_Gilbert_shooting":
        return {
            "deaths": 5,
            "injuries": 0,
            "date": "May 2, 2012",
            "state": "Arizona",
        }
    elif url_path == "/wiki/J._T._Ready":
        return {
            "deaths": 4,
            "injuries": 0,
            "date": "May 2, 2012",
            "state": "Arizona",
        }
    elif url_path == "/wiki/Melcroft_shooting":
        return {
            "deaths": 5,
            "injuries": 6,
            "date": "January 28, 2018",
            "state": "Pennsylvania",
        }
    elif url_path == "/wiki/2020_Williamsburg_massacre":
        return {
            "deaths": 6,
            "injuries": 0,
            "date": "December 8, 2020",
            "state": "Virginia",
        }
    elif url_path == "/wiki/Aguanga_shooting":
        return {
            "deaths": 7,
            "injuries": 0,
            "date": "September 7, 2020",
            "state": "California",
        }
    elif url_path == "/wiki/2020_Bellevue,_Nebraska_shooting":
        return {
            "deaths": 2,
            "injuries": 2,
            "date": "November 21, 2020",
            "state": "Nebraska",
        }
    elif url_path == "/wiki/Valhermoso_Springs_shooting":
        return {
            "deaths": 7,
            "injuries": 0,
            "date": "June 5, 2020",
            "state": "Alabama",
        }
    elif url_path == "/wiki/Aurora_Central_High_School_shooting":
        return {
            "deaths": 0,
            "injuries": 6,
            "date": "November 15, 2021",
            "state": "Colorado",
        }
    elif url_path == "/wiki/Boise_Towne_Square_shooting":
        return {
            "deaths": 2,
            "injuries": 4,
            "date": "October 25, 2021",
            "state": "Idaho",
        }
    elif url_path == "/wiki/Bryan_shooting":
        return {
            "deaths": 1,
            "injuries": 5,
            "date": "April 8, 2021",
            "state": "Texas",
        }
    elif url_path == "/wiki/2021_Denver_shootings":
        return {
            "deaths": 5,
            "injuries": 2,
            "date": "December 27, 2021",
            "state": "Colorado",
        }
    elif url_path == "/wiki/2021_Evanston_shooting":
        return {
            "deaths": 5,
            "injuries": 2,
            "date": "January 9, 2021",
            "state": "Illinois",
        }
    elif url_path == "/wiki/2021_Lakeland,_Florida_shooting":
        return {
            "deaths": 4,
            "injuries": 2,
            "date": "September 5, 2021",
            "state": "Florida",
        }
    elif url_path == "/wiki/Hazelwood_massacre":
        return {
            "deaths": 8,
            "injuries": 0,
            "date": "June 14, 1971",
            "state": "Michigan",
        }
    elif url_path == "/wiki/Mansfield_Timberview_High_School_shooting":
        return {
            "deaths": 0,
            "injuries": 3,
            "date": "October 6, 2021",
            "state": "Texas",
        }
    elif url_path == "/wiki/2021_Normal_shooting":
        return {
            "deaths": 3,
            "injuries": 3,
            "date": "August 31, 2021",
            "state": "Illinois",
        }
    elif url_path == "/wiki/Olney_Transportation_Center_shooting":
        return {
            "deaths": 0,
            "injuries": 8,
            "date": "February 18, 2021",
            "state": "Pennsylvania",
        }
    elif url_path == "/wiki/2021_Providence_shooting":
        return {
            "deaths": 0,
            "injuries": 8,
            "date": "May 14, 2021",
            "state": "Rhode Island",
        }
    elif url_path == "/wiki/West_Jefferson_shooting":
        return {
            "deaths": 4,
            "injuries": 0,
            "date": "May 24, 2021",
            "state": "North Carolina",
        }
    elif url_path == "/wiki/Dumas_shooting":
        return {
            "deaths": 1,
            "injuries": 26,
            "date": "March 19, 2022",
            "state": "Arkansas",
        }
    elif url_path == "/wiki/East_Glacier_Park_Village_attack":
        return {
            "deaths": 2,
            "injuries": 2,
            "date": "July 19, 2022",
            "state": "Montana",
        }
    elif url_path == "/wiki/2022_Tulsa_hospital_shooting":
        return {
            "deaths": 5,
            "injuries": 1,
            "date": "June 1, 2022",
            "state": "Oklahoma",
        }
    elif url_path == "/wiki/W.O.W._Hall_shooting":
        return {
            "deaths": 0,
            "injuries": 6,
            "date": "January 14, 2022",
            "state": "Oregon",
        }
    elif url_path == "/wiki/2023_El_Paso_shooting":
        return {
            "deaths": 1,
            "injuries": 3,
            "date": "February 15, 2023",
            "state": "Texas",
        }
    elif url_path == "/wiki/1985_Murray%E2%80%93Wright_High_School_shooting":
        return {
            "deaths": 0,
            "injuries": 6,
            "date": "October 18, 1985",
            "state": "Michigan",
        }
    elif url_path == "/wiki/1969_Greensboro_uprising":
        return {
            "deaths": 2,
            "injuries": 18,
            "date": "May 25, 1969",
            "state": "North Carolina",
        }
    elif (
        url_path == "/wiki/Pacific_Southwest_Airlines_Flight_1771"
        or url_path == "/wiki/Harlem_Nights_massacre"
        or url_path == "/wiki/Henry%27s_Pub_hostage_incident"
        or url_path == "/wiki/Glenville_shootout"
        or url_path == "/wiki/Robison_family_murders"
        or url_path == "/wiki/Ronald_DeFeo_Jr."
        or url_path == "/wiki/Attempted_assassination_of_George_Wallace"
        or url_path == "/wiki/Assassination_of_William_Cann"
        or url_path == "/wiki/Blackfriars_Massacre"
    ):
        return None
    elif url_path == "/wiki/Murder_of_Nick_Corwin":
        return None
    elif url_path == "/wiki/Palm_Bay_shooting":
        return {
            "deaths": 6,
            "injuries": 10,
            "date": "April 23, 1987",
            "state": "Florida",
        }
    elif (
        url_path == "/wiki/Englewood,_Chicago_shooting"
        or url_path == "/wiki/Red_Bluff_shooting"
    ):
        return None
    elif "List_of_mass_shootings_in_the_United_States_in_" in url_path:
        return None

    print(url_path)
    page = requests.get("https://en.wikipedia.org" + url_path)
    soup = BeautifulSoup(page.content, "html.parser")
    infoboxes = soup.find_all("table", {"class": "infobox"})
    for infobox in infoboxes:
        try:
            return parse_infobox(infobox)
        except Exception as e:
            print(traceback.format_exc())
    raise Exception("No infobox compatible")


mass_shootings = []
for year in tqdm(range(1960, 2024)):
    shooting_list = f"https://en.wikipedia.org/wiki/Category:{year}_mass_shootings_in_the_United_States"
    page = requests.get(shooting_list)
    soup = BeautifulSoup(page.content, "html.parser")
    subpages = soup.find("div", {"id": "mw-pages"})
    if subpages is None:
        continue
    block = subpages.find("div", {"class": "mw-category"})
    if block is None:
        continue
    link_groups = [m.find_all("a") for m in block.find_all("li")]
    links = [x["href"] for x in flat(link_groups) if "Category:" not in x["href"]]
    results = [parse_page(link) for link in links]
    for i, result in enumerate(results):
        if result is not None:
            results[i]["url"] = links[i]
    mass_shootings.extend([x for x in results if x is not None])


def parse_date(date: str):
    parts = (
        date.replace("\xa0", " ")
        .replace(";", "")
        .replace(".", "")
        .replace("c", " ")
        .replace("2:23 p", " ")
        .replace("3:30 a", " ")
        .split(" ")
    )
    for part in parts:
        # check if part is int

        if part.isnumeric() and int(part) > 1940:
            print(date, part)
            return int(part)
    pdb.set_trace()
    raise Exception("No year found " + date)


df = pd.DataFrame(mass_shootings)
df["year"] = df.date.apply(parse_date)
df.to_csv("data/mass_shootings_wiki.csv", index=False)
