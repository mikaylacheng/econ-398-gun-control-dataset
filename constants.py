MAP_STATE_TO_ABBREV = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}
MAP_ABBREV_TO_STATE = {v: k for k, v in MAP_STATE_TO_ABBREV.items()}
STATES = sorted(list(MAP_STATE_TO_ABBREV.keys()), reverse=True)

# Federal law Gun Control Act of 1968 requires background checks for 18+ years old for shotguns, rifles or ammo.
# 21 years or older for handguns.

# States that require background checks for all firearms, including private sales
STATES_WITH_BG_CHECKS = [
    MAP_ABBREV_TO_STATE[x]
    for x in [
        "CA",
        "CO",
        "CT",
        "DE",
        "DC",
        "NV",
        "NM",
        "NJ",
        "NY",
        "VA",
        "MD",
        "OR",
        "RI",
        "VT",
        "WA",
    ]
]

# Background check years per state
STATE_BG_CHECK_YEAR_ENACTED = {
    "CA": 1991,
    "CO": 2013,
    "CT": 1993,
    "DE": 2016,
    "MA": 2021,
    "NV": 2019,
    "NJ": 2002,
    "NM": 2019,
    "NY": 2013,
    "OR": 2015,
    "RI": 2021,
    "VT": 2018,
    "VA": 2020,
    "WA": 2014,
}

assert len(STATES) == 51, "Expected 51 states but got {}".format(len(STATES))
assert len(STATES_WITH_BG_CHECKS) == 15
assert len(MAP_STATE_TO_ABBREV) == 51
