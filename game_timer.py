import pygame
import math

class GameTimer:
    def __init__(self, initial_time=60, warning_threshold=15, critical_threshold=5):
        """
        Initialize a game timer
        
        Args:
            initial_time: Initial time in seconds
            warning_threshold: Time in seconds when timer starts showing warning
            critical_threshold: Time in seconds when timer becomes critical
        """
        self.initial_time = initial_time
        self.time_left = initial_time
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.active = True
        self.paused = False
        self.warning_triggered = False
        self.critical_triggered = False
        self.pulse_effect = 0
        
        # Colors
        self.normal_color = (50, 200, 50)  # Green
        self.warning_color = (255, 200, 0)  # Yellow/Orange
        self.critical_color = (255, 50, 50)  # Red
        
        # Callback functions
        self.on_warning = None
        self.on_critical = None
        self.on_timeout = None
    
    def update(self, dt):
        """Update timer with delta time in seconds"""
        if not self.active or self.paused:
            return
        
        # Update time left
        self.time_left -= dt
        
        # Update pulse effect for visual feedback
        self.pulse_effect = (self.pulse_effect + dt * 5) % (2 * math.pi)
        
        # Check if timer has reached warning threshold
        if not self.warning_triggered and self.time_left <= self.warning_threshold:
            self.warning_triggered = True
            if self.on_warning:
                self.on_warning()
        
        # Check if timer has reached critical threshold
        if not self.critical_triggered and self.time_left <= self.critical_threshold:
            self.critical_triggered = True
            if self.on_critical:
                self.on_critical()
        
        # Check if timer has run out
        if self.time_left <= 0:
            self.time_left = 0
            self.active = False
            if self.on_timeout:
                self.on_timeout()
    
    def reset(self, new_time=None):
        """Reset the timer"""
        self.time_left = new_time if new_time is not None else self.initial_time
        self.active = True
        self.warning_triggered = False
        self.critical_triggered = False
    
    def add_time(self, seconds):
        """Add time to the timer"""
        self.time_left += seconds
        
        # Reset warning/critical flags if we're back above thresholds
        if self.time_left > self.warning_threshold:
            self.warning_triggered = False
        if self.time_left > self.critical_threshold:
            self.critical_triggered = False
    
    def get_color(self):
        """Get the current color based on time left"""
        if self.time_left <= self.critical_threshold:
            return self.critical_color
        elif self.time_left <= self.warning_threshold:
            return self.warning_color
        else:
            return self.normal_color
    
    def get_pulse_scale(self):
        """Get a pulsing scale factor for visual effects"""
        if self.time_left <= self.critical_threshold:
            # Faster, stronger pulse when critical
            return 1.0 + 0.2 * abs(math.sin(self.pulse_effect * 2))
        elif self.time_left <= self.warning_threshold:
            # Gentle pulse when warning
            return 1.0 + 0.1 * abs(math.sin(self.pulse_effect))
        else:
            return 1.0
    
    def get_time_string(self):
        """Get time as a formatted string (MM:SS)"""
        minutes = int(self.time_left) // 60
        seconds = int(self.time_left) % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def draw(self, surface, x, y, width=200, height=30, show_text=True, font=None):
        """Draw the timer as a progress bar"""
        # Calculate fill width
        fill_ratio = max(0, min(1, self.time_left / self.initial_time))
        fill_width = int(width * fill_ratio)
        
        # Get current color
        color = self.get_color()
        
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height), border_radius=5)
        
        # Draw fill
        if fill_width > 0:
            pygame.draw.rect(surface, color, (x, y, fill_width, height), border_radius=5)
        
        # Draw border
        pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height), 2, border_radius=5)
        
        # Draw text
        if show_text and font:
            text = self.get_time_string()
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
            surface.blit(text_surface, text_rect)
            
            # Draw "TIME" label
            label_surface = font.render("TIME", True, (255, 255, 255))
            label_rect = label_surface.get_rect(midright=(x - 10, y + height // 2))
            surface.blit(label_surface, label_rect)

# Test the timer
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Timer Test")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    
    # Create timer with 30 seconds
    timer = GameTimer(30, 15, 5)
    
    # Set callbacks
    timer.on_warning = lambda: print("Warning!")
    timer.on_critical = lambda: print("Critical!")
    timer.on_timeout = lambda: print("Time's up!")
    
    # For testing
    paused = False
    
    running = True
    while running:
        # Calculate delta time
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    timer.paused = paused
                elif event.key == pygame.K_r:
                    timer.reset()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    timer.add_time(5)
                elif event.key == pygame.K_MINUS:
                    timer.add_time(-5)
        
        # Update timer
        timer.update(dt)
        
        # Draw
        screen.fill((0, 0, 0))
        
        # Draw timer
        timer.draw(screen, 200, 100, 400, 40, True, font)
        
        # Draw instructions
        instructions = [
            "SPACE: Pause/Resume",
            "R: Reset timer",
            "+: Add 5 seconds",
            "-: Remove 5 seconds"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (50, 200 + i * 40))
        
        # Draw status
        status = "PAUSED" if paused else "RUNNING"
        status_surface = font.render(status, True, (255, 255, 0) if paused else (0, 255, 0))
        screen.blit(status_surface, (650, 50))
        
        pygame.display.flip()
    
    pygame.quit()
