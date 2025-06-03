import pygame
import random
import math

# Enhanced particle effects
class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def create_collection_effect(self, x, y, color, count=20):
        """Create particles for gem collection effect"""
        for _ in range(count):
            # Random velocity
            speed = random.uniform(1, 5)
            angle = random.uniform(0, 2 * math.pi)
            velocity = [speed * math.cos(angle), speed * math.sin(angle)]
            
            # Random size
            size = random.uniform(2, 6)
            
            # Random lifespan
            lifespan = random.randint(20, 60)
            
            # Create particle
            particle = {
                'pos': [x, y],
                'velocity': velocity,
                'size': size,
                'color': color,
                'alpha': 255,
                'lifespan': lifespan,
                'type': 'circle'
            }
            self.particles.append(particle)
    
    def create_trail_effect(self, x, y, color, count=1):
        """Create trail particles that follow the player"""
        for _ in range(count):
            # Small random offset
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            
            # Slow downward velocity
            velocity = [random.uniform(-0.2, 0.2), random.uniform(0.1, 0.5)]
            
            # Random size
            size = random.uniform(1, 3)
            
            # Short lifespan
            lifespan = random.randint(10, 30)
            
            # Create particle
            particle = {
                'pos': [x + offset_x, y + offset_y],
                'velocity': velocity,
                'size': size,
                'color': color,
                'alpha': 150,
                'lifespan': lifespan,
                'type': 'circle'
            }
            self.particles.append(particle)
    
    def create_sparkle_effect(self, x, y, color, count=1):
        """Create sparkle particles for gems"""
        for _ in range(count):
            # Random position near the gem
            pos_x = x + random.uniform(-10, 10)
            pos_y = y + random.uniform(-10, 10)
            
            # No velocity
            velocity = [0, 0]
            
            # Random size
            size = random.uniform(1, 3)
            
            # Short lifespan
            lifespan = random.randint(5, 15)
            
            # Create particle
            particle = {
                'pos': [pos_x, pos_y],
                'velocity': velocity,
                'size': size,
                'color': (255, 255, 255),  # White sparkles
                'alpha': 200,
                'lifespan': lifespan,
                'type': 'star'
            }
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        # Update each particle
        for particle in self.particles[:]:
            # Move particle
            particle['pos'][0] += particle['velocity'][0]
            particle['pos'][1] += particle['velocity'][1]
            
            # Decrease lifespan
            particle['lifespan'] -= 1
            
            # Fade out
            if particle['lifespan'] < 10:
                particle['alpha'] = int(particle['alpha'] * 0.9)
            
            # Remove if dead
            if particle['lifespan'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        """Draw all particles"""
        for particle in self.particles:
            # Get particle properties
            x, y = int(particle['pos'][0]), int(particle['pos'][1])
            size = int(particle['size'])
            color = particle['color']
            alpha = particle['alpha']
            
            # Create a surface for the particle
            particle_surface = pygame.Surface((size * 2 + 1, size * 2 + 1), pygame.SRCALPHA)
            
            # Draw based on type
            if particle['type'] == 'circle':
                # Apply alpha to color
                color_with_alpha = (*color, alpha)
                pygame.draw.circle(particle_surface, color_with_alpha, (size, size), size)
            elif particle['type'] == 'star':
                # Draw a star shape
                color_with_alpha = (255, 255, 255, alpha)
                points = []
                for i in range(5):
                    # Outer points
                    angle = 2 * math.pi * i / 5 - math.pi / 2
                    points.append((
                        size + size * math.cos(angle),
                        size + size * math.sin(angle)
                    ))
                    # Inner points
                    angle += math.pi / 5
                    points.append((
                        size + size * 0.4 * math.cos(angle),
                        size + size * 0.4 * math.sin(angle)
                    ))
                pygame.draw.polygon(particle_surface, color_with_alpha, points)
            
            # Draw the particle
            surface.blit(particle_surface, (x - size, y - size))

# Light effect for gems and UI
class LightEffect:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lights = []
    
    def add_light(self, x, y, radius, color, intensity=0.5):
        """Add a light source"""
        self.lights.append({
            'pos': [x, y],
            'radius': radius,
            'color': color,
            'intensity': intensity
        })
    
    def update_light(self, index, x, y):
        """Update light position"""
        if 0 <= index < len(self.lights):
            self.lights[index]['pos'] = [x, y]
    
    def remove_light(self, index):
        """Remove a light"""
        if 0 <= index < len(self.lights):
            self.lights.pop(index)
    
    def clear_lights(self):
        """Remove all lights"""
        self.lights = []
    
    def render(self):
        """Render the light effect"""
        # Create a surface for the light overlay
        light_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        # Draw each light
        for light in self.lights:
            x, y = light['pos']
            radius = light['radius']
            color = light['color']
            intensity = light['intensity']
            
            # Create a radial gradient
            for r in range(int(radius), 0, -1):
                alpha = int(255 * (1 - r / radius) * intensity)
                color_with_alpha = (*color, alpha)
                pygame.draw.circle(light_surface, color_with_alpha, (int(x), int(y)), r)
        
        return light_surface

# Screen transition effects
class ScreenTransition:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.progress = 0
        self.speed = 0.02
        self.transition_type = 'fade'
        self.direction = 'in'  # 'in' or 'out'
        self.callback = None
    
    def start(self, transition_type='fade', direction='in', speed=0.02, callback=None):
        """Start a transition effect"""
        self.active = True
        self.progress = 0 if direction == 'in' else 1
        self.transition_type = transition_type
        self.direction = direction
        self.speed = speed
        self.callback = callback
    
    def update(self):
        """Update the transition progress"""
        if not self.active:
            return
        
        # Update progress
        if self.direction == 'in':
            self.progress += self.speed
            if self.progress >= 1:
                self.progress = 1
                self.active = False
                if self.callback:
                    self.callback()
        else:  # 'out'
            self.progress -= self.speed
            if self.progress <= 0:
                self.progress = 0
                self.active = False
                if self.callback:
                    self.callback()
    
    def render(self):
        """Render the transition effect"""
        if not self.active:
            return None
        
        # Create a surface for the transition
        transition_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        if self.transition_type == 'fade':
            # Fade to black
            alpha = int(255 * self.progress)
            transition_surface.fill((0, 0, 0, alpha))
        
        elif self.transition_type == 'circle':
            # Circle wipe
            max_radius = math.sqrt(self.screen_width**2 + self.screen_height**2) / 2
            radius = max_radius * (1 - self.progress)
            pygame.draw.circle(transition_surface, (0, 0, 0, 255), 
                              (self.screen_width // 2, self.screen_height // 2), 
                              int(radius))
            # Invert the circle
            transition_surface.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_SUB)
        
        elif self.transition_type == 'horizontal':
            # Horizontal wipe
            width = int(self.screen_width * self.progress)
            transition_surface.fill((0, 0, 0, 255), (0, 0, width, self.screen_height))
        
        elif self.transition_type == 'vertical':
            # Vertical wipe
            height = int(self.screen_height * self.progress)
            transition_surface.fill((0, 0, 0, 255), (0, 0, self.screen_width, height))
        
        return transition_surface

# Test the visual effects
if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Visual Effects Test")
    clock = pygame.time.Clock()
    
    # Create effect systems
    particles = ParticleSystem()
    lights = LightEffect(screen_width, screen_height)
    transition = ScreenTransition(screen_width, screen_height)
    
    # Add some lights
    lights.add_light(200, 300, 100, (255, 0, 0), 0.3)
    lights.add_light(400, 200, 150, (0, 255, 0), 0.3)
    lights.add_light(600, 400, 120, (0, 0, 255), 0.3)
    
    # For testing
    mouse_pos = [0, 0]
    show_help = True
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Create collection effect
                    particles.create_collection_effect(
                        mouse_pos[0], mouse_pos[1], 
                        (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                    )
                elif event.button == 3:  # Right click
                    # Start a transition
                    transition_types = ['fade', 'circle', 'horizontal', 'vertical']
                    transition.start(
                        random.choice(transition_types),
                        'in' if random.random() > 0.5 else 'out',
                        0.01
                    )
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    show_help = not show_help
        
        # Create trail effect following mouse
        if pygame.mouse.get_pressed()[0]:  # Left button held
            particles.create_trail_effect(
                mouse_pos[0], mouse_pos[1], 
                (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            )
        
        # Create sparkle effect randomly
        if random.random() < 0.1:
            particles.create_sparkle_effect(
                random.randint(0, screen_width),
                random.randint(0, screen_height),
                (255, 255, 255)
            )
        
        # Update effects
        particles.update()
        transition.update()
        
        # Move the first light to follow the mouse
        if len(lights.lights) > 0:
            lights.update_light(0, mouse_pos[0], mouse_pos[1])
        
        # Draw
        screen.fill((20, 20, 30))
        
        # Draw particles
        particles.draw(screen)
        
        # Draw lights
        light_surface = lights.render()
        screen.blit(light_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        
        # Draw transition
        if transition.active:
            transition_surface = transition.render()
            if transition_surface:
                screen.blit(transition_surface, (0, 0))
        
        # Draw help text
        if show_help:
            font = pygame.font.SysFont(None, 24)
            help_texts = [
                "Left click: Create explosion effect",
                "Hold left click: Create trail effect",
                "Right click: Start random transition",
                "H: Toggle help text"
            ]
            for i, text in enumerate(help_texts):
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, (10, 10 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
