import pygame

FPS = 30 # Frame par Second
f = 0 # Frame

plant_img = "plant.png" # 植物(障害物1)の画像
plant_f = 0 # 植物基準でのフレーム
plant_s = 3 # 植物基準での秒数
plant_scroll = -15.0 # 植物のスクロール速度
plant_count_mode = 0 # 植物が主人公を通り過ぎたらカウント

class Plant(pygame.sprite.Sprite): # 植物のクラス(Spriteを継承)
    def __init__(self, x, y, vx, vy):
        super().__init__() 
        self.vx,self.vy = (vx, vy)
        self.image = pygame.image.load(plant_img) #plant_imgを引数として画像を読み込む
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height()) #plant_imgと同じ大きさの当たり判定の四角形を生成
    
    def update(self): #座標の更新
        self.rect.move_ip(self.vx, self.vy)
