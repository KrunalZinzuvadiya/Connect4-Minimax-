# Connect4 Minimax

A Python implementation of the Connect 4 game with an AI opponent that uses the Minimax algorithm with Alpha-Beta pruning for decision-making.

## Features
- **AI vs. Human Gameplay**: Play against an AI that evaluates moves using Minimax.
- **Dynamic Board Evaluation**: The AI scores board states to decide the best move.
- **Winning Detection**: The game highlights winning moves for both players.
- **Graphical Interface**: Interactive UI created using Pygame.

## Requirements
- Python 3.x
- Pygame library

Install Pygame via pip:
```bash
pip install pygame
```
Folder Structure
```
Connect4-Minimax/
├── Connect4_minimax.py  # Main game script
├── img/
      ├── Board_Image.png  # Board background image
      ├── Red2.png         # Player piece image
      ├── Yellow2.png      # AI piece image
```
Minimax Algorithm
The AI uses the Minimax algorithm with Alpha-Beta pruning to evaluate possible moves:  

    Evaluation Function: Assigns scores to board states based on potential winning opportunities.
    Alpha-Beta Pruning: Optimizes the decision-making process by pruning suboptimal branches.  
    
Future Enhancements  

      Add difficulty levels for AI.  
      Multiplayer mode.  
      Online gameplay support.  
      
      
License  
This project is licensed under the MIT License. See the LICENSE file for details.  

Contributions  
Contributions are welcome! Feel free to fork the repository and submit pull requests.  

Author  
Krunal Zinzuvadiya
