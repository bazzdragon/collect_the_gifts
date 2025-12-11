# Game Design Document

## Collect the Gifts - Pygame Implementation

### Overview
A time-based gift collection game where players drag floating gifts into Santa's bag to score points.

### Game Flow
```
START GAME
    ↓
Spawn 10 gifts
    ↓
Start 30-second timer
    ↓
[GAME LOOP]
    - Gifts float around screen
    - Player drags gifts to bag
    - Score +1 per gift collected
    - If all 10 collected → Spawn 10 new gifts
    ↓
Time reaches 0
    ↓
GAME OVER - Display final score
```

### Core Mechanics

1. **Gift Spawning**
   - 10 gifts spawn at random positions
   - Each gift has random velocity (-1 to 1 pixels/frame)
   - Gifts bounce off screen edges

2. **Player Interaction**
   - Click and hold to pick up a gift
   - Drag gift to Santa's bag
   - Release to drop gift
   - Gift scores if dropped in bag collision zone

3. **Scoring System**
   - +1 point per gift successfully dropped in bag
   - No penalty for missing
   - Score displayed in real-time

4. **Timer**
   - 30-second countdown
   - Displayed in top-right corner
   - Game ends when timer reaches 0

5. **Respawn System**
   - When all 10 gifts collected, immediately spawn 10 new gifts
   - Allows unlimited scoring potential within time limit

### Technical Implementation

#### Classes
- **Gift**: Manages individual gift state, movement, and rendering
- **Bag**: Represents Santa's bag (collision target)
- **Game**: Main game controller, event handling, and game state

#### Key Features
- Real-time collision detection
- Smooth drag-and-drop mechanics
- Automatic wall bouncing
- Score and timer display
- Game over screen

### Controls
- **Mouse Left Click + Drag**: Pick up and move gifts
- **Mouse Left Click Release**: Drop gift

### Win Condition
- Score as many points as possible in 30 seconds
- No traditional "win" - high score challenge

### Visual Elements
- Gifts: Red squares with gold ribbon (cross pattern)
- Bag: Green oval with darker opening
- Score: Top-left corner
- Timer: Top-right corner
- Game Over: Full-screen overlay with final score
