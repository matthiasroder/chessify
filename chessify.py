import chess
import chess.pgn
import chess.engine
import pandas as pd

def open_games(file):
    games = []
    with open(file) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is not None:
                games.append(game)
            else:
                break
    return games

def create_fens(games):
    fens = []
    for game in games:
        board = game.board()
        for move in game.mainline_moves():
            fens.append(board.fen())
            board.push(move)
    return fens

def analyze_position(fen):
    global progress
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(time=0.01))
    engine.quit()
    score = info['score'].white().score()
    progress += 1
    print(progress, fen, score)
    return(score)

games = open_games('./data/lichess_matthiasroder_2023-01-21.pgn')
fens = create_fens(games)
df = pd.DataFrame(games, columns=['pgn'])
df['id'] = df['pgn'].apply(lambda x: x.headers['Site'].split('/')[-1:][0])
df['url'] = df['pgn'].apply(lambda x: x.headers['Site'])
df['is_white'] = df['pgn'].apply(lambda x: x.headers['White'] == 'matthiasroder')
df['mainline'] = df['pgn'].apply(lambda x: x.mainline())
df['mainline_moves'] = df['pgn'].apply(lambda x: x.mainline_moves())
df2 = pd.DataFrame([(tup.pgn, tup.id, tup.url, tup.is_white, tup.mainline, tup.mainline_moves, move) for tup in df.itertuples() for move in tup.mainline_moves])
df2 = df2.rename(columns={0:'pgn',1:'id',2:'url',3:'is_white',4:'mainline',5:'mainline_moves',6:'move'})
df2['fen'] = fens
progress = 0
df2['score'] = df2['fen'].apply(analyze_position)
