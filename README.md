# Gomoku Game AI
**Due Date: Fall 2023**

## Project Overview
An implementation of the Gomoku (Five in a Row) game with an AI opponent. The project includes a game board implementation and an AI engine that uses strategic scoring to determine optimal moves.

## Game Rules
- Played on an 8x8 board
- Two players: black (AI) and white (human)
- Black moves first
- Players alternate placing stones
- Win condition: 5 stones in a row (horizontal, vertical, or diagonal)

## Features
- Interactive gameplay against AI opponent
- Board visualization
- Strategic AI move calculation
- Sequence detection in multiple directions
- Win condition verification

## Key Components
### Board Analysis
- Detects stone sequences in four directions:
  - Horizontal (left-to-right)
  - Vertical (top-to-bottom)
  - Diagonal (upper-left to lower-right)
  - Diagonal (upper-right to lower-left)

### Sequence Types
- Open sequences
- Semi-open sequences
- Closed sequences

## Core Functions
- `is_empty(board)`: Checks if board is empty
- `is_bounded(board, y_end, x_end, length, d_y, d_x)`: Analyzes sequence boundaries
- `detect_row(board, col, y_start, x_start, length, d_y, d_x)`: Finds sequences in a row
- `detect_rows(board, col, length)`: Analyzes entire board for sequences
- `search_max(board)`: Determines optimal AI move
- `is_win(board)`: Checks for win conditions

## Usage
```python
board = make_empty_board(8)
play_gomoku(8)
