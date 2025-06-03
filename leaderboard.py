import pygame
import json
import os
from datetime import datetime

class Leaderboard:
    def __init__(self, max_entries=10):
        self.max_entries = max_entries
        self.entries = []
        self.leaderboard_file = "leaderboard.json"
        self.load_leaderboard()
    
    def load_leaderboard(self):
        """Load leaderboard from file"""
        try:
            if os.path.exists(self.leaderboard_file):
                with open(self.leaderboard_file, 'r') as f:
                    self.entries = json.load(f)
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            self.entries = []
    
    def save_leaderboard(self):
        """Save leaderboard to file"""
        try:
            with open(self.leaderboard_file, 'w') as f:
                json.dump(self.entries, f)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
    
    def add_entry(self, score, time_taken, level_reached):
        """Add a new entry to the leaderboard"""
        # Create entry with current date/time
        entry = {
            "score": score,
            "time_taken": time_taken,
            "level_reached": level_reached,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # Add entry to list
        self.entries.append(entry)
        
        # Sort entries by score (primary) and time (secondary, lower is better)
        self.entries.sort(key=lambda x: (-x["score"], x["time_taken"]))
        
        # Keep only top entries
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[:self.max_entries]
        
        # Save to file
        self.save_leaderboard()
        
        # Return position in leaderboard (1-based)
        return self.get_position(score, time_taken)
    
    def get_position(self, score, time_taken):
        """Get position of a score in the leaderboard (1-based)"""
        for i, entry in enumerate(self.entries):
            if entry["score"] == score and entry["time_taken"] == time_taken:
                return i + 1
        return -1
    
    def draw(self, surface, x, y, width, height, font_large, font_medium, font_small):
        """Draw the leaderboard on the screen"""
        # Create background panel
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 200))  # Semi-transparent black
        
        # Draw title
        title = font_large.render("LEADERBOARD", True, (255, 215, 0))  # Gold
        title_rect = title.get_rect(centerx=width // 2, y=10)
        panel.blit(title, title_rect)
        
        # Draw headers
        header_y = title_rect.bottom + 20
        headers = ["Rank", "Score", "Time", "Level", "Date"]
        header_widths = [0.1, 0.2, 0.2, 0.15, 0.35]  # Proportions of total width
        
        for i, header in enumerate(headers):
            header_x = sum(header_widths[:i]) * width
            header_w = header_widths[i] * width
            header_text = font_medium.render(header, True, (200, 200, 200))
            header_rect = header_text.get_rect(centerx=header_x + header_w // 2, y=header_y)
            panel.blit(header_text, header_rect)
        
        # Draw separator line
        pygame.draw.line(panel, (150, 150, 150), (10, header_y + 30), (width - 10, header_y + 30), 2)
        
        # Draw entries
        entry_y = header_y + 40
        entry_height = 30
        
        for i, entry in enumerate(self.entries):
            # Alternate row colors
            row_color = (50, 50, 80) if i % 2 == 0 else (40, 40, 60)
            pygame.draw.rect(panel, row_color, (10, entry_y, width - 20, entry_height))
            
            # Draw rank
            rank_text = font_medium.render(f"{i+1}", True, (255, 255, 255))
            rank_x = header_widths[0] * width // 2
            panel.blit(rank_text, rank_text.get_rect(center=(rank_x, entry_y + entry_height // 2)))
            
            # Draw score
            score_text = font_medium.render(f"{entry['score']}", True, (255, 255, 0))
            score_x = header_widths[0] * width + header_widths[1] * width // 2
            panel.blit(score_text, score_text.get_rect(center=(score_x, entry_y + entry_height // 2)))
            
            # Draw time
            minutes = int(entry['time_taken']) // 60
            seconds = int(entry['time_taken']) % 60
            time_text = font_medium.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
            time_x = sum(header_widths[:2]) * width + header_widths[2] * width // 2
            panel.blit(time_text, time_text.get_rect(center=(time_x, entry_y + entry_height // 2)))
            
            # Draw level
            level_text = font_medium.render(f"{entry['level_reached']}", True, (255, 255, 255))
            level_x = sum(header_widths[:3]) * width + header_widths[3] * width // 2
            panel.blit(level_text, level_text.get_rect(center=(level_x, entry_y + entry_height // 2)))
            
            # Draw date
            date_text = font_small.render(entry['date'], True, (200, 200, 200))
            date_x = sum(header_widths[:4]) * width + header_widths[4] * width // 2
            panel.blit(date_text, date_text.get_rect(center=(date_x, entry_y + entry_height // 2)))
            
            entry_y += entry_height
        
        # Draw border
        pygame.draw.rect(panel, (150, 150, 150), (0, 0, width, height), 2, border_radius=5)
        
        # Draw on surface
        surface.blit(panel, (x, y))
        
        return panel

# Test the leaderboard
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Leaderboard Test")
    clock = pygame.time.Clock()
    
    # Create fonts
    font_large = pygame.font.SysFont(None, 48)
    font_medium = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 24)
    
    # Create leaderboard
    leaderboard = Leaderboard()
    
    # Add some test entries if empty
    if not leaderboard.entries:
        leaderboard.add_entry(100, 45.5, 3)
        leaderboard.add_entry(80, 60.2, 2)
        leaderboard.add_entry(120, 55.8, 3)
        leaderboard.add_entry(100, 40.0, 3)
        leaderboard.add_entry(50, 30.0, 1)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Add random entry on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                import random
                score = random.randint(10, 150)
                time = random.uniform(30, 90)
                level = random.randint(1, 3)
                position = leaderboard.add_entry(score, time, level)
                print(f"Added entry: Score {score}, Time {time:.1f}, Level {level} - Position: {position}")
        
        # Draw
        screen.fill((30, 30, 50))
        leaderboard.draw(screen, 50, 50, 700, 500, font_large, font_medium, font_small)
        
        # Draw instructions
        instructions = font_small.render("Click to add random entry", True, (255, 255, 255))
        screen.blit(instructions, (50, 560))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
