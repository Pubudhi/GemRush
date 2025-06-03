import pygame
import random
import math

class Cloud:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Cloud properties
        self.x = random.randint(-200, -100)  # Start off-screen to the left
        self.y = random.randint(20, int(screen_height * 0.4))
        self.speed = random.uniform(0.05, 0.2)  # Reduced speed (was 0.2-0.8)
        
        # Cloud size and shape
        self.width = random.randint(100, 200)
        self.height = random.randint(40, 80)
        self.segments = random.randint(3, 5)
        
        # Cloud color (white with slight variations and reduced opacity)
        self.base_color = (255, 255, 255)
        self.color_variation = random.randint(-20, 0)
        self.color = (
            max(0, min(255, self.base_color[0] + self.color_variation)),
            max(0, min(255, self.base_color[1] + self.color_variation)),
            max(0, min(255, self.base_color[2] + self.color_variation))
        )
        self.opacity = random.randint(100, 180)  # Reduced opacity
        
    def update(self):
        # Move cloud
        self.x += self.speed
        
        # Reset if off-screen
        if self.x > self.screen_width + 100:
            self.x = random.randint(-200, -100)
            self.y = random.randint(20, int(self.screen_height * 0.4))
            self.speed = random.uniform(0.05, 0.2)  # Reduced speed
            self.width = random.randint(100, 200)
            self.height = random.randint(40, 80)
    
    def draw(self, surface):
        # Create a temporary surface for the cloud with alpha channel
        cloud_surface = pygame.Surface((self.width + 50, self.height + 50), pygame.SRCALPHA)
        
        # Draw cloud as a series of overlapping circles with transparency
        for i in range(self.segments):
            segment_x = 25 + (i * self.width / self.segments)
            segment_y = 25 + random.randint(-10, 10)
            segment_radius = random.randint(int(self.height * 0.6), int(self.height * 0.8))
            
            # Create color with opacity
            color_with_alpha = (*self.color, self.opacity)
            pygame.draw.circle(cloud_surface, color_with_alpha, (int(segment_x), int(segment_y)), segment_radius)
        
        # Blit the cloud surface onto the main surface
        surface.blit(cloud_surface, (int(self.x - 25), int(self.y - 25)))

class ParallaxBackground:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.SKY_COLORS = {
            'dawn': [(70, 40, 90), (120, 80, 100)],    # Purple to pink
            'day': [(100, 180, 255), (180, 220, 255)], # Blue to light blue
            'dusk': [(255, 120, 50), (70, 40, 90)],    # Orange to purple
            'night': [(10, 10, 40), (30, 30, 70)]      # Dark blue to slightly lighter blue
        }
        self.STAR_COLOR = (255, 255, 255)
        self.MOUNTAIN_COLORS = [
            (60, 40, 80),  # Far mountains (purple)
            (40, 50, 80),  # Mid mountains (blue-purple)
            (30, 60, 70)   # Near mountains (blue-green)
        ]
        self.GROUND_COLORS = [
            (20, 40, 20),  # Dark grass
            (30, 60, 30)   # Light grass
        ]
        
        # Time of day
        self.time_of_day = 0  # 0 to 1, representing a full day cycle
        self.day_cycle_speed = 0.0002  # Speed of day/night cycle
        self.current_sky_colors = self.get_sky_colors()
        
        # Stars
        self.stars = []
        self.generate_stars(100)
        
        # Create layers
        self.layers = []
        self.create_layers()
        
        # Camera position for parallax effect
        self.camera_pos = [0, 0]
    
    def generate_stars(self, count):
        for _ in range(count):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height // 2)
            size = random.uniform(0.5, 2.5)
            brightness = random.randint(100, 255)
            twinkle_speed = random.uniform(0.01, 0.05)
            twinkle_phase = random.uniform(0, 2 * math.pi)
            
            self.stars.append({
                'x': x,
                'y': y,
                'size': size,
                'brightness': brightness,
                'twinkle_speed': twinkle_speed,
                'twinkle_phase': twinkle_phase
            })
    
    def generate_clouds(self, count):
        for _ in range(count):
            self.clouds.append(Cloud(self.screen_width, self.screen_height))
        
        # Add more clouds for a fuller sky
        for _ in range(count):
            cloud = Cloud(self.screen_width, self.screen_height)
            # Position these clouds further to the right so they don't all appear at once
            cloud.x = random.randint(self.screen_width // 2, self.screen_width * 2)
            self.clouds.append(cloud)
    
    def get_sky_colors(self):
        # Determine time of day period
        if self.time_of_day < 0.25:  # Dawn: 0.0 - 0.25
            period = 'dawn'
            t = self.time_of_day / 0.25
        elif self.time_of_day < 0.75:  # Day: 0.25 - 0.75
            period = 'day'
            t = (self.time_of_day - 0.25) / 0.5
        elif self.time_of_day < 1.0:  # Dusk: 0.75 - 1.0
            period = 'dusk'
            t = (self.time_of_day - 0.75) / 0.25
        else:  # Night: 1.0 (wraps to 0.0)
            period = 'night'
            t = 0
        
        return {
            'period': period,
            'colors': self.SKY_COLORS[period],
            'blend': t
        }
        
    def create_layers(self):
        # Sky layer (will be updated dynamically)
        sky_layer = self.create_sky_layer()
        self.layers.append({"surface": sky_layer, "speed": 0.0, "pos": [0, 0]})
        
        # Far mountains layer
        mountains_far = self.create_mountain_layer(0, 0.1)
        self.layers.append({"surface": mountains_far, "speed": 0.1, "pos": [0, 0]})
        
        # Mid mountains layer
        mountains_mid = self.create_mountain_layer(1, 0.2)
        self.layers.append({"surface": mountains_mid, "speed": 0.3, "pos": [0, 0]})
        
        # Near mountains layer
        mountains_near = self.create_mountain_layer(2, 0.3)
        self.layers.append({"surface": mountains_near, "speed": 0.5, "pos": [0, 0]})
        
        # Ground layer
        ground_layer = self.create_ground_layer()
        self.layers.append({"surface": ground_layer, "speed": 1.0, "pos": [0, 0]})
    
    def create_sky_layer(self):
        # Create a sky layer with gradient based on time of day
        layer = pygame.Surface((self.screen_width, self.screen_height))
        
        # Get current sky colors
        sky_info = self.current_sky_colors
        top_color = sky_info['colors'][0]
        bottom_color = sky_info['colors'][1]
        blend = sky_info['blend']
        
        # Draw gradient
        for y in range(self.screen_height):
            # Calculate color at this height
            t = y / self.screen_height
            r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
            g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
            b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
            color = (r, g, b)
            
            # Draw horizontal line with this color
            pygame.draw.line(layer, color, (0, y), (self.screen_width, y))
        
        return layer
    
    def create_mountain_layer(self, color_index, height_factor):
        # Create a layer with mountains
        layer_width = self.screen_width * 2  # Make wider for scrolling
        layer_height = self.screen_height
        layer = pygame.Surface((layer_width, layer_height), pygame.SRCALPHA)
        
        # Generate mountain points
        num_points = 20
        points = []
        for i in range(num_points + 1):
            x = i * (layer_width / num_points)
            # Height varies based on position with some randomness
            height = self.screen_height * (0.3 + height_factor * math.sin(i * 0.5) + random.uniform(0, 0.2))
            y = self.screen_height - height
            points.append((x, y))
        
        # Add bottom corners to close the polygon
        points.append((layer_width, layer_height))
        points.append((0, layer_height))
        
        # Draw mountains
        pygame.draw.polygon(layer, self.MOUNTAIN_COLORS[color_index], points)
        
        # Add some variation/detail
        for _ in range(10):
            x1 = random.randint(0, layer_width)
            y1 = random.randint(int(self.screen_height * 0.5), layer_height)
            width = random.randint(50, 200)
            height = random.randint(20, 100)
            
            # Slightly lighter color for highlights
            highlight_color = tuple(min(c + 20, 255) for c in self.MOUNTAIN_COLORS[color_index])
            
            pygame.draw.ellipse(layer, highlight_color, (x1, y1, width, height))
        
        return layer
    
    def create_ground_layer(self):
        # Create a ground layer with grass pattern
        layer_width = self.screen_width * 2  # Make wider for scrolling
        layer_height = self.screen_height
        layer = pygame.Surface((layer_width, layer_height), pygame.SRCALPHA)
        
        # Fill with base color
        layer.fill(self.GROUND_COLORS[0])
        
        # Add grass patches
        for _ in range(200):
            x = random.randint(0, layer_width)
            y = random.randint(int(self.screen_height * 0.7), layer_height)
            size = random.randint(10, 50)
            
            pygame.draw.circle(layer, self.GROUND_COLORS[1], (x, y), size)
        
        # Add some small details
        for _ in range(300):
            x = random.randint(0, layer_width)
            y = random.randint(int(self.screen_height * 0.7), layer_height)
            size = random.randint(2, 8)
            
            # Random color between the two ground colors
            mix = random.random()
            color = tuple(int(self.GROUND_COLORS[0][i] * (1-mix) + self.GROUND_COLORS[1][i] * mix) for i in range(3))
            
            pygame.draw.circle(layer, color, (x, y), size)
        
        return layer
    
    def update(self, player_movement):
        # Update camera position based on player movement
        self.camera_pos[0] -= player_movement[0]
        self.camera_pos[1] -= player_movement[1]
        
        # Update layer positions
        for layer in self.layers:
            layer["pos"][0] = (self.camera_pos[0] * layer["speed"]) % self.screen_width
            layer["pos"][1] = (self.camera_pos[1] * layer["speed"]) % self.screen_height
        
        # Update time of day
        self.time_of_day = (self.time_of_day + self.day_cycle_speed) % 1.0
        self.current_sky_colors = self.get_sky_colors()
        
        # Update sky layer
        self.layers[0]["surface"] = self.create_sky_layer()
    
    def draw(self, surface):
        # Draw all layers with parallax effect
        for layer in self.layers:
            # Draw the layer twice side by side for seamless scrolling
            x_pos = int(layer["pos"][0])
            y_pos = int(layer["pos"][1])
            
            # Draw main part
            surface.blit(layer["surface"], (x_pos, 0))
            
            # Draw wrapped part if needed
            if x_pos > 0:
                surface.blit(layer["surface"], (x_pos - layer["surface"].get_width(), 0))
            elif x_pos < 0:
                surface.blit(layer["surface"], (x_pos + layer["surface"].get_width(), 0))
        
        # Draw stars if it's dusk or night
        period = self.current_sky_colors['period']
        if period in ['dusk', 'night']:
            # Calculate star visibility (0 to 1)
            if period == 'dusk':
                # Stars gradually appear during dusk
                star_visibility = (self.time_of_day - 0.75) / 0.25
            else:  # night
                star_visibility = 1.0
                
            # Draw stars with twinkle effect
            for star in self.stars:
                # Calculate current brightness with twinkle effect
                twinkle = math.sin(star['twinkle_phase'] + pygame.time.get_ticks() * star['twinkle_speed'])
                brightness_factor = 0.7 + 0.3 * twinkle  # 0.7 to 1.0
                
                # Apply star visibility
                final_brightness = int(star['brightness'] * brightness_factor * star_visibility)
                star_color = (final_brightness, final_brightness, final_brightness)
                
                # Draw star
                pygame.draw.circle(surface, star_color, (int(star['x']), int(star['y'])), star['size'])

# Test the parallax background
if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Parallax Background Test")
    clock = pygame.time.Clock()
    
    background = ParallaxBackground(screen_width, screen_height)
    
    # For testing movement
    movement = [0, 0]
    speed = 2
    
    # For testing time acceleration
    time_acceleration = 1.0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle key presses for testing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    time_acceleration *= 2
                elif event.key == pygame.K_MINUS:
                    time_acceleration /= 2
        
        # Get keyboard input for testing
        keys = pygame.key.get_pressed()
        movement = [0, 0]
        
        if keys[pygame.K_LEFT]:
            movement[0] = -speed
        if keys[pygame.K_RIGHT]:
            movement[0] = speed
        if keys[pygame.K_UP]:
            movement[1] = -speed
        if keys[pygame.K_DOWN]:
            movement[1] = speed
        
        # Update background with time acceleration
        background.day_cycle_speed = 0.0002 * time_acceleration
        background.update(movement)
        
        # Draw background
        screen.fill((0, 0, 0))
        background.draw(screen)
        
        # Draw instructions
        font = pygame.font.SysFont(None, 24)
        text = font.render("Use arrow keys to move the background", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        time_text = font.render(f"Time of day: {background.time_of_day:.2f} ({background.current_sky_colors['period']})", True, (255, 255, 255))
        screen.blit(time_text, (10, 40))
        
        speed_text = font.render(f"Time speed: {time_acceleration:.1f}x (use +/- to change)", True, (255, 255, 255))
        screen.blit(speed_text, (10, 70))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
