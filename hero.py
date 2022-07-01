import pygame

FPS = 30
f = 0

WINDOW_X, WINDOW_Y = (800, 600)

hero_img = "hero_walk1.png" #主人公の画像
hero_X = 100 # 主人公のx座標
hero_Y = 300 # y座標
hero_mode = 0 # 主人公のモード
jump_power = -20 # 主人公がジャンプする力
fall = 1.5 # 重力

class Hero(pygame.sprite.Sprite): # 主人公のクラス(Spriteを継承) 
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.x, self.y, self.vx,self.vy = (x, y, vx, vy)
        self.image = pygame.image.load(hero_img) #hero_imgを引数として画像を読み込む
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height()) #hero_imgと同じ大きさの当たり判定の四角形を生成
    
    def update(self): #座標の更新
        self.rect.move_ip(self.vx, self.vy)
        