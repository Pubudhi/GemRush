import pygame
import math
import random

# Improved Gem class with better graphics and animations
class ImprovedGem(pygame.sprite.Sprite):
    def __init__(self, gem_type=None, x=None, y=None):
        super().__init__()
        
        # Gem types and colors
        self.gem_types = ["diamond", "ruby", "emerald", "sapphire", "topaz"]
        self.colors = {
            "diamond": (200, 255, 255),  # Cyan
            "ruby": (255, 50, 50),       # Red
            "emerald": (50, 255, 80),    # Green
            "sapphire": (50, 100, 255),  # Blue
            "topaz": (255, 255, 50)      # Yellow
        }
        self.glow_colors = {
            "diamond": (220, 255, 255),  # Lighter cyan
            "ruby": (255, 150, 150),     # Lighter red
            "emerald": (150, 255, 150),  # Lighter green
            "sapphire": (150, 200, 255), # Lighter blue
            "topaz": (255, 255, 150)     # Lighter yellow
        }
        
        # Select gem type
        if gem_type is None:
            self.gem_type = random.choice(self.gem_types)
        else:
            self.gem_type = gem_type
            
        self.color = self.colors[self.gem_type]
        self.glow_color = self.glow_colors[self.gem_type]
        
        # Create animation frames
        self.frames = []
        self.create_animation_frames()
        
        # Animation variables
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        
        # Set initial image and position
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
        # Position the gem
        if x is None or y is None:
            self.rect.x = random.randint(50, 750)  # Assuming screen width is 800
            self.rect.y = random.randint(50, 550)  # Assuming screen height is 600
        else:
            self.rect.x = x
            self.rect.y = y
            
        # Store original position for bobbing animation
        self.original_y = self.rect.y
        self.bob_offset = random.uniform(0, 2 * math.pi)  # Random start phase
        self.bob_speed = random.uniform(0.05, 0.1)
        self.bob_height = random.uniform(3, 6)
        
        # Value of the gem
        self.value = self.get_value()
        
    def create_animation_frames(self):
        # Create frames for gem animation (rotation effect)
        num_frames = 8
        
        for i in range(num_frames):
            # Calculate rotation factor (0 to 1)
            rotation = i / num_frames
            
            # Create frame
            frame = pygame.Surface((40, 40), pygame.SRCALPHA)
            
            # Draw gem based on type and rotation
            if self.gem_type == "diamond":
                self.draw_diamond(frame, rotation)
            elif self.gem_type == "ruby":
                self.draw_ruby(frame, rotation)
            elif self.gem_type == "emerald":
                self.draw_emerald(frame, rotation)
            elif self.gem_type == "sapphire":
                self.draw_sapphire(frame, rotation)
            else:  # topaz
                self.draw_topaz(frame, rotation)
                
            self.frames.append(frame)
    
    def draw_diamond(self, surface, rotation):
        # Diamond shape (rhombus) with random variations
        width = 30 - abs(rotation - 0.5) * 20  # Simulate rotation by changing width
        height = 30
        
        # Random variation in shape
        skew = random.uniform(-0.2, 0.2)
        stretch = random.uniform(0.8, 1.2)
        height *= stretch
        
        # Draw main shape
        points = [
            (20 - width/2, 20 - height/2),  # Top
            (20 + width/2, 20 + height/2 * skew),  # Right
            (20, 20 + height/2),            # Bottom
            (20 - width/2, 20 + height/2 * -skew),  # Left
        ]
        
        # Draw glow
        pygame.draw.polygon(surface, self.glow_color, points)
        
        # Draw gem with slightly different points for 3D effect
        inner_points = [
            (20, 5 + random.uniform(-2, 2)),                # Top
            (35 - rotation * 10, 20 + random.uniform(-2, 2)),  # Right
            (20, 35 + random.uniform(-2, 2)),               # Bottom
            (5 + rotation * 10, 20 + random.uniform(-2, 2)),   # Left
        ]
        pygame.draw.polygon(surface, self.color, inner_points)
        
        # Draw facets
        pygame.draw.line(surface, (255, 255, 255, 150), inner_points[0], inner_points[2], 1)
        pygame.draw.line(surface, (255, 255, 255, 150), inner_points[1], inner_points[3], 1)
        
        # Draw sparkle
        if rotation < 0.2 or rotation > 0.8:
            self.draw_sparkle(surface)
    
    def draw_ruby(self, surface, rotation):
        # Ruby shape (circle/oval) with random variations
        width = 30 - abs(rotation - 0.5) * 10
        height = 30
        
        # Random variation
        stretch = random.uniform(0.8, 1.2)
        squish = random.uniform(0.8, 1.2)
        width *= stretch
        height *= squish
        
        # Draw glow
        pygame.draw.ellipse(surface, self.glow_color, (20 - width/2, 20 - height/2, width, height))
        
        # Draw gem
        pygame.draw.ellipse(surface, self.color, (20 - width/2 + 2, 20 - height/2 + 2, width - 4, height - 4))
        
        # Draw facets
        angle = rotation * 2 * math.pi
        end_x = 20 + math.cos(angle) * width/2 * 0.8
        end_y = 20 + math.sin(angle) * height/2 * 0.8
        pygame.draw.line(surface, (255, 255, 255, 150), (20, 20), (end_x, end_y), 1)
        pygame.draw.line(surface, (255, 255, 255, 150), (20, 20), (2*20 - end_x, 2*20 - end_y), 1)
        
        # Draw sparkle
        if rotation < 0.2 or rotation > 0.8:
            self.draw_sparkle(surface)
    
    def draw_emerald(self, surface, rotation):
        # Emerald shape (rectangle) with random variations
        width = 30 - abs(rotation - 0.5) * 20
        height = 24
        
        # Random variation
        skew = random.uniform(-0.15, 0.15)
        stretch = random.uniform(0.9, 1.1)
        width *= stretch
        
        # Calculate skewed rectangle points
        points = [
            (20 - width/2, 20 - height/2),  # Top-left
            (20 + width/2, 20 - height/2 + height * skew),  # Top-right
            (20 + width/2, 20 + height/2 + height * skew),  # Bottom-right
            (20 - width/2, 20 + height/2),  # Bottom-left
        ]
        
        # Draw glow
        pygame.draw.polygon(surface, self.glow_color, points)
        
        # Draw gem (slightly smaller)
        inner_points = []
        for x, y in points:
            inner_points.append((x + (20 - x) * 0.1, y + (20 - y) * 0.1))
        
        pygame.draw.polygon(surface, self.color, inner_points)
        
        # Draw facets - fixed to use correct number of arguments
        mid_top = ((inner_points[0][0] + inner_points[1][0]) / 2, (inner_points[0][1] + inner_points[1][1]) / 2)
        mid_bottom = ((inner_points[2][0] + inner_points[3][0]) / 2, (inner_points[2][1] + inner_points[3][1]) / 2)
        pygame.draw.line(surface, (255, 255, 255, 150), mid_top, mid_bottom, 1)
        
        # Draw sparkle
        if rotation < 0.2 or rotation > 0.8:
            self.draw_sparkle(surface)
    
    def draw_sapphire(self, surface, rotation):
        # Sapphire shape (hexagon) with random variations
        radius = 15 - abs(rotation - 0.5) * 5
        points = []
        
        # Random variation
        stretch = random.uniform(0.9, 1.1)
        radius *= stretch
        offset_x = random.uniform(-2, 2)
        offset_y = random.uniform(-2, 2)
        
        for i in range(6):
            angle = 2 * math.pi * i / 6 + rotation * math.pi / 3
            x = 20 + offset_x + radius * math.cos(angle) * (1 + random.uniform(-0.1, 0.1))
            y = 20 + offset_y + radius * math.sin(angle) * (1 + random.uniform(-0.1, 0.1))
            points.append((x, y))
        
        # Draw glow
        pygame.draw.polygon(surface, self.glow_color, points)
        
        # Draw gem (slightly smaller)
        inner_points = []
        inner_radius = radius - 2
        for i in range(6):
            angle = 2 * math.pi * i / 6 + rotation * math.pi / 3
            x = 20 + offset_x + inner_radius * math.cos(angle) * (1 + random.uniform(-0.05, 0.05))
            y = 20 + offset_y + inner_radius * math.sin(angle) * (1 + random.uniform(-0.05, 0.05))
            inner_points.append((x, y))
        
        pygame.draw.polygon(surface, self.color, inner_points)
        
        # Draw facets
        pygame.draw.line(surface, (255, 255, 255, 150), inner_points[0], inner_points[3], 1)
        pygame.draw.line(surface, (255, 255, 255, 150), inner_points[1], inner_points[4], 1)
        
        # Draw sparkle
        if rotation < 0.2 or rotation > 0.8:
            self.draw_sparkle(surface)
    
    def draw_topaz(self, surface, rotation):
        # Topaz shape (octagon) with random variations
        radius = 15 - abs(rotation - 0.5) * 5
        points = []
        
        # Random variation
        stretch_x = random.uniform(0.9, 1.1)
        stretch_y = random.uniform(0.9, 1.1)
        offset_angle = random.uniform(-0.1, 0.1)
        
        for i in range(8):
            angle = 2 * math.pi * i / 8 + rotation * math.pi / 4 + offset_angle
            x = 20 + radius * math.cos(angle) * stretch_x
            y = 20 + radius * math.sin(angle) * stretch_y
            points.append((x, y))
        
        # Draw glow
        pygame.draw.polygon(surface, self.glow_color, points)
        
        # Draw gem (slightly smaller)
        inner_points = []
        inner_radius = radius - 2
        for i in range(8):
            angle = 2 * math.pi * i / 8 + rotation * math.pi / 4 + offset_angle
            x = 20 + inner_radius * math.cos(angle) * stretch_x
            y = 20 + inner_radius * math.sin(angle) * stretch_y
            inner_points.append((x, y))
        
        pygame.draw.polygon(surface, self.color, inner_points)
        
        # Draw facets
        pygame.draw.line(surface, (255, 255, 255, 150), inner_points[0], inner_points[4], 1)
        pygame.draw.line(surface, (255, 255, 255, 150), inner_points[2], inner_points[6], 1)
        
        # Draw sparkle
        if rotation < 0.2 or rotation > 0.8:
            self.draw_sparkle(surface)
    
    def draw_sparkle(self, surface):
        # Draw sparkle effect
        pygame.draw.line(surface, (255, 255, 255), (15, 15), (25, 25), 1)
        pygame.draw.line(surface, (255, 255, 255), (25, 15), (15, 25), 1)
        pygame.draw.line(surface, (255, 255, 255), (20, 10), (20, 30), 1)
        pygame.draw.line(surface, (255, 255, 255), (10, 20), (30, 20), 1)
    
    def get_value(self):
        # Return point value based on gem type
        if self.gem_type == "diamond":
            return 10
        elif self.gem_type == "ruby":
            return 8
        elif self.gem_type == "emerald":
            return 6
        elif self.gem_type == "sapphire":
            return 5
        else:  # topaz
            return 4
    
    def update(self):
        # Update animation frame
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
        
        # Bob up and down
        self.bob_offset += self.bob_speed
        self.rect.y = self.original_y + math.sin(self.bob_offset) * self.bob_height

# Test the gem animations
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gem Animation Test")
    clock = pygame.time.Clock()
    
    # Create one of each gem type
    gems = pygame.sprite.Group()
    for i, gem_type in enumerate(["diamond", "ruby", "emerald", "sapphire", "topaz"]):
        gem = ImprovedGem(gem_type=gem_type, x=150 + i * 100, y=300)
        gems.add(gem)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        gems.update()
        
        screen.fill((20, 20, 20))
        gems.draw(screen)
        
        # Draw gem names
        font = pygame.font.SysFont(None, 24)
        for i, gem_type in enumerate(["diamond", "ruby", "emerald", "sapphire", "topaz"]):
            text = font.render(gem_type.capitalize(), True, (255, 255, 255))
            screen.blit(text, (150 + i * 100 - text.get_width() // 2, 350))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
