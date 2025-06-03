import pygame
import math

class ImprovedUI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GOLD = (255, 215, 0)
        self.BLUE = (50, 100, 255)
        self.DARK_BLUE = (20, 40, 100)
        self.GREEN = (50, 200, 50)
        self.RED = (200, 50, 50)
        
        # Load fonts
        pygame.font.init()
        try:
            self.title_font = pygame.font.Font(None, 64)
            self.header_font = pygame.font.Font(None, 48)
            self.medium_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except:
            # Fallback to system font
            self.title_font = pygame.font.SysFont(None, 64)
            self.header_font = pygame.font.SysFont(None, 48)
            self.medium_font = pygame.font.SysFont(None, 36)
            self.small_font = pygame.font.SysFont(None, 24)
        
        # UI elements
        self.buttons = []
        self.panels = []
        self.animations = {}
        
        # Animation timer
        self.animation_timer = 0
    
    def update(self, dt=1/60):
        """Update UI animations"""
        self.animation_timer += dt
        
        # Update button animations
        for button in self.buttons:
            if button.get('hover_animation', False):
                button['hover_scale'] = 1.0 + 0.05 * math.sin(self.animation_timer * 5)
    
    def draw_text(self, surface, text, font, color, x, y, align="center", shadow=True, shadow_color=(0, 0, 0), shadow_offset=2):
        """Draw text with optional shadow and alignment"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        # Set position based on alignment
        if align == "center":
            text_rect.center = (x, y)
        elif align == "left":
            text_rect.midleft = (x, y)
        elif align == "right":
            text_rect.midright = (x, y)
        
        # Draw shadow
        if shadow:
            shadow_surface = font.render(text, True, shadow_color)
            shadow_rect = shadow_surface.get_rect()
            shadow_rect.x = text_rect.x + shadow_offset
            shadow_rect.y = text_rect.y + shadow_offset
            surface.blit(shadow_surface, shadow_rect)
        
        # Draw text
        surface.blit(text_surface, text_rect)
        
        return text_rect
    
    def create_button(self, text, x, y, width, height, color, hover_color, text_color=None, action=None, animated=True):
        """Create a button"""
        if text_color is None:
            text_color = self.WHITE
            
        button = {
            'text': text,
            'rect': pygame.Rect(x, y, width, height),
            'color': color,
            'hover_color': hover_color,
            'text_color': text_color,
            'action': action,
            'hover': False,
            'hover_animation': animated,
            'hover_scale': 1.0
        }
        
        self.buttons.append(button)
        return len(self.buttons) - 1  # Return button index
    
    def draw_button(self, surface, button_index):
        """Draw a button"""
        button = self.buttons[button_index]
        
        # Get button properties
        rect = button['rect']
        color = button['hover_color'] if button['hover'] else button['color']
        text = button['text']
        text_color = button['text_color']
        
        # Apply hover animation
        if button['hover'] and button['hover_animation']:
            # Create a slightly larger rect for the hover effect
            scaled_rect = rect.copy()
            scale = button['hover_scale']
            scaled_rect.width = int(rect.width * scale)
            scaled_rect.height = int(rect.height * scale)
            scaled_rect.center = rect.center
            
            # Draw button with rounded corners
            pygame.draw.rect(surface, color, scaled_rect, border_radius=10)
            pygame.draw.rect(surface, self.BLACK, scaled_rect, 2, border_radius=10)
            
            # Draw text
            self.draw_text(surface, text, self.medium_font, text_color, 
                          scaled_rect.centerx, scaled_rect.centery)
        else:
            # Draw button with rounded corners
            pygame.draw.rect(surface, color, rect, border_radius=10)
            pygame.draw.rect(surface, self.BLACK, rect, 2, border_radius=10)
            
            # Draw text
            self.draw_text(surface, text, self.medium_font, text_color, 
                          rect.centerx, rect.centery)
    
    def check_button_hover(self, mouse_pos):
        """Check if mouse is hovering over any button"""
        for button in self.buttons:
            button['hover'] = button['rect'].collidepoint(mouse_pos)
    
    def check_button_click(self, mouse_pos):
        """Check if a button was clicked and execute its action"""
        for button in self.buttons:
            if button['rect'].collidepoint(mouse_pos) and button['action']:
                button['action']()
                return True
        return False
    
    def create_panel(self, x, y, width, height, color=(0, 0, 0, 180), border=True, border_color=None, border_width=2, border_radius=10):
        """Create a panel"""
        if border_color is None:
            border_color = self.WHITE
            
        panel = {
            'rect': pygame.Rect(x, y, width, height),
            'color': color,
            'border': border,
            'border_color': border_color,
            'border_width': border_width,
            'border_radius': border_radius,
            'elements': []
        }
        
        self.panels.append(panel)
        return len(self.panels) - 1  # Return panel index
    
    def add_text_to_panel(self, panel_index, text, font, color, x, y, align="center", shadow=True):
        """Add text to a panel"""
        element = {
            'type': 'text',
            'text': text,
            'font': font,
            'color': color,
            'x': x,
            'y': y,
            'align': align,
            'shadow': shadow
        }
        
        self.panels[panel_index]['elements'].append(element)
    
    def add_image_to_panel(self, panel_index, image, x, y, width=None, height=None):
        """Add image to a panel"""
        if width and height:
            image = pygame.transform.scale(image, (width, height))
            
        element = {
            'type': 'image',
            'image': image,
            'x': x,
            'y': y
        }
        
        self.panels[panel_index]['elements'].append(element)
    
    def draw_panel(self, surface, panel_index):
        """Draw a panel with all its elements"""
        panel = self.panels[panel_index]
        
        # Get panel properties
        rect = panel['rect']
        color = panel['color']
        border = panel['border']
        border_color = panel['border_color']
        border_width = panel['border_width']
        border_radius = panel['border_radius']
        
        # Create a surface for the panel with alpha
        panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # Fill with background color
        pygame.draw.rect(panel_surface, color, (0, 0, rect.width, rect.height), border_radius=border_radius)
        
        # Draw border
        if border:
            pygame.draw.rect(panel_surface, border_color, (0, 0, rect.width, rect.height), 
                           border_width, border_radius=border_radius)
        
        # Draw elements
        for element in panel['elements']:
            if element['type'] == 'text':
                self.draw_text(panel_surface, element['text'], element['font'], element['color'],
                              element['x'], element['y'], element['align'], element['shadow'])
            elif element['type'] == 'image':
                image_rect = element['image'].get_rect()
                image_rect.topleft = (element['x'], element['y'])
                panel_surface.blit(element['image'], image_rect)
        
        # Draw panel to surface
        surface.blit(panel_surface, rect)
    
    def draw_progress_bar(self, surface, x, y, width, height, progress, max_value, color, bg_color=(50, 50, 50), border_color=None, show_text=True):
        """Draw a progress bar"""
        if border_color is None:
            border_color = self.BLACK
            
        # Calculate fill width
        fill_width = int((progress / max_value) * width) if max_value > 0 else 0
        
        # Draw background
        pygame.draw.rect(surface, bg_color, (x, y, width, height), border_radius=5)
        
        # Draw fill
        if fill_width > 0:
            pygame.draw.rect(surface, color, (x, y, fill_width, height), border_radius=5)
        
        # Draw border
        pygame.draw.rect(surface, border_color, (x, y, width, height), 2, border_radius=5)
        
        # Draw text
        if show_text:
            text = f"{progress}/{max_value}"
            self.draw_text(surface, text, self.small_font, self.WHITE, x + width // 2, y + height // 2)
    
    def draw_gem_counter(self, surface, x, y, gem_count, max_gems, gem_image=None):
        """Draw a gem counter with icon"""
        # Draw gem icon or placeholder
        icon_size = 30
        if gem_image:
            scaled_image = pygame.transform.scale(gem_image, (icon_size, icon_size))
            surface.blit(scaled_image, (x, y))
        else:
            # Draw a simple diamond shape
            points = [(x + icon_size//2, y), (x + icon_size, y + icon_size//2), 
                     (x + icon_size//2, y + icon_size), (x, y + icon_size//2)]
            pygame.draw.polygon(surface, self.GOLD, points)
            pygame.draw.polygon(surface, self.BLACK, points, 2)
        
        # Draw text
        text = f"{gem_count}/{max_gems}"
        self.draw_text(surface, text, self.medium_font, self.WHITE, x + icon_size + 10, y + icon_size//2, align="left")
    
    def draw_score_display(self, surface, x, y, score, text="Score"):
        """Draw a score display with animation for score changes"""
        # Draw text
        self.draw_text(surface, text, self.medium_font, self.WHITE, x, y, align="left")
        
        # Draw score with pulsing effect if it changed recently
        score_text = str(score)
        score_color = self.GOLD
        
        # Check if we have a score animation
        if 'score' in self.animations:
            if self.animations['score']['value'] != score:
                # Score changed, start animation
                self.animations['score'] = {
                    'value': score,
                    'timer': 1.0,  # Animation duration in seconds
                    'start_scale': 1.5,  # Starting scale
                    'end_scale': 1.0     # Ending scale
                }
            elif self.animations['score']['timer'] > 0:
                # Animation in progress
                self.animations['score']['timer'] -= 1/60  # Assuming 60 FPS
                
                # Calculate current scale
                progress = 1.0 - (self.animations['score']['timer'] / 1.0)  # 0 to 1
                current_scale = self.animations['score']['start_scale'] + (
                    self.animations['score']['end_scale'] - self.animations['score']['start_scale']
                ) * progress
                
                # Draw with scale
                score_surface = self.medium_font.render(score_text, True, score_color)
                score_rect = score_surface.get_rect()
                score_rect.midleft = (x + 100, y)
                
                # Scale the surface
                scaled_width = int(score_rect.width * current_scale)
                scaled_height = int(score_rect.height * current_scale)
                scaled_surface = pygame.transform.scale(score_surface, (scaled_width, scaled_height))
                
                # Adjust position to keep midleft anchor
                scaled_rect = scaled_surface.get_rect()
                scaled_rect.midleft = score_rect.midleft
                
                # Draw
                surface.blit(scaled_surface, scaled_rect)
                return
        else:
            # Initialize animation
            self.animations['score'] = {
                'value': score,
                'timer': 0,
                'start_scale': 1.0,
                'end_scale': 1.0
            }
        
        # Draw normal score
        self.draw_text(surface, score_text, self.medium_font, score_color, x + 100, y, align="left")
    
    def draw_level_indicator(self, surface, x, y, level, max_level):
        """Draw a level indicator with stars"""
        # Draw text
        self.draw_text(surface, f"Level {level}/{max_level}", self.medium_font, self.WHITE, x, y)
        
        # Draw stars
        star_spacing = 30
        for i in range(max_level):
            star_x = x + (i - max_level/2) * star_spacing
            star_y = y + 30
            
            # Determine if star is filled
            filled = i < level
            color = self.GOLD if filled else (100, 100, 100)
            
            # Draw star
            self.draw_star(surface, star_x, star_y, 10, color, filled)
    
    def draw_star(self, surface, x, y, size, color, filled=True):
        """Draw a star shape"""
        points = []
        for i in range(5):
            # Outer points
            angle = 2 * math.pi * i / 5 - math.pi / 2
            points.append((
                x + size * math.cos(angle),
                y + size * math.sin(angle)
            ))
            # Inner points
            angle += math.pi / 5
            points.append((
                x + size * 0.4 * math.cos(angle),
                y + size * 0.4 * math.sin(angle)
            ))
        
        if filled:
            pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, self.BLACK, points, 2)
    
    def draw_game_over_screen(self, surface, score, high_score=None):
        """Draw a game over screen"""
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Draw game over text
        self.draw_text(surface, "Game Over", self.title_font, self.RED, 
                      self.screen_width // 2, self.screen_height // 2 - 100)
        
        # Draw score
        self.draw_text(surface, f"Score: {score}", self.header_font, self.WHITE, 
                      self.screen_width // 2, self.screen_height // 2)
        
        # Draw high score if provided
        if high_score is not None:
            if score > high_score:
                self.draw_text(surface, "New High Score!", self.medium_font, self.GOLD, 
                              self.screen_width // 2, self.screen_height // 2 + 50)
            else:
                self.draw_text(surface, f"High Score: {high_score}", self.medium_font, self.WHITE, 
                              self.screen_width // 2, self.screen_height // 2 + 50)
        
        # Draw restart instruction - moved lower to avoid overlap
        self.draw_text(surface, "Press R to restart", self.medium_font, self.WHITE, 
                      self.screen_width // 2, self.screen_height // 2 + 120)
    
    def draw_victory_screen(self, surface, score, high_score=None):
        """Draw a victory screen"""
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Draw victory text
        self.draw_text(surface, "Victory!", self.title_font, self.GOLD, 
                      self.screen_width // 2, self.screen_height // 2 - 100)
        
        # Draw score
        self.draw_text(surface, f"Final Score: {score}", self.header_font, self.WHITE, 
                      self.screen_width // 2, self.screen_height // 2)
        
        # Draw high score if provided
        if high_score is not None:
            if score > high_score:
                self.draw_text(surface, "New High Score!", self.medium_font, self.GOLD, 
                              self.screen_width // 2, self.screen_height // 2 + 50)
            else:
                self.draw_text(surface, f"High Score: {high_score}", self.medium_font, self.WHITE, 
                              self.screen_width // 2, self.screen_height // 2 + 50)
        
        # Draw restart instruction - moved lower to align better with time value
        self.draw_text(surface, "Press R to play again", self.medium_font, self.WHITE, 
                      self.screen_width // 2, self.screen_height // 2 + 150)
                      
        # Draw exit button
        exit_button_width = 180  # Increased from 120
        exit_button_height = 50  # Increased from 40
        exit_button_x = self.screen_width // 2 - exit_button_width // 2
        exit_button_y = self.screen_height // 2 + 220
        
        # Draw button background
        pygame.draw.rect(surface, (180, 30, 30), 
                        (exit_button_x, exit_button_y, exit_button_width, exit_button_height),
                        border_radius=10)
        
        # Draw button border
        pygame.draw.rect(surface, (255, 255, 255), 
                        (exit_button_x, exit_button_y, exit_button_width, exit_button_height),
                        2, border_radius=10)
        
        # Draw button text
        self.draw_text(surface, "Exit Game", self.medium_font, self.WHITE,
                      self.screen_width // 2, exit_button_y + exit_button_height // 2)

# Test the UI
if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("UI Test")
    clock = pygame.time.Clock()
    
    ui = ImprovedUI(screen_width, screen_height)
    
    # Create some buttons
    start_button = ui.create_button("Start Game", screen_width // 2 - 100, screen_height // 2 - 50, 
                                   200, 50, ui.BLUE, ui.GREEN)
    
    options_button = ui.create_button("Options", screen_width // 2 - 100, screen_height // 2 + 20, 
                                     200, 50, ui.BLUE, ui.GREEN)
    
    quit_button = ui.create_button("Quit", screen_width // 2 - 100, screen_height // 2 + 90, 
                                  200, 50, ui.RED, (255, 100, 100))
    
    # Create a panel
    panel = ui.create_panel(50, 50, 300, 200)
    ui.add_text_to_panel(panel, "Game Stats", ui.header_font, ui.WHITE, 150, 30)
    ui.add_text_to_panel(panel, "Score: 1000", ui.medium_font, ui.WHITE, 150, 80)
    ui.add_text_to_panel(panel, "Level: 3", ui.medium_font, ui.WHITE, 150, 120)
    ui.add_text_to_panel(panel, "Time: 02:45", ui.medium_font, ui.WHITE, 150, 160)
    
    # Test variables
    score = 0
    gems = 0
    max_gems = 10
    level = 1
    max_level = 3
    show_game_over = False
    show_victory = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    ui.check_button_click(event.pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    score += 10
                elif event.key == pygame.K_DOWN:
                    score = max(0, score - 10)
                elif event.key == pygame.K_RIGHT:
                    gems = min(max_gems, gems + 1)
                elif event.key == pygame.K_LEFT:
                    gems = max(0, gems - 1)
                elif event.key == pygame.K_g:
                    show_game_over = not show_game_over
                elif event.key == pygame.K_v:
                    show_victory = not show_victory
        
        # Update UI
        ui.update()
        ui.check_button_hover(pygame.mouse.get_pos())
        
        # Draw
        screen.fill((20, 20, 30))
        
        # Draw UI elements
        ui.draw_button(screen, start_button)
        ui.draw_button(screen, options_button)
        ui.draw_button(screen, quit_button)
        ui.draw_panel(screen, panel)
        
        # Draw progress bar
        ui.draw_progress_bar(screen, 400, 50, 300, 30, gems, max_gems, ui.GREEN)
        
        # Draw gem counter
        ui.draw_gem_counter(screen, 400, 100, gems, max_gems)
        
        # Draw score display
        ui.draw_score_display(screen, 400, 150, score)
        
        # Draw level indicator
        ui.draw_level_indicator(screen, 400, 200, level, max_level)
        
        # Draw help text
        ui.draw_text(screen, "Controls:", ui.medium_font, ui.WHITE, 400, 300, align="left")
        ui.draw_text(screen, "Up/Down: Change score", ui.small_font, ui.WHITE, 400, 330, align="left")
        ui.draw_text(screen, "Left/Right: Change gems", ui.small_font, ui.WHITE, 400, 360, align="left")
        ui.draw_text(screen, "G: Toggle game over screen", ui.small_font, ui.WHITE, 400, 390, align="left")
        ui.draw_text(screen, "V: Toggle victory screen", ui.small_font, ui.WHITE, 400, 420, align="left")
        
        # Draw game over or victory screen if active
        if show_game_over:
            ui.draw_game_over_screen(screen, score, high_score=1000)
        elif show_victory:
            ui.draw_victory_screen(screen, score, high_score=1000)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
