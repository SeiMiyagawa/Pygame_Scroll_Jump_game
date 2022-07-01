import pygame
from random import randint

FPS = 30 # Frame par Second
f = 0 # Frame

WINDOW_X,WINDOW_Y = (800,600) # ウィンドウの大きさ

botton = "target.png" # マウスカーソルを合わせる的の画像
target_change = 450 # 的の位置がランダムな位置に移動するまでのフレーム
target_v = 2 # ターゲットの初期の移動速度

class Target(pygame.sprite.Sprite): # 的のクラス
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.vx, self.vy = (vx, vy)
        self.image = pygame.image.load(botton) # 的の画像を読み込む
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height()) # 的と同じ大きさの判定を作成

    def update(self): #座標の更新
        self.rect.move_ip(self.vx, self.vy)