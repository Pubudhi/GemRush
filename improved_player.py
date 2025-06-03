import pygame
import math

# Player class with improved graphics and animations
class ImprovedPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Colors
        self.BLUE = (50, 120, 255)
        self.DARK_BLUE = (30, 60, 180)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Animation frames
        self.frames = {
            'idle': [],
            'walk_right': [],
            'walk_left': [],
            'walk_up': [],
            'walk_down': []
        }
        
        # Create animation frames
        self.create_animation_frames()
        
        # Animation state
        self.state = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.facing_right = True
        
        # Set initial image
        self.image = self.frames['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)  # Center of screen
        
        # Movement
        self.speed = 5
        self.moving = False
        self.direction = pygame.math.Vector2(0, 0)
        
    def create_animation_frames(self):
        # Create idle frames
        for i in range(2):
            frame = pygame.Surface((50, 50), pygame.SRCALPHA)
            
            # Body
            pygame.draw.circle(frame, self.BLUE, (25, 25), 20)
            pygame.draw.circle(frame, self.DARK_BLUE, (25, 25), 20, 2)
            
            # Eyes
            eye_y = 20 if i == 0 else 22  # Blink animation
            pygame.draw.ellipse(frame, self.WHITE, (15, eye_y, 8, 8 if i == 0 else 4))
            pygame.draw.ellipse(frame, self.WHITE, (27, eye_y, 8, 8 if i == 0 else 4))
            pygame.draw.ellipse(frame, self.BLACK, (17, eye_y + 2, 4, 4 if i == 0 else 2))
            pygame.draw.ellipse(frame, self.BLACK, (29, eye_y + 2, 4, 4 if i == 0 else 2))
            
            # Mouth
            mouth_y = 30 + (i * 2)
            pygame.draw.arc(frame, self.WHITE, (15, mouth_y, 20, 10), 0, math.pi, 2)
            
            self.frames['idle'].append(frame)
        
        # Create walking right frames
        for i in range(4):
            frame = pygame.Surface((50, 50), pygame.SRCALPHA)
            
            # Body with squash and stretch
            stretch = abs(((i % 2) * 2) - 1) * 3  # 0,1,0,1 -> 0,3,0,3
            pygame.draw.ellipse(frame, self.BLUE, (25 - 20, 25 - 20 + stretch, 40, 40 - stretch * 2))
            pygame.draw.ellipse(frame, self.DARK_BLUE, (25 - 20, 25 - 20 + stretch, 40, 40 - stretch * 2), 2)
            
            # Eyes
            pygame.draw.ellipse(frame, self.WHITE, (25, 20, 8, 8))
            pygame.draw.ellipse(frame, self.WHITE, (37, 20, 8, 8))
            pygame.draw.ellipse(frame, self.BLACK, (27, 22, 4, 4))
            pygame.draw.ellipse(frame, self.BLACK, (39, 22, 4, 4))
            
            # Mouth
            pygame.draw.arc(frame, self.WHITE, (25, 30, 20, 10), 0, math.pi, 2)
            
            # Arms
            arm_offset = ((i % 2) * 2 - 1) * 5  # -5, 5, -5, 5
            pygame.draw.line(frame, self.DARK_BLUE, (15, 25), (5, 25 + arm_offset), 3)
            pygame.draw.line(frame, self.DARK_BLUE, (35, 25), (45, 25 - arm_offset), 3)
            
            self.frames['walk_right'].append(frame)
        
        # Create walking left frames (flip right frames)
        for frame in self.frames['walk_right']:
            left_frame = pygame.transform.flip(frame, True, False)
            self.frames['walk_left'].append(left_frame)
        
        # Create walking up frames
        for i in range(4):
            frame = pygame.Surface((50, 50), pygame.SRCALPHA)
            
            # Body with squash and stretch
            stretch = abs(((i % 2) * 2) - 1) * 3  # 0,1,0,1 -> 0,3,0,3
            pygame.draw.ellipse(frame, self.BLUE, (25 - 20 + stretch, 25 - 20, 40 - stretch * 2, 40))
            pygame.draw.ellipse(frame, self.DARK_BLUE, (25 - 20 + stretch, 25 - 20, 40 - stretch * 2, 40), 2)
            
            # Eyes (looking up)
            pygame.draw.ellipse(frame, self.WHITE, (15, 15, 8, 8))
            pygame.draw.ellipse(frame, self.WHITE, (27, 15, 8, 8))
            pygame.draw.ellipse(frame, self.BLACK, (17, 16, 4, 4))
            pygame.draw.ellipse(frame, self.BLACK, (29, 16, 4, 4))
            
            # Mouth (smaller when moving up)
            pygame.draw.arc(frame, self.WHITE, (20, 30, 10, 5), 0, math.pi, 2)
            
            # Arms
            arm_offset = ((i % 2) * 2 - 1) * 5  # -5, 5, -5, 5
            pygame.draw.line(frame, self.DARK_BLUE, (15, 25), (15 + arm_offset, 15), 3)
            pygame.draw.line(frame, self.DARK_BLUE, (35, 25), (35 - arm_offset, 15), 3)
            
            self.frames['walk_up'].append(frame)
        
        # Create walking down frames
        for i in range(4):
            frame = pygame.Surface((50, 50), pygame.SRCALPHA)
            
            # Body with squash and stretch
            stretch = abs(((i % 2) * 2) - 1) * 3  # 0,1,0,1 -> 0,3,0,3
            pygame.draw.ellipse(frame, self.BLUE, (25 - 20 + stretch, 25 - 20, 40 - stretch * 2, 40))
            pygame.draw.ellipse(frame, self.DARK_BLUE, (25 - 20 + stretch, 25 - 20, 40 - stretch * 2, 40), 2)
            
            # Eyes (looking down)
            pygame.draw.ellipse(frame, self.WHITE, (15, 20, 8, 8))
            pygame.draw.ellipse(frame, self.WHITE, (27, 20, 8, 8))
            pygame.draw.ellipse(frame, self.BLACK, (17, 23, 4, 4))
            pygame.draw.ellipse(frame, self.BLACK, (29, 23, 4, 4))
            
            # Mouth (bigger smile when moving down)
            pygame.draw.arc(frame, self.WHITE, (15, 30, 20, 10), 0, math.pi, 2)
            
            # Arms
            arm_offset = ((i % 2) * 2 - 1) * 5  # -5, 5, -5, 5
            pygame.draw.line(frame, self.DARK_BLUE, (15, 25), (15 + arm_offset, 35), 3)
            pygame.draw.line(frame, self.DARK_BLUE, (35, 25), (35 - arm_offset, 35), 3)
            
            self.frames['walk_down'].append(frame)
    
    def update(self):
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Reset direction
        self.direction.x = 0
        self.direction.y = 0
        self.moving = False
        
        # Move the player
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.state = 'walk_left'
            self.facing_right = False
            self.moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.state = 'walk_right'
            self.facing_right = True
            self.moving = True
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            if not self.moving:  # Only change state if not already moving horizontally
                self.state = 'walk_up'
            self.moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            if not self.moving:  # Only change state if not already moving horizontally
                self.state = 'walk_down'
            self.moving = True
        
        # If not moving, set to idle
        if not self.moving:
            self.state = 'idle'
        
        # Normalize diagonal movement
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # Move the player
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:  # Assuming screen width is 800
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:  # Assuming screen height is 600
            self.rect.bottom = 600
        
        # Update animation
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            # Make sure we have frames for this state
            if self.state in self.frames and len(self.frames[self.state]) > 0:
                self.frame_index = (self.frame_index + 1) % len(self.frames[self.state])
            else:
                # Fallback to idle if state doesn't have frames
                self.state = 'idle'
                self.frame_index = 0
        
        # Make sure frame_index is valid
        if self.state in self.frames:
            max_frames = len(self.frames[self.state])
            if self.frame_index >= max_frames:
                self.frame_index = 0
        
        # Update image
        if self.state in self.frames and self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][self.frame_index]
        else:
            # Fallback to first idle frame if something goes wrong
            self.image = self.frames['idle'][0]

# Test the player animation
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Player Animation Test")
    clock = pygame.time.Clock()
    
    player = ImprovedPlayer()
    all_sprites = pygame.sprite.Group(player)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        all_sprites.update()
        
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
