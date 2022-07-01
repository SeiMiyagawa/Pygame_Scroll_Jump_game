import pygame

FPS = 30
f = 0

bird_img = "bird1.png" # 鳥(障害物2)の画像
bird_f = 0 # 鳥基準基準のフレーム
bird_s = 30 # 鳥基準での秒数
bird_scroll = -15
bird_scroll_min = -15 # 鳥のscroll速度の最低
bird_scroll_max = bird_scroll_min - 10 # 最高
bird_count_mode = 0 # 鳥が主人公を通り過ぎたらカウント

class Bird(pygame.sprite.Sprite): #鳥のクラス(Sprite) 
    def __init__(self, x, y, vx, vy):
        super().__init__() 
        self.vx,self.vy = (vx, vy)
        self.image = pygame.image.load(bird_img) #鳥の画像の読み込み
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height()) # 鳥の画像と同じ大きさの判定を設定
    
    def update(self): #座標の更新
        self.rect.move_ip(self.vx, self.vy)