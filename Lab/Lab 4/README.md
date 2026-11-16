# Lab 4: Modularization & Game Engine Refactoring (Frogger)

**Student:** C Rohit Reddy  
**SRN:** PES2UG24CS125  
**Course:** Software Engineering (SETA Labs)  

---

## Overview

Lab 4 explores modular software refactoring, object-oriented design patterns, and AI-assisted debugging applied to a Python **Pygame** implementation of the classic arcade game **Frogger**.

### Refactored Architecture (`frogger/`):
The game is modularized into dedicated components following single-responsibility principles:
- **`main.py`**: Application bootstrap, Pygame initialization, display setup, and main event loop.
- **`game/frog.py`**: Encapsulates frog entity position, grid movement (up/down/left/right), jump animations, and boundary clamping.
- **`game/vehicle.py`**: Implements vehicular traffic entities across multiple road lanes with variable velocities, directions, and lane-wrapping behavior.
- **`game/collisions.py`**: Pure-logic collision detection algorithms checking bounding-box intersections between the frog and active traffic obstacles.
- **`game/renderer.py`**: Handles drawing sprites, lanes, grass safe zones, water barriers, score displays, and game-over states.
- **`game/game_engine.py`**: Central coordinator managing game states (`MENU`, `PLAYING`, `GAME_OVER`, `VICTORY`), lives count, and level transitions.

### Deliverables Included:
1. **Complete Modular Source Code (`frogger/`)**:
   - Structured into clean object-oriented modules with `requirements.txt`.
2. **Gameplay Demonstration Video (`before_and_after_merged_video.mp4`)**:
   - Side-by-side gameplay recording showing the initial buggy version versus the refactored, fully operational game.
3. **AI Pair Programming Transcript (`Frogger_Lab4_Chat_History.pdf`)**:
   - Record of iterative prompt engineering, troubleshooting, and code refinement sessions.
4. **Code Review & Implementation Document (`Frogger_Updated_Code.pdf`)**:
   - Comprehensive source code listing with architectural documentation.
