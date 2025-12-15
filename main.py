from loader import load_and_prepare, get_game_df
from parser import parse_game

# Load all events and rosters
events_df, rosters = load_and_prepare()

# List available game IDs
available_ids = events_df["game_id"].dropna().unique()
print("Available game IDs:", available_ids[:10], "...")  # first 10 only

# Select a game (first available)
game_id = available_ids[0]
print(f"\nUsing game ID: {game_id}\n")

# Load DataFrame for that game
game_df = get_game_df(events_df, game_id)
if game_df.empty:
    print(f"No data found for game ID {game_id}.")
    exit(0)

# Parse into structured summary
summary = parse_game(game_df)

vis = summary["visiting_team"]
home = summary["home_team"]

# ---------------------
# GAME HEADER
# ---------------------
print(f"Game recap: {vis} vs {home}")
print(f"Final score: {vis} {int(summary['final_vis_score'])}, {home} {int(summary['final_home_score'])}\n")

# ---------------------
# INNING SCORES
# ---------------------
print("Inning-by-inning scores:")
for inning in summary["innings"]:
    print(f"Inning {int(inning['inning'])}: "
          f"{vis} {int(inning['vis_score'])}, {home} {int(inning['home_score'])}")
print()

# ---------------------
# SCORING PLAYS
# ---------------------
print("Scoring plays:")
for play in summary["scoring_plays"]:
    print(f"Inning {int(play['inning'])}, {play['batting_team']}: "
          f"{play['batter']} drove in {int(play['RBI'])} run(s) with {play['event_readable']}")
print()

# ---------------------
# STRIKEOUTS
# ---------------------
print("Strikeouts:")
for so in summary["strikeouts"]:
    print(f"{so['batter']} struck out vs {so['pitcher']}: {so['event_readable']}")
print()

# ---------------------
# WALKS / HBP
# ---------------------
print("Walks / Hit by pitch:")
for w in summary["walks"]:
    print(f"{w['batter']} vs {w['pitcher']}: {w['event_readable']}")
print()

# ---------------------
# STOLEN BASES
# ---------------------
print("Stolen bases:")
for sb in summary["stolen_bases"]:
    print(f"{sb['runner']} stole a base in inning {int(sb['inning'])}: {sb['event_readable']}")
print()

# ---------------------
# CAUGHT STEALINGS
# ---------------------
print("Caught stealings:")
for cs in summary["caught_stealings"]:
    print(f"{cs['runner']} was caught stealing in inning {int(cs['inning'])}: {cs['event_readable']}")
