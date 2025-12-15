import pandas as pd

# -------------------------
# HELPER MAPPINGS
# -------------------------

FIELDERS = {
    "1": "pitcher",
    "2": "catcher",
    "3": "first baseman",
    "4": "second baseman",
    "5": "third baseman",
    "6": "shortstop",
    "7": "left fielder",
    "8": "center fielder",
    "9": "right fielder"
}

HIT_TYPES = {
    "S": "Single",
    "D": "Double",
    "T": "Triple",
    "HR": "Home run",
    "H": "Home run"
}

OUT_TYPES = {
    "F": "Fly out",
    "G": "Ground out",
    "L": "Line out",
    "P": "Pop out",
    "DP": "Double play",
    "TP": "Triple play",
    "SF": "Sacrifice fly",
    "SH": "Sacrifice bunt",
    "FC": "Fielder's choice",
    "E": "Error",
    "K": "Strikeout"
}

BASE_EVENTS = {
    "SB": "Stolen base",
    "CS": "Caught stealing",
    "PB": "Passed ball",
    "WP": "Wild pitch",
    "DI": "Defensive indifference",
    "OA": "Other advance",
    "PO": "Pickoff",
    "HP": "Hit by pitch",
    "W": "Walk",
    "IW": "Intentional walk"
}

# -------------------------
# HELPER FUNCTION
# -------------------------

def translate_advances(part: str) -> str:
    """Converts runner advance codes into readable text."""
    return part.replace(";", "; ").replace("-", " to ")

# -------------------------
# EVENT DECODING
# -------------------------

def decode_event(event_code: str) -> str:
    if not event_code:
        return "Unknown play"

    # Base runner events
    for code, text in BASE_EVENTS.items():
        if event_code.startswith(code):
            parts = event_code.split(".")
            desc = text
            if len(parts) > 1:
                desc += f"; {translate_advances(parts[1])}"
            return desc

    # Strikeouts
    if event_code.startswith("K"):
        parts = event_code.split(".")
        desc = "Strikeout"
        if len(parts) > 1:
            desc += f"; {translate_advances(parts[1])}"
        return desc

    # Hits
    for code, text in HIT_TYPES.items():
        if event_code.startswith(code):
            if code in ["HR", "H"]:
                return "Home run"  # Simplified for HRs
            parts = event_code.split(".")
            desc = text
            # Runner advances
            if len(parts) > 1:
                desc += f"; {translate_advances(parts[1])}"
            return desc

    # Outs
    for code, text in OUT_TYPES.items():
        if event_code.startswith(code):
            parts = event_code.split(".")
            desc = text
            if len(parts) > 1:
                desc += f"; {translate_advances(parts[1])}"
            return desc

    return event_code

# -------------------------
# GAME PARSING
# -------------------------

def parse_game(game_df: pd.DataFrame):
    """
    Parse a single game's DataFrame into a structured summary object.
    """
    summary = {}

    # Home team from first 3 chars of game_id
    game_id = game_df["game_id"].iloc[0]
    summary["home_team"] = game_id[:3]

    # Visiting team is always the second column after game_id
    summary["visiting_team"] = game_df.iloc[0, 1]  # second column

    # Final scores
    summary["final_vis_score"] = game_df["vis_score"].iloc[-1]
    summary["final_home_score"] = game_df["home_score"].iloc[-1]

    # Inning-by-inning scores
    summary["innings"] = []
    for inning, df_inning in game_df.groupby("inning"):
        vis_runs = df_inning["vis_score"].iloc[-1]
        home_runs = df_inning["home_score"].iloc[-1]
        summary["innings"].append({
            "inning": inning,
            "vis_score": vis_runs,
            "home_score": home_runs
        })

    # Scoring plays
    summary["scoring_plays"] = []
    if "rbi_on_play" in game_df.columns:
        scoring_plays = game_df[game_df["rbi_on_play"] > 0]
        for _, row in scoring_plays.iterrows():
            event_plain = decode_event(row.get("event_text", ""))
            batting_team_name = summary["home_team"] if row["batting_team"] == 1 else summary["visiting_team"]
            summary["scoring_plays"].append({
                "inning": row["inning"],
                "batting_team": batting_team_name,
                "batter": row["batter"],
                "event_text": row.get("event_text", ""),
                "event_readable": event_plain,
                "RBI": row["rbi_on_play"],
                "pitch_sequence": row.get("pitch_sequence", "")
            })

    # Strikeouts
    so_plays = game_df[game_df["event_type"] == 3]
    summary["strikeouts"] = []
    for _, row in so_plays.iterrows():
        event_plain = decode_event(row.get("event_text", ""))
        summary["strikeouts"].append({
            "inning": row["inning"],
            "batter": row["batter"],
            "pitcher": row["pitcher"],
            "event_text": row.get("event_text", ""),
            "event_readable": event_plain
        })

    # Walks / HBP
    walk_plays = game_df[game_df["event_type"].isin([14,15,16])]
    summary["walks"] = []
    for _, row in walk_plays.iterrows():
        event_plain = decode_event(row.get("event_text", ""))
        summary["walks"].append({
            "inning": row["inning"],
            "batter": row["batter"],
            "pitcher": row["pitcher"],
            "event_text": row.get("event_text", ""),
            "event_readable": event_plain
        })

    # Stolen bases / caught stealings
    sb_plays = game_df[game_df["event_type"] == 4]
    cs_plays = game_df[game_df["event_type"] == 6]
    summary["stolen_bases"] = []
    for _, r in sb_plays.iterrows():
        event_plain = decode_event(r.get("event_text", ""))
        summary["stolen_bases"].append({
            "inning": r["inning"],
            "runner": r["first_runner"],
            "event_text": r.get("event_text", ""),
            "event_readable": event_plain
        })
    summary["caught_stealings"] = []
    for _, r in cs_plays.iterrows():
        event_plain = decode_event(r.get("event_text", ""))
        summary["caught_stealings"].append({
            "inning": r["inning"],
            "runner": r["first_runner"],
            "event_text": r.get("event_text", ""),
            "event_readable": event_plain
        })

    return summary
