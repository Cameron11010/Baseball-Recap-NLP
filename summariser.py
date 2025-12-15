# summariser.py
from typing import Dict

def summarise_game(summary: Dict, perspective: str = "casual") -> str:
    """
    Generate a natural language recap of a game.

    Parameters:
    - summary: parsed game dictionary from parser.py
    - perspective: "casual", "statistical", "visiting_team", "home_team"
    """
    lines = []

    visiting = summary["visiting_team"]
    home = summary["home_team"]
    vis_score = summary["final_vis_score"]
    home_score = summary["final_home_score"]

    # Header
    if perspective == "casual":
        lines.append(f"Game recap: {visiting} vs {home}")
        lines.append(f"Final score: {visiting} {vis_score}, {home} {home_score}\n")
    elif perspective == "statistical":
        lines.append(f"Game: {summary['game_id']}")
        lines.append(f"{visiting}: {vis_score} runs, {home}: {home_score} runs\n")
    elif perspective == "visiting_team":
        lines.append(f"{visiting} fans, here’s your recap:")
        lines.append(f"Final: {visiting} {vis_score} - {home} {home_score}\n")
    elif perspective == "home_team":
        lines.append(f"{home} fans, here’s your recap:")
        lines.append(f"Final: {home} {home_score} - {visiting} {vis_score}\n")

    # Walkoff note
    if summary.get("walkoff"):
        lines.append("The game ended with a dramatic walk-off!\n")

    # Inning-by-inning summary
    lines.append("Inning-by-inning scores:")
    for inning in summary["innings"]:
        lines.append(f"Inning {inning['inning']}: {visiting} {inning['vis_score']}, {home} {inning['home_score']}")

    # Scoring plays
    if summary["scoring_plays"]:
        lines.append("\nScoring plays:")
        for play in summary["scoring_plays"]:
            batter = play["batter"]
            event = play["event_text"]
            rbi = play["RBI"]
            inning = play["inning"]
            # Determine which team batted
            batting_team = visiting if play["batting_team"] == visiting else home
            if perspective in ["casual", "home_team", "visiting_team"]:
                lines.append(f"Inning {inning}, {batting_team}: {batter} drove in {rbi} run(s) with {event}.")
            elif perspective == "statistical":
                lines.append(f"Inning {inning}: {batter} ({batting_team}) RBI={rbi}, event={event}")

    # Home runs
    if summary["home_runs"]:
        hr_lines = []
        for hr in summary["home_runs"]:
            team_name = visiting if hr["team"] == visiting else home
            hr_lines.append(f"{hr['batter']} ({team_name})")
        lines.append("\nHome runs: " + ", ".join(hr_lines))

    # Strikeouts
    if summary["strikeouts"]:
        so_lines = []
        for so in summary["strikeouts"]:
            so_lines.append(f"{so['batter']} struck out vs {so['pitcher']}")
        if perspective != "casual":
            lines.append("\nStrikeouts: " + "; ".join(so_lines))

    # Walks / HBPs
    if summary["walks"]:
        walk_lines = []
        for w in summary["walks"]:
            walk_lines.append(f"{w['batter']} ({w['type']}) by {w['pitcher']}")
        if perspective == "statistical":
            lines.append("\nWalks / HBPs: " + "; ".join(walk_lines))

    # Stolen bases / caught stealings
    if summary["stolen_bases"]:
        sb_lines = [f"{sb['runner']} stole a base in inning {sb['inning']}" for sb in summary["stolen_bases"]]
        lines.append("\nStolen bases: " + "; ".join(sb_lines))
    if summary["caught_stealings"]:
        cs_lines = [f"{cs['runner']} was caught stealing in inning {cs['inning']}" for cs in summary["caught_stealings"]]
        lines.append("\nCaught stealings: " + "; ".join(cs_lines))

    return "\n".join(lines)
