import ollama


def generate_recap(summary: dict, favored_team: str = "Phillies") -> str:

    # ---------------------
    # Build the prompt
    # ---------------------
    vis = summary["visiting_team"]
    home = summary["home_team"]

    lines = []
    lines.append(f"The selected team is: {favored_team}")
    lines.append(f"Using game ID: {home} vs {vis}")
    lines.append("\nGame recap:")
    lines.append(f"{vis} vs {home}")
    lines.append(f"Final score: {vis} {int(summary['final_vis_score'])}, {home} {int(summary['final_home_score'])}\n")

    # Inning-by-inning scores
    lines.append("Inning-by-inning scores:")
    for inning in summary["innings"]:
        lines.append(f"Inning {int(inning['inning'])}: {vis} {int(inning['vis_score'])}, {home} {int(inning['home_score'])}")
    lines.append("")

    # Scoring plays
    lines.append("Scoring plays:")
    for play in summary["scoring_plays"]:
        lines.append(f"Inning {int(play['inning'])}, {play['batting_team']}: {play['batter']} drove in {int(play['RBI'])} run(s) with {play['event_readable']}")
    lines.append("")

    # Strikeouts
    lines.append("Strikeouts:")
    for so in summary["strikeouts"]:
        lines.append(f"{so['batter']} struck out vs {so['pitcher']}: {so['event_readable']}")
    lines.append("")

    # Walks / HBP
    lines.append("Walks / Hit by pitch:")
    for w in summary["walks"]:
        lines.append(f"{w['batter']} vs {w['pitcher']}: {w['event_readable']}")
    lines.append("")

    # Stolen bases
    lines.append("Stolen bases:")
    for sb in summary["stolen_bases"]:
        lines.append(f"{sb['runner']} stole a base in inning {int(sb['inning'])}: {sb['event_readable']}")
    lines.append("")

    # Caught stealings
    lines.append("Caught stealings:")
    for cs in summary["caught_stealings"]:
        lines.append(f"{cs['runner']} was caught stealing in inning {int(cs['inning'])}: {cs['event_readable']}")
    lines.append("")

    prompt_text = "\n".join(lines)

    # ---------------------
    # Send to Ollama
    # ---------------------
    client = ollama.Client()
    model = "Tommy_John"

    response = client.generate(model=model, prompt=prompt_text)
    return response.response
