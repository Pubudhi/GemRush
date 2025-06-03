import pygame
import random
import math
import os
import sys
import time

# Import our improved modules
from improved_player import ImprovedPlayer
from improved_gems import ImprovedGem
from improved_background import ParallaxBackground
from improved_effects import ParticleSystem, LightEffect, ScreenTransition
from improved_ui import ImprovedUI
from game_timer import GameTimer
from leaderboard import Leaderboard

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GemRush")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Create directories for assets if they don't exist
os.makedirs("assets", exist_ok=True)
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/sounds", exist_ok=True)

# Load fonts
font_large = pygame.font.SysFont(None, 64)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

# Show loading screen
def show_loading_screen():
    loading_duration = 3  # seconds
    start_time = time.time()
    
    # Create background
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 20, 30))  # Dark blue background
    
    # Create title text
    title_text = font_large.render("GemRush", True, (255, 215, 0))  # Gold color
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    
    # Loading bar parameters
    bar_width = 400
    bar_height = 30
    bar_border = 3
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT // 2 + 50
    
    while time.time() - start_time < loading_duration:
        # Calculate progress (0 to 1)
        progress = min(1.0, (time.time() - start_time) / loading_duration)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Draw background
        screen.blit(background, (0, 0))
        
        # Draw title
        screen.blit(title_text, title_rect)
        
        # Draw loading text
        loading_text = font_medium.render("Loading...", True, (255, 255, 255))
        loading_rect = loading_text.get_rect(center=(WIDTH // 2, bar_y - 30))
        screen.blit(loading_text, loading_rect)
        
        # Draw loading bar border
        pygame.draw.rect(screen, (150, 150, 150), 
                        (bar_x - bar_border, bar_y - bar_border, 
                         bar_width + bar_border * 2, bar_height + bar_border * 2), 
                        border_radius=5)
        
        # Draw loading bar background
        pygame.draw.rect(screen, (50, 50, 50), 
                        (bar_x, bar_y, bar_width, bar_height), 
                        border_radius=5)
        
        # Draw loading bar fill
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            # Gradient color from red to green based on progress
            r = int(255 * (1 - progress))
            g = int(255 * progress)
            b = 50
            pygame.draw.rect(screen, (r, g, b), 
                            (bar_x, bar_y, fill_width, bar_height), 
                            border_radius=5)
        
        # Draw percentage text
        percent_text = font_small.render(f"{int(progress * 100)}%", True, (255, 255, 255))
        percent_rect = percent_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        screen.blit(percent_text, percent_rect)
        
        # Draw tips
        tips = [
            "Collect diamonds for maximum points!",
            "Each gem type gives different time bonuses",
            "Press L to view the leaderboard after a game",
            "Complete all three levels to win",
            "Watch the timer - it changes color when time is low"
        ]
        tip_index = int(progress * len(tips))
        if tip_index < len(tips):
            tip_text = font_small.render(f"Tip: {tips[tip_index]}", True, (200, 200, 200))
            tip_rect = tip_text.get_rect(center=(WIDTH // 2, bar_y + 70))
            screen.blit(tip_text, tip_rect)
        
        pygame.display.flip()
        clock.tick(60)

# Show loading screen
show_loading_screen()

# Game variables
score = 0
level = 1
gems_collected = 0
gems_required = 10
game_active = True
game_over = False
victory = False
high_score = 0
game_start_time = time.time()
total_time_played = 0
show_leaderboard = False

# Try to load high score
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# Create leaderboard
leaderboard = Leaderboard()

# Create sprite groups
all_sprites = pygame.sprite.Group()
gems = pygame.sprite.Group()
particles = pygame.sprite.Group()

# Create player
player = ImprovedPlayer()
all_sprites.add(player)

# Create background
background = ParallaxBackground(WIDTH, HEIGHT)
# Set day cycle speed - adjust this to control how fast day/night changes
background.day_cycle_speed = 0.0001  # Slower cycle for better atmosphere

# Create effects
particle_system = ParticleSystem()
light_effect = LightEffect(WIDTH, HEIGHT)
screen_transition = ScreenTransition(WIDTH, HEIGHT)

# Create UI
ui = ImprovedUI(WIDTH, HEIGHT)

# Create timer
level_times = [60, 50, 40]  # Time in seconds for each level
game_timer = GameTimer(level_times[level-1], 20, 10)

# Set timer callbacks
def on_timer_warning():
    print("Timer warning!")
    # Play warning sound
    # pygame.mixer.Sound("assets/sounds/timer_warning.wav").play()

def on_timer_critical():
    print("Timer critical!")
    # Play critical sound
    # pygame.mixer.Sound("assets/sounds/timer_critical.wav").play()

def on_timer_timeout():
    global game_active, game_over, total_time_played
    print("Time's up!")
    game_active = False
    game_over = True
    total_time_played = time.time() - game_start_time
    # Play game over sound
    # pygame.mixer.Sound("assets/sounds/game_over.wav").play()

game_timer.on_warning = on_timer_warning
game_timer.on_critical = on_timer_critical
game_timer.on_timeout = on_timer_timeout

# Create initial gems
def create_gems(count):
    for i in range(count):
        gem = ImprovedGem()
        all_sprites.add(gem)
        gems.add(gem)
        
        # Add light for each gem
        light_effect.add_light(gem.rect.centerx, gem.rect.centery, 50, gem.color, 0.3)

create_gems(gems_required)

# Function to reset the level
def reset_level():
    global gems_collected, level, gems_required
    
    # Clear existing gems and lights
    for gem in gems:
        gem.kill()
    light_effect.clear_lights()
    
    # Reset variables
    gems_collected = 0
    level += 1
    gems_required = 10 + (level - 1) * 5  # Increase required gems each level
    
    # Reset timer with new level time
    if level <= len(level_times):
        game_timer.reset(level_times[level-1])
    else:
        game_timer.reset(30)  # Default time if we run out of predefined times
    
    # Create new gems
    create_gems(gems_required)
    
    # Reset player position
    player.rect.center = (WIDTH // 2, HEIGHT // 2)
    
    # Start transition
    screen_transition.start('fade', 'out', 0.02)

# Function to restart the game
def restart_game():
    global score, level, gems_collected, gems_required, game_active, game_over, victory, game_start_time, total_time_played, show_leaderboard
    
    # Reset game
    game_over = False
    victory = False
    game_active = True
    score = 0
    level = 1
    gems_collected = 0
    gems_required = 10
    game_start_time = time.time()
    total_time_played = 0
    show_leaderboard = False
    
    # Reset timer
    game_timer.reset(level_times[level-1])
    
    # Clear all sprites
    for sprite in all_sprites:
        sprite.kill()
    light_effect.clear_lights()
    
    # Create player
    player = ImprovedPlayer()
    all_sprites.add(player)
    
    # Create initial gems
    create_gems(gems_required)
    
    # Start transition
    screen_transition.start('fade', 'out', 0.02)

# Game loop
running = True
while running:
    # Keep the loop running at the right speed
    dt = clock.tick(FPS) / 1000.0
    
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
            # Restart game if it's over
            if (game_over or victory) and event.key == pygame.K_r:
                restart_game()
                
            # Show/hide leaderboard
            if (game_over or victory) and event.key == pygame.K_l:
                show_leaderboard = not show_leaderboard
                
        # Handle mouse clicks for exit button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if victory and not show_leaderboard:
                    # Check if exit button was clicked
                    exit_button_width = 180  # Updated to match UI change
                    exit_button_height = 50  # Updated to match UI change
                    exit_button_x = WIDTH // 2 - exit_button_width // 2
                    exit_button_y = HEIGHT // 2 + 220
                    exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, exit_button_width, exit_button_height)
                    
                    if exit_button_rect.collidepoint(event.pos):
                        running = False
    
    # Get mouse position for UI
    mouse_pos = pygame.mouse.get_pos()
    ui.check_button_hover(mouse_pos)
    
    # Update
    if game_active and not game_over and not victory:
        # Update timer
        game_timer.update(dt)
        
        # Update player
        player.update()
        
        # Update gems
        gems.update()
        
        # Update lights to follow gems
        for i, gem in enumerate(gems):
            if i < len(light_effect.lights):
                light_effect.update_light(i, gem.rect.centerx, gem.rect.centery)
        
        # Create trail particles behind player
        if random.random() < 0.2:
            particle_system.create_trail_effect(
                player.rect.centerx + random.uniform(-10, 10),
                player.rect.centery + random.uniform(-10, 10),
                (50, 100, 255)
            )
        
        # Create sparkle effects on gems
        for gem in gems:
            if random.random() < 0.05:
                particle_system.create_sparkle_effect(
                    gem.rect.centerx,
                    gem.rect.centery,
                    gem.color
                )
        
        # Check for collisions between player and gems
        gem_collisions = pygame.sprite.spritecollide(player, gems, True)
        for gem in gem_collisions:
            # Increase score based on gem type
            gem_value = gem.value
            score += gem_value
            gems_collected += 1
            
            # Add time bonus based on gem type
            time_bonus = 0
            if gem.gem_type == "diamond":
                time_bonus = 5
            elif gem.gem_type == "ruby":
                time_bonus = 4
            elif gem.gem_type == "emerald":
                time_bonus = 3
            elif gem.gem_type == "sapphire":
                time_bonus = 2
            else:  # topaz
                time_bonus = 1
                
            game_timer.add_time(time_bonus)
            
            # Create particle effect
            particle_system.create_collection_effect(
                gem.rect.centerx,
                gem.rect.centery,
                gem.color,
                30
            )
            
            # Remove the gem's light - fixed to avoid index error
            # Find the light index by position instead of sprite index
            for i, light in enumerate(light_effect.lights):
                if abs(light['pos'][0] - gem.rect.centerx) < 10 and abs(light['pos'][1] - gem.rect.centery) < 10:
                    light_effect.remove_light(i)
                    break
            
            # Play sound effect (placeholder)
            # pygame.mixer.Sound("assets/sounds/collect.wav").play()
            
            print(f"Collected {gem.gem_type}! Score: {score}, Gems: {gems_collected}/{gems_required}")
        
        # Check if level is complete
        if gems_collected >= gems_required:
            if level < 3:  # 3 levels total
                reset_level()
            else:
                victory = True
                game_active = False
                total_time_played = time.time() - game_start_time
                
                # Add to leaderboard
                leaderboard.add_entry(score, total_time_played, level)
                
                # Update high score
                if score > high_score:
                    high_score = score
                    try:
                        with open("high_score.txt", "w") as f:
                            f.write(str(high_score))
                    except:
                        pass
        
        # Update background based on player movement
        player_movement = [player.direction.x * player.speed * 0.1, 
                          player.direction.y * player.speed * 0.1]
        background.update(player_movement)
    
    # Update particles
    particle_system.update()
    
    # Update UI
    ui.update(dt)
    
    # Update screen transition
    screen_transition.update()
    
    # Draw / render
    # Draw background
    background.draw(screen)
    
    # Draw all sprites
    all_sprites.draw(screen)
    
    # Draw particles
    particle_system.draw(screen)
    
    # Draw lights
    light_surface = light_effect.render()
    screen.blit(light_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    
    # Draw UI
    ui.draw_score_display(screen, 20, 20, score)
    ui.draw_gem_counter(screen, WIDTH // 2 - 50, 20, gems_collected, gems_required)
    ui.draw_level_indicator(screen, WIDTH - 100, 20, level, 3)
    
    # Draw timer
    if game_active and not game_over and not victory:
        game_timer.draw(screen, 250, 60, 300, 20, True, ui.small_font)
    
    # Draw game over screen
    if game_over:
        if not show_leaderboard:
            ui.draw_game_over_screen(screen, score, high_score)
            
            # Draw additional instructions - moved lower
            instructions = ui.small_font.render("Press L to view leaderboard", True, (255, 255, 255))
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 + 200))
        else:
            # Draw leaderboard
            leaderboard.draw(screen, WIDTH // 2 - 350, HEIGHT // 2 - 250, 700, 500, ui.title_font, ui.medium_font, ui.small_font)
            
            # Draw back button instruction
            back_text = ui.small_font.render("Press L to return", True, (255, 255, 255))
            screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 50))
    
    # Draw victory screen
    if victory:
        if not show_leaderboard:
            ui.draw_victory_screen(screen, score, high_score)
            
            # Draw time played
            minutes = int(total_time_played) // 60
            seconds = int(total_time_played) % 60
            time_text = ui.medium_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
            screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + 90))
            
            # Draw additional instructions - moved lower
            instructions = ui.small_font.render("Press L to view leaderboard", True, (255, 255, 255))
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 + 200))
            
            # Check for exit button click
            exit_button_width = 180  # Updated to match UI change
            exit_button_height = 50  # Updated to match UI change
            exit_button_x = WIDTH // 2 - exit_button_width // 2
            exit_button_y = HEIGHT // 2 + 220
            exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, exit_button_width, exit_button_height)
            
            # Check if mouse is over exit button
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            if exit_button_rect.collidepoint(mouse_pos):
                if mouse_clicked:
                    running = False
        else:
            # Draw leaderboard
            leaderboard.draw(screen, WIDTH // 2 - 350, HEIGHT // 2 - 250, 700, 500, ui.title_font, ui.medium_font, ui.small_font)
            
            # Draw back button instruction
            back_text = ui.small_font.render("Press L to return", True, (255, 255, 255))
            screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 50))
    
    # Draw transition effect
    if screen_transition.active:
        transition_surface = screen_transition.render()
        if transition_surface:
            screen.blit(transition_surface, (0, 0))
    
    # Flip the display
    pygame.display.flip()

# Save high score before quitting
if score > high_score:
    try:
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))
    except:
        pass

# Quit the game
pygame.quit()
sys.exit()
