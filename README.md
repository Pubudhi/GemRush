# GemRush

A beautiful 2D gem collecting game with dynamic visuals, time challenges, and a leaderboard system.

![GemRush Game](assets/images/gemrush_icon.png)

## Description

GemRush is an exciting 2D game where you control a character to collect various types of gems against the clock. The game features a day/night cycle, dynamic lighting, particle effects, and a competitive leaderboard system.

## Features

### Core Gameplay
- Collect gems to score points and advance through levels
- Race against the clock with a countdown timer
- Three progressively challenging levels
- Five different gem types with varying point values
- Time bonuses for collecting different gems

### Visual Elements
- Animated player character with smooth movement
- Randomly shaped, colorful gems with unique designs
- Dynamic day/night cycle with changing sky colors
- Twinkling stars that appear during night time
- Particle effects for movement and gem collection
- Dynamic lighting that illuminates the environment
- Screen transitions between game states

### Game Systems
- Leaderboard that tracks scores, completion times, and levels
- Time-based challenge with warning indicators
- Score tracking and high score saving
- Victory and game over screens

## How to Play

### Running the Game
You can run GemRush in three ways:

1. **Desktop Shortcut**:
   - Double-click the GemRush icon on your desktop

2. **Executable**:
   - Run the standalone executable:
   ```
   <path>/gem_collector/dist/GemRush
   ```

3. **Python Script**:
   - Run the Python script directly:
   ```
   cd <path>/pygame-2d/gem_collector
   python3 GemRush.py
   ```

### Controls
- **Arrow keys** or **WASD**: Move the player
- **ESC**: Quit the game
- **R**: Restart after game over or victory
- **L**: View leaderboard (after game over or victory)

## Gem Types and Values

| Gem Type | Points | Time Bonus |
|----------|--------|------------|
| Diamond  | 10     | +5 seconds |
| Ruby     | 8      | +4 seconds |
| Emerald  | 6      | +3 seconds |
| Sapphire | 5      | +2 seconds |
| Topaz    | 4      | +1 second  |

## Requirements

- Python 3.x
- Pygame

## Installation

### From Source
1. Make sure you have Python installed
2. Install Pygame:
```
pip install pygame
```
3. Run the game:
```
python3 GemRush.py
```

### Creating the Executable
If you want to create the executable yourself:
```
pip install pyinstaller
pyinstaller --onefile --windowed --name GemRush GemRush.py
```

## Project Structure

```
gem_collector/
├── GemRush.py              # Main game file
├── improved_player.py      # Player character with animations
├── improved_gems.py        # Detailed gem graphics and animations
├── improved_background.py  # Parallax background with day/night cycle
├── improved_effects.py     # Particle systems and visual effects
├── improved_ui.py          # Enhanced UI elements
├── game_timer.py           # Timer system with warnings
├── leaderboard.py          # Leaderboard system
├── create_icon.py          # Script to create the game icon
├── assets/                 # Directory for game assets
│   ├── images/             # Images and sprites
│   │   └── gemrush_icon.png # Game icon
│   └── sounds/             # Sound effects
├── dist/                   # Contains the compiled executable
│   └── GemRush             # Standalone executable
├── high_score.txt          # Saved high score
├── leaderboard.json        # Saved leaderboard data
└── README.md               # This file
```

## Game Mechanics

### Levels
- **Level 1**: 10 gems required, 60 seconds
- **Level 2**: 15 gems required, 50 seconds
- **Level 3**: 20 gems required, 40 seconds

### Timer
- Timer changes color as time runs low (green → yellow → red)
- Visual and audio warnings when time is running out
- Collect gems to gain additional time

### Leaderboard
- Ranks players by score (higher is better)
- Uses time as a tiebreaker (lower is better)
- Tracks level reached and date/time
- Saves data between game sessions

## Development

GemRush was developed using Python and Pygame. The game features several custom modules:

- **Player System**: Animated character with smooth movement
- **Gem System**: Randomly shaped gems with unique properties
- **Background System**: Dynamic parallax background with day/night cycle
- **Effects System**: Particle effects and dynamic lighting
- **UI System**: Polished user interface elements
- **Timer System**: Countdown timer with visual feedback
- **Leaderboard System**: Score tracking and ranking

## Credits

Created by Pubudhi using Python, Pygame and #AmazonQCLI.

## Future Improvements

- Add sound effects and background music
- Add power-ups and special abilities
- Add obstacles and enemies
- Add more levels and environments
- Add customizable player characters
