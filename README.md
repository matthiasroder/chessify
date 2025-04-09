# Chessify

A Python tool for analyzing chess games using the Stockfish engine.

## Features

- Load chess games from PGN files
- Extract FEN positions from games
- Analyze positions with Stockfish engine
- Find specific positions within games
- Open positions directly in Lichess
- Calculate evaluation scores for positions
- Track move-by-move variations
- Identify potential mistakes by calculating score differences

## Requirements

- Python 3.6+
- python-chess
- pandas
- Stockfish chess engine (must be installed separately)
- pgn-extract (for finding positions)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/chessify.git
   cd chessify
   ```

2. Install the required Python packages:
   ```
   pip install chess pandas
   ```

3. Install Stockfish engine (if not already installed)
   - Download from [Stockfish website](https://stockfishchess.org/download/)
   - Make sure the path to Stockfish is correct in the code

## Usage

```python
import chessify

# Load games from a PGN file
games = chessify.open_games('path/to/your/game.pgn')

# Extract FEN positions
fens = chessify.create_fens(games)

# Analyze a position
score = chessify.analyze_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# Find positions matching a FEN pattern
chessify.find_positions('input.pgn', 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'output.pgn')

# Open a position in Lichess
chessify.open_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
```

## License

See the [LICENSE](LICENSE) file for details.