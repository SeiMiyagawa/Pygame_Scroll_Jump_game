from game import * 

WINDOW_X, WINDOW_Y = (1000, 400)  # ウィンドウサイズを指定

def main():
    game = Game(WINDOW_X, WINDOW_Y, "running_game")
    game.setup() # 初期設定と初期処理
    game.run()

if __name__ == "__main__":
    main()