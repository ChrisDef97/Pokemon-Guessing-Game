import sqlite3
import random
import time
import pygame
import sys
import os
from background import Background  

DB_FILE_PATH = 'C:/Users/CHRISTIAN/OneDrive/Documents/Projects/Pokemon Guessing Game/database/pokemon.db'



# Initialize Pygame
pygame.init()

# Get the directory of the current file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Set paths using absolute paths
font_path = os.path.join(base_dir, "fonts", "font.ttf")
background_path = r'C:\Users\CHRISTIAN\OneDrive\Documents\Projects\Pokemon Guessing Game\src\images\GIF frames'

# Set up display
width, height = 1600, 1000  
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pokémon Guessing Game')
clock = pygame.time.Clock() # Create a clock object to control the frame rate
running = True  # Flag to keep the game running

font = pygame.font.Font(font_path, 40)
background = Background(r'C:\Users\CHRISTIAN\OneDrive\Documents\Projects\Pokemon Guessing Game\src\images\GIF frames')  # Adjust frame rate as needed


class Button:
    def __init__(self, text, x, y, font):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.width = self.calculate_width()
        self.height = self.calculate_height()
        self.button_color = (173, 216, 230)  # Light blue color
        self.border_color = (0, 0, 0)  # Black color for the border

    def calculate_width(self):
        return self.font.size(self.text)[0] + 20  # Add padding

    def calculate_height(self):
        return self.font.size(self.text)[1] + 10  # Add padding

    def draw(self, surface):
        # Draw button background
        pygame.draw.rect(surface, self.button_color, (self.x, self.y, self.width, self.height), border_radius=10)
        # Draw button border
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), 2, border_radius=10)
        # Draw button text
        text_surface = self.font.render(self.text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        # Check if the button is hovered by the mouse position
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

    def is_clicked(self, pos):
        # Check if the button is clicked by the mouse position
        return self.is_hovered(pos)  # Reuse the hover check for click

# Place this function outside the game loop, at the top of the script or in a separate file.
def render_multicolor_text(screen, font, text_parts, colors, x, y):
    total_width = 0
    for i, part in enumerate(text_parts):
        text_surface = font.render(part, True, colors[i])
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x + total_width, y)
        screen.blit(text_surface, text_rect)
        total_width += text_rect.width  # Increment x for the next part

# Function to fetch a random Pokémon from the selected generation(s)
def get_random_pokemon(generation=None):
    conn = sqlite3.connect(DB_FILE_PATH)
    cur = conn.cursor()

    # Fetch Pokémon based on the selected generation(s)
    if generation and generation != "ALL":
        cur.execute('SELECT * FROM Pokemon WHERE Generation = ?', (generation,))
    else:
        cur.execute('SELECT * FROM Pokemon')  # Select from all generations

    pokemon_list = cur.fetchall()
    conn.close()

    # Pick a random Pokémon
    if pokemon_list:
        return random.choice(pokemon_list)
    else:
        return None

# Function to display the hidden Pokémon name with underscores
def display_hidden_name(pokemon_name, revealed_indices):
    return ' '.join([pokemon_name[i] if i in revealed_indices else '_' for i in range(len(pokemon_name))])

# Timer functions
def start_timer():
    return time.time()

def get_elapsed_time(start_time):
    elapsed_seconds = time.time() - start_time
    minutes = int(elapsed_seconds // 60)
    seconds = int(elapsed_seconds % 60)
    return f"{minutes:02}:{seconds:02}"

    words = text.split(' ')
    rendered_words = [font.render(word, True, (255, 255, 255)) for word in words]

    # Calculate total width of all words combined
    total_text_width = sum(word.get_width() for word in rendered_words)
    
    # If the total width is less than the desired width, we need to add spaces
    if total_text_width < width:
        # Calculate total spaces needed
        space_width = font.render(' ', True, (255, 255, 255)).get_width()
        total_spaces = len(words) - 1  # Number of spaces between words

        # Calculate the extra space needed
        extra_space = (width - total_text_width) // total_spaces if total_spaces > 0 else 0

        # Adjust the positions of the rendered words
        x_offset = 0
        justified_lines = []
        for word in rendered_words:
            justified_lines.append((x_offset, word))
            x_offset += word.get_width() + extra_space + space_width  # Add space width and extra space
        
        return justified_lines
    else:
        # If the text is too wide, return without justification
        return [(0, word) for word in rendered_words]

def game_rules_screen():
    # Create a new font for the game rules screen
    rules_font = pygame.font.Font(font_path, 30)  # Font for the rules text
    title_font = pygame.font.Font(font_path, 48)  # Larger font for the title

    while True:
        screen.fill((128, 0, 128))  # Purple background
        # Title text
        title_text = title_font.render("Game Rules:", True, (255, 0, 0))  # Red color for the title
        title_rect = title_text.get_rect(center=(width // 2, 75))  # Center the title
        screen.blit(title_text, title_rect)

        # Updated rules text with detailed explanations for hints
        rules_text = [
            "1. You have to guess the Pokémon name based on the displayed clues.",
            "2. In Easy Mode:",
            "   - After 3 wrong guesses, you will receive the Pokémon's type as a hint.",
            "   - After 5 wrong guesses, you will get the Pokédex number.",
            "   - You'll start receiving letter hints every 2 wrong guesses after that.",
            "   - You'll have a timer to check how long it took you to guess the word.",
            "3. In Hard Mode:",
            "   - After 3 wrong guesses, you will receive the Pokémon's type as a hint.",
            "   - After 7 wrong guesses, you will get the Pokédex number.",
            "   - You will receive the first letter hint after 10 wrong guesses,",
            "     and every 5 wrong guesses after that.",
            "   - In this mode, you have a 5-minute timer, and if it reaches 0, you lose.",
            "4. The game ends when you guess the Pokémon correctly or when all",
            " letters are revealed.",
            "5. You can select a specific generation or all generations of Pokémon.",
            "6. Have fun and good luck!"
        ]

        y_offset = 150  # Starting position for the rules text
        for line in rules_text:
            # Split line into words and change colors for specific words/letters
            words = line.split(" ")
            x_offset = 35  # Reset x offset for each line
            for word in words:
                # Change color for specific letters/words
                if "Pokémon" in word:
                    colored_word = rules_font.render(word, True, (255, 0, 0))  # Red for Pokémon
                else:
                    colored_word = rules_font.render(word, True, (255, 255, 255))  # Default white
                
                # Position each word with an offset
                screen.blit(colored_word, (x_offset, y_offset))
                x_offset += colored_word.get_width() + 10  # Move x offset for next word

            y_offset += 50  # Increment y position for the next line

        # Back button
        back_button = Button("Back", width // 2 - 50, height - 80, rules_font)  # Use the new font here
        back_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and back_button.is_hovered(pygame.mouse.get_pos()):
                    return  # Go back to main menu

# Main menu screen
def main_menu():
    while True:
        screen.fill((128, 0, 128))  # Purple background
        

        # Draw the background
        background.draw(screen)

        # Use render_multicolor_text to render "Welcome to the" in blue
        render_multicolor_text(screen, font, ["Welcome to the"], [(0, 0, 139)], width // 2 - 190, 150)
        
        # Use render_multicolor_text to render "Pokémon" in red and "Guessing Game!" in deep blue
        render_multicolor_text(screen, font, ["Pokémon", " Guessing Game!"], [(255, 0, 0), (0, 0, 139)], width // 2 - 390, 250)

        # Render the buttons
        start_button = Button("Start Game", width // 2 - 190, 400, font)
        rules_button = Button("Game Rules", width // 2 - 175, 500, font)
        exit_button = Button("Exit Game", width // 2 - 160, 600, font)

        # Draw the buttons
        start_button.draw(screen)
        rules_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:  # Check mouse movement
                pos = pygame.mouse.get_pos()
                if start_button.is_hovered(pos):
                    # Optional: Change the button color or appearance to indicate hover
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(pos):
                        return  # Proceed to difficulty selection
                    elif rules_button.is_clicked(pos):
                        game_rules_screen()  # Go to game rules screen
                    elif exit_button.is_clicked(pos):
                        pygame.quit()
                        sys.exit()  # Exit the game

# Difficulty selection screen
def difficulty_selection():
    # Create a larger font for the title
    title_font = pygame.font.Font(font_path, 48)  # Adjust the size as needed
    
    easy_button = Button("Easy Mode", width // 2 - 140, height // 2 - 100, font)  # Centered vertically and horizontally
    hard_button = Button("Hard Mode", width // 2 - 140, height // 2, font)  # Adjusted to be below the Easy button
    back_button = Button("Back", width // 2 - 40, height - 150, font)

    while True:
        screen.fill((128, 0, 128))  # Purple background

        # Title text
        title_text = title_font.render("Select your Difficulty:", True, (0, 0, 139))  # Red color for title
        title_rect = title_text.get_rect(center=(width // 2 + 30, 200))  # Center the title
        screen.blit(title_text, title_rect)

        # Draw buttons
        easy_button.draw(screen)
        hard_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if easy_button.is_clicked(pos):
                        return 'easy'  # Return 'easy' mode
                    elif hard_button.is_clicked(pos):
                        return 'hard'  # Return 'hard' mode
                    elif back_button.is_clicked(pos):
                        # Reset game state to return to the main menu
                        return None  # Indicate that we want to go back to the main menu

# Generation selection screen
def generation_selection():
    generation_buttons = []
    button_width = 200
    button_height = 50
    column_spacing = 300  # Increased column spacing
    row_spacing = 70  # Row spacing
    start_x = (width - (button_width * 2 + column_spacing)) // 2 - 50 # Center horizontally
    start_y = 200  # Starting Y position for the first button (moved down a bit)

    # Create buttons for generations 1 to 9
    for i in range(1, 10):
        if i % 2 == 1:  # Odd index for column 1
            button = Button(
                f"Generation {i}",
                start_x,
                start_y + (i // 2) * (button_height + row_spacing),  # Row position
                font
            )
        else:  # Even index for column 2
            button = Button(
                f"Generation {i}",
                start_x + button_width + column_spacing,  # Shift to the right for column 2
                start_y + ((i - 1) // 2) * (button_height + row_spacing),  # Row position
                font
            )
        generation_buttons.append(button)

    # Create the All Generations button
    all_button = Button(
        "All Generations",
        start_x + button_width + column_spacing,
        start_y + 4 * (button_height + row_spacing),  # Position it in column 2
        font
    )
    generation_buttons.append(all_button)

    # Create Back button
    back_button = Button("Back", width // 2 - 40, height - 150, font)  # Position in the bottom

    while True:
        screen.fill((128, 0, 128))  # Purple background

        # Draw title
        title_text = font.render("Select Your Generation:", True,(0, 0, 139))
        title_rect = title_text.get_rect(center=(width // 2 + 40, 110))  # Center the title
        screen.blit(title_text, title_rect)

        # Draw generation buttons
        for button in generation_buttons:
            button.draw(screen)

        # Draw Back button
        back_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    for i, button in enumerate(generation_buttons):
                        if button.is_clicked(pos):
                            if i == 9:  # "All Generations" button
                                return "ALL"
                            else:
                                return i + 1  # Return generation 1-9
                    if back_button.is_clicked(pos):  # Check if Back button is clicked
                        return None  # Go back to difficulty selection

# Function to display the end game screen
def display_end_game(selected_pokemon, elapsed_time, win):
    screen.fill((128, 0, 128))  # Purple background
    pokemon_name = selected_pokemon[1]
    pokedex_number = selected_pokemon[0]
    type1 = selected_pokemon[3]
    type2 = selected_pokemon[4] if selected_pokemon[4] else 'None'
    
    if win:
        message = f"Congratulations! You guessed {pokemon_name} correctly!"
    else:
        message = f"You lost! The Pokémon was {pokemon_name}."

    end_text = font.render(message, True, (255, 255, 255))
    time_text = font.render(f"Time taken: {elapsed_time}", True, (255, 255, 255))
    screen.blit(end_text, (50, 100))
    screen.blit(time_text, (50, 200))
    
    pygame.display.flip()
    time.sleep(5)  # Display for 5 seconds

def provide_hint(selected_pokemon, wrong_guesses, revealed_indices, mode, hints_given):
    pokemon_name = selected_pokemon[1]
    type_hint = selected_pokemon[3]  # Pokémon's type
    pokedex_number_hint = selected_pokemon[0]  # Pokémon's Pokédex number

    if mode == 'easy':
        # Reveal Pokémon's type after 3 wrong guesses
        if wrong_guesses >= 3 and 'type' not in hints_given:
            hints_given.append('type')
            return "Type: " + type_hint, revealed_indices

        # Reveal Pokédex number after 5 wrong guesses
        elif wrong_guesses >= 5 and 'pokedex' not in hints_given:
            hints_given.append('pokedex')
            return "Pokedex Number: " + str(pokedex_number_hint), revealed_indices

        # Reveal one letter every 2 wrong guesses starting after 7 wrong guesses
        elif wrong_guesses >= 7 and wrong_guesses % 2 == 0 and len(revealed_indices) < len(pokemon_name):
            for i in range(len(pokemon_name)):
                if i not in revealed_indices:
                    revealed_indices.append(i)
                    return None, revealed_indices  # No text hint, just reveal the letter

    elif mode == 'hard':
        # Reveal Pokémon's type after 3 wrong guesses
        if wrong_guesses >= 3 and 'type' not in hints_given:
            hints_given.append('type')
            return "Type: " + type_hint, revealed_indices

        # Reveal Pokédex number after 7 wrong guesses
        elif wrong_guesses >= 7 and 'pokedex' not in hints_given:
            hints_given.append('pokedex')
            return "Pokedex Number: " + str(pokedex_number_hint), revealed_indices

        # Reveal one letter every 5 wrong guesses starting after 10 wrong guesses
        elif wrong_guesses >= 10 and wrong_guesses % 5 == 0 and len(revealed_indices) < len(pokemon_name):
            for i in range(len(pokemon_name)):
                if i not in revealed_indices:
                    revealed_indices.append(i)
                    return None, revealed_indices  # No text hint, just reveal the letter

    return None, revealed_indices

# Game loop
def game_loop():
    global running  # This tells Python to use the global variable
    while running:
        print("Game loop is running")  # Debugging print

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # This will properly exit the loop

        background.update()  # Ensure this is being called
        background.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    while True:  # Outer loop to allow restarting the game
        background.update()  # Update the frame of the background
        background.draw(screen)  # Draw the current background frame

        # Continue with other game rendering (text, buttons, etc.)
        
        main_menu()  # Show the main menu

        pygame.display.update()  # Make sure the display is updated

        while True:
            mode = difficulty_selection()
            if mode is None:
                break  # Go back to main menu if 'Back' is clicked in difficulty selection

            while True:
                exit_game = False  # Initialize exit_game before the generation selection loop
                generation_choice = generation_selection()
                if generation_choice is None:
                    break  # Go back to difficulty selection if 'Back' is clicked in generation selection

                selected_pokemon = get_random_pokemon(generation_choice)

                if selected_pokemon:
                    pokemon_name = selected_pokemon[1]
                    wrong_guesses = 0
                    revealed_indices = []
                    hints_given = []
                    user_input = ''
                    hint_display = []  # Store hints persistently

                    # Extract hints for display
                    type_hint = selected_pokemon[3]  # Pokémon's type
                    pokedex_number_hint = selected_pokemon[0]  # Pokémon's Pokédex number

                    # Timer setup
                    if mode == 'easy':
                        start_time = start_timer()  # Timer counting up
                        countdown = None  # No countdown for easy mode
                    elif mode == 'hard':
                        start_time = time.time()  # Get the current time
                        countdown = 300  # 5-minute countdown for hard mode

                    while True:
                        # Handle timers for both modes
                        if mode == 'easy':
                            elapsed_time = get_elapsed_time(start_time)
                        else:
                            elapsed_time = countdown - (time.time() - start_time)
                            if elapsed_time <= 0:
                                display_end_game(selected_pokemon, "00:00", False)
                                break  # Time ran out, player loses

                        # Timer display formatting
                        if mode == 'easy':
                            timer_display = font.render(f'Timer: {elapsed_time}', True, (255, 255, 255))
                        else:
                            minutes, seconds = divmod(max(0, int(elapsed_time)), 60)
                            timer_display = font.render(f'Timer: {minutes:02}:{seconds:02}', True, (255, 255, 255))

                        # Game logic (rendering, input, etc.)
                        hidden_name_display = font.render(display_hidden_name(pokemon_name, revealed_indices), True, (255, 255, 255))

                        # Replace title_text logic with the multicolor rendering
                        screen.fill((128, 0, 128))  # Purple background

                        # Call the render_multicolor_text function to display the title with "Pokemon" in red and "Guessing Game!" in deep blue
                        render_multicolor_text(screen, font, ["Pokemon", " Guessing Game!"], [(255, 0, 0), (0, 0, 139)], width // 2 - 420, 180)

                        # Render other elements on the screen
                        screen.blit(hidden_name_display, (width // 2 - 230, 400))
                        screen.blit(timer_display, (width // 2 - 230, 500))

                        # Display the user's current guess
                        input_text = font.render(f'Your Guess: {user_input}', True, (255, 255, 255))
                        screen.blit(input_text, (width // 2 - 400, 300))

                        # Exit Game button
                        exit_button = Button("Exit Game", width // 2 - 200, height - 150, font)
                        exit_button.draw(screen)

                        # Display type hint
                        if 'type' in hints_given:
                            type_hint_text = font.render(f"Type: {type_hint}", True, (255, 255, 255))
                            screen.blit(type_hint_text, (width // 2 - 230, 600))  # Type hint position

                        # Display Pokédex number hint with increased spacing
                        if 'pokedex' in hints_given:
                            pokedex_hint_text = font.render(f"Pokedex Number: {pokedex_number_hint}", True, (255, 255, 255))
                            screen.blit(pokedex_hint_text, (width // 2 - 230, 700))  # Increased spacing for Pokédex number

                        pygame.display.flip()

                        # Handle events
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:  # Check guess on Enter key
                                    if user_input.lower() == pokemon_name.lower():
                                        display_end_game(selected_pokemon, elapsed_time, True)
                                        break
                                    else:
                                        wrong_guesses += 1
                                        new_hint, revealed_indices = provide_hint(selected_pokemon, wrong_guesses, revealed_indices, mode, hints_given)
                                        if new_hint:  # If a new hint was provided, add it to hint_display
                                            hint_display.append(new_hint)
                                        user_input = ''  # Reset input after guess

                                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                                    user_input = user_input[:-1]

                                else:
                                    user_input += event.unicode  # Append character to input
                            
                            # Check if Exit Game button is clicked
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:  # Left mouse button
                                    pos = pygame.mouse.get_pos()
                                    if exit_button.is_clicked(pos):
                                        exit_game = True  # Set flag to indicate exit is requested

                        # Check if exit game was requested
                        if exit_game:
                            break  # Exit the guessing game loop and return to main menu

                        # Check if the game should end
                        if len(revealed_indices) == len(pokemon_name):  # All letters revealed
                            display_end_game(selected_pokemon, elapsed_time, False)
                            break

                    # This should be outside the guessing game loop
                    if exit_game:
                        break  # Exit the generation selection screen
            if exit_game:
                break  # Exit the difficulty selection screen

# Start the game
game_loop()

pygame.quit() # Quit Pygame when the game loop ends