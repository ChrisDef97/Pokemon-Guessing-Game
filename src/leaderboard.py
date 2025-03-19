import os
import json

LEADERBOARD_FILE = 'leaderboard.json'

# Initialize the leaderboard file if not present
def initialize_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump({
                'easy': {'single_gen': [], 'all_gen': []},
                'hard': {'single_gen': [], 'all_gen': []}
            }, f)

# Load the leaderboard
def load_leaderboard():
    with open(LEADERBOARD_FILE, 'r') as f:
        return json.load(f)

# Save the updated leaderboard back to the file
def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=4)

# Function to add a score to the leaderboard
def add_to_leaderboard(player_name, generation, mode, guesses, elapsed_time, pokemon_name):
    leaderboard = load_leaderboard()

    # Determine the category (single generation or all generations)
    if generation == "ALL":
        category = 'all_gen'
        generation_display = "ALL"
    else:
        category = 'single_gen'
        generation_display = f"Generation {generation}"

    # Create the leaderboard entry
    entry = {
        'name': player_name,
        'generation': generation_display,
        'mode': mode.capitalize(),
        'guesses': guesses,
        'time': elapsed_time,
        'pokemon': pokemon_name
    }

    # Append the entry to the appropriate leaderboard and sort it
    leaderboard[mode][category].append(entry)
    leaderboard[mode][category] = sorted(leaderboard[mode][category], key=lambda x: (x['guesses'], x['time']))

    # Ensure only top 10 entries are stored
    leaderboard[mode][category] = leaderboard[mode][category][:10]

    # Save the updated leaderboard
    save_leaderboard(leaderboard)


# Function to display the leaderboard
def display_leaderboard(mode=None, generation_label=None):
    leaderboard = load_leaderboard()

    print("\n--- Leaderboard ---")
    for m in ['easy', 'hard']:
        for category in ['single_gen', 'all_gen']:
            if mode and m != mode:  # If a mode is specified and it's not the current mode, skip it
                continue

            category_name = "All Generations" if category == 'all_gen' else "Single Generation"
            print(f"\nMode: {m.capitalize()}, Category: {category_name}")
            print(f"{'Pos':<4} {'Name':<10} {'Generation':<10} {'Guesses':<8} {'Time':<6} {'Pokemon'}")

            for i, entry in enumerate(leaderboard[m][category], 1):
                generation_display = entry['generation'] if entry['generation'] == "ALL" else entry['generation'].split()[-1]
                time_display = f"{float(entry['time']):.2f}"  # Limit time to 2 decimal places
                print(f"{i:<4} {entry['name']:<10} {generation_display:<10} {entry['guesses']:<8} {time_display:<6} {entry['pokemon']}")

# Admin function to reset the leaderboard
def reset_leaderboard():
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump({
            'easy': {'single_gen': [], 'all_gen': []},
            'hard': {'single_gen': [], 'all_gen': []}
        }, f)
    print("Leaderboard reset.")
reset_leaderboard()