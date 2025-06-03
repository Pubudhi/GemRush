import pygame
import os

# Initialize pygame
pygame.init()

# Create a surface for the icon
icon = pygame.Surface((128, 128), pygame.SRCALPHA)

# Draw the player character (blue circle with face)
pygame.draw.circle(icon, (50, 100, 255), (64, 64), 60)  # Blue circle
pygame.draw.circle(icon, (255, 255, 255), (64, 64), 60, 3)  # White outline

# Add eyes
pygame.draw.circle(icon, (255, 255, 255), (45, 50), 15)
pygame.draw.circle(icon, (255, 255, 255), (83, 50), 15)
pygame.draw.circle(icon, (0, 0, 0), (45, 50), 7)
pygame.draw.circle(icon, (0, 0, 0), (83, 50), 7)

# Add smile
pygame.draw.arc(icon, (255, 255, 255), (34, 50, 60, 50), 0.2, 2.9, 4)

# Ensure directory exists
os.makedirs("assets/images", exist_ok=True)

# Save the icon
pygame.image.save(icon, 'assets/images/gemrush_icon.png')

print("Icon created successfully at assets/images/gemrush_icon.png")
