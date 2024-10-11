import pygame
import random
import os
import json 

def main():

  # Initialize pygame
    pygame.init()
    pygame.font.init()  # Initialize font module
    pygame.key.start_text_input()

    # Set up display
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo de advinhação da bandeira (by Dudu)")

    # Colors
    WHITE = (255, 255, 255)
    LIGHT_GREY = (211, 211, 211)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Fonts
    #font = pygame.font.Font(None, 36)
    font = pygame.font.Font("fonts/DejaVuSans.ttf", 32) 

    # Load flags
    flag_folder = "flags"  # Folder containing flag images
    flags = [f for f in os.listdir(flag_folder) if os.path.isfile(os.path.join(flag_folder, f))]
    
    # Load country names from JSON file
    with open("country_names.json", "r", encoding="utf-8") as f:
        country_name_mapping = json.load(f)

    # Extract country names from filenames (assuming filenames are in format "country.png")
    countries = [os.path.splitext(flag)[0] for flag in flags]


    # Game variables
    score = 0
    total_flags = len(flags)
    guess = ""
    remaining_flags = flags.copy()
    current_flag = random.choice(remaining_flags) if remaining_flags else None
        

    # Enable text input (supports better Unicode handling)
    pygame.key.start_text_input()
    
    # Game loop
    running = True
    while running:
        if not remaining_flags:
            # End game if no flags are left
            running = False
            continue

        screen.fill(LIGHT_GREY)

        # Display current flag
        flag_image = pygame.image.load(os.path.join(flag_folder, current_flag))
        flag_image = pygame.transform.scale(flag_image, (300, 200))
        screen.blit(flag_image, ((WIDTH - 300) // 2, 50))

        # Display score
        score_text = font.render(f"Pontuação: {score}/{total_flags}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Display user input
        guess_text = font.render(f"Sua resposta: {guess}", True, BLACK)
        screen.blit(guess_text, (10, 300))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    country_code = os.path.splitext(current_flag)[0]
                    correct_country_name = country_name_mapping.get(country_code, "Unknown Country")
                    # Check if the guess is correct
                    if guess.lower() == correct_country_name.lower():
                        score += 1
                    else:
                        # Display incorrect message and correct answer
                        incorrect_text = font.render(f"Errou! A resposta correta era: {correct_country_name}", True, RED, 32)
                        screen.blit(incorrect_text, ((WIDTH - incorrect_text.get_width()) // 2 + 10, HEIGHT // 2 + 50))
                        pygame.display.flip()
                        pygame.time.delay(2000)
                    remaining_flags.remove(current_flag)
                    if remaining_flags:
                        current_flag = random.choice(remaining_flags)
                    else:
                        running = False
                    guess = ""
                elif event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
            elif event.type == pygame.TEXTINPUT:
                # Use text input event to handle all characters correctly, including accents
                guess += event.text

        # Update the display
        pygame.display.flip()
    
    # Stop text input when done
    pygame.key.stop_text_input()    
    # Display end message
    screen.fill(LIGHT_GREY)
    end_message = font.render(f"Fim de jogo! Sua pontuação final é: {score}", True, BLACK)
    screen.blit(end_message, ((WIDTH - end_message.get_width()) // 2, HEIGHT // 2))
    pygame.display.flip()

    # Wait for a few seconds before quitting
    pygame.time.delay(3000)

    
    # Quit pygame 
    pygame.quit()


if __name__ == "__main__":
    main()
