import chess
import chess.pgn
import chess.engine
import pandas as pd
import time
import os

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
    info = engine.analyse(board, chess.engine.Limit(depth=24))
    engine.quit()
    score = info['score'].white().score()
    progress += 1
    print(progress, fen, score)
    return(score)

def create_analysis(fen):
    global progress
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(depth=24))
    engine.quit()
    progress += 1
    print(progress, fen, info)
    return(info)

def find_positions(file, fen, outfile):
    command = f"pgn-extract -o{outfile} --fenpattern '{fen}' {file}"
    os.system(command)
    print('Done')

if __name__ == '__main__':
    games = open_games('./data/lichess_licoach_2023-01-23.pgn')
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
    df['ply'] = df.groupby(['id']).cumcount()+1
    progress = 0
    df2['score'] = df2['fen'].apply(analyze_position)
    progress = 0
    df2['info'] = df2['fen'].apply(create_analysis)
    df2['score_diff'] = df2['score'].diff()
    print('Done.')
