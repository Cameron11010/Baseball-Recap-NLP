from loader import load_and_prepare, get_game_df
from game_parser import parse_game
from perspective import generate_recap

# ---------------------
# Load game data
# ---------------------
events_df, rosters = load_and_prepare()
available_ids = events_df["game_id"].dropna().unique()
game_id = available_ids[0]

game_df = get_game_df(events_df, game_id)
if game_df.empty:
    print(f"No data found for game ID {game_id}.")
    exit(0)

summary = parse_game(game_df)

# ---------------------
# Select team bias
# ---------------------
favored_team = "Toronto Blue Jays"  # change this to bias recap toward another team

# ---------------------
# Generate recap using LLM
# ---------------------
recap_text = generate_recap(summary, favored_team=favored_team)

print("LLM-generated recap:")
print(recap_text)
