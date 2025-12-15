import pandas as pd
import os
import re

EVENTS_PATH = "bevent/2025eve/2025events.xlsx"
ROSTER_FOLDER = "bevent/2025eve/"

# -------------------------
# COLUMN CLEANING
# -------------------------

def clean_column_name(col: str) -> str:
    """Clean column names: remove asterisks, trim, replace spaces with underscores."""
    col = col.strip()
    col = col.replace("*", "")
    col = re.sub(r"\s+", "_", col)
    col = col.replace("#", "")
    return col.lower()

# -------------------------
# LOAD EVENTS FILE
# -------------------------

def load_events():
    df = pd.read_excel(EVENTS_PATH)

    # Clean columns
    df.columns = [clean_column_name(c) for c in df.columns]

    return df


# -------------------------
# LOAD ROSTERS
# -------------------------

def load_rosters():
    roster_map = {}

    for file in os.listdir(ROSTER_FOLDER):
        if file.endswith(".ROS"):
            team = file.replace(".ROS", "")
            path = os.path.join(ROSTER_FOLDER, file)

            with open(path, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        player_id = parts[0]
                        last = parts[1]
                        first = parts[2]

                        # Build full name: "First Last"
                        full_name = f"{first} {last}"

                        roster_map[player_id] = full_name

    return roster_map


# -------------------------
# DECODE PLAYER IDs
# -------------------------

def decode_players(df, roster_map):
    """Replace player IDs with actual names in all relevant columns."""
    # Columns based on your sample
    player_columns = [
        "batter", "res_batter", "pitcher", "res_pitcher",
        "catcher", "first_base", "second_base", "third_base",
        "shortstop", "left_field", "center_field", "right_field",
        "first_runner", "second_runner", "third_runner",
        "fielder_with_first_putout",
        "fielder_with_second_putout",
        "fielder_with_third_putout",
        "fielder_with_first_assist",
        "fielder_with_second_assist",
        "fielder_with_third_assist",
        "fielder_with_fourth_assist",
        "fielder_with_fifth_assist",
    ]

    for col in player_columns:
        if col in df.columns:
            df[col] = df[col].map(roster_map).fillna(df[col])

    return df


# -------------------------
# GAME SELECTION
# -------------------------

def get_game_df(df, game_id):
    """Return all rows for a single game."""
    return df[df["game_id"] == game_id].copy()


# -------------------------
# FULL PIPELINE
# -------------------------

def load_and_prepare():
    df = load_events()
    rosters = load_rosters()
    df = decode_players(df, rosters)
    return df, rosters
