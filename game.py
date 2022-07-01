import pygame
import sys
import time
from random import randint

from hero import * 
from plant import *
from bird import *
from target import *

FPS = 30 # frame par second
s = int(time.perf_counter()) # second

hero_img = "" # 主人公の画像を入れるための変数
hero_X, hero_Y = (100, 300) # 主人公の座標
jump_power = -20 # 主人公のジャンプ力
fall = 1.5 # 重力

plant_s = 3 # 植物が発生し始めるまでの秒数
plant_scroll = -15.0 # scroll速度

bird_img = "" # 鳥の画像を入れるための変数
bird_s = 20 # 鳥が発生し始めるまでの秒数
bird_scroll_min = plant_scroll # 鳥のscroll速度の最小
bird_scroll_max = bird_scroll_min + 10 # 最大d

wall_move_x = 3 # 横壁の移動速度
wall_move_y = 2 # 竪壁の移動速度

# ------------------------------------------------------------

class Game(): # Gameクラスで全体の管理を行う
    # (初期設定)
    def __init__(self, width, height, window_name): # 初期処理
        pygame.init() # pygameの初期化
        self.width, self.height = (width, height) # ウィンドウサイズ
        self.screen = pygame.display.set_mode((width, height)) # ウィンドウを表示
        pygame.display.set_caption(window_name) # ウィンドウの名前
        self.clock = pygame.time.Clock() # フレームを管理する関数の呼び出し
        self.font = pygame.font.Font(None, 30) # 文字の設定
    
    def setup(self): # 初期値などの設定
        self.f = 0 # フレーム
        self.score = 0 # スコア
        self.game_mode = 0 # ゲームのモード
        self.hero = Hero(hero_X,hero_Y,0,0) # 主人公の配置
        self.hero_mode = 0 # 主人公のモード
        self.plants = pygame.sprite.Group() # 植物の枠を設置(Group)
        self.plant_f = 0 # 植物基準で見たフレーム
        self.plant_border = 0 # 植物が発生するまでのボーダー
        self.plant_count_mode = 0 # 主人公が植物のX座標を超えた時にスコアにカウントする際に使う変数
        self.birds = pygame.sprite.Group() # 鳥の枠を設置(Group)
        self.bird_f = 0 # 鳥基準で見たフレーム
        self.bird_border = 0 # 鳥が発生するまでのボーダー
        self.bird_count_mode = 0 # 主人公が鳥のX座標を超えた時にスコアにカウントする際に使う変数
        self.plant_border = randint(30,120) # ボーダーの設定
        self.bird_border = randint(100, 200)
        self.target = Target(100, self.height - 200, 0, 0) # 的の配置
        self.target_v = 2 # 的の移動速度の初期設定
        self.target_change = 600 # 的が再配置されるまでのフレーム数
        self.wall_x = 0 # 横壁の座標
        self.wall_y = 0 # 竪壁の座標

    # -----------------------------------------------------------
    # (メインプログラム)
    def run(self): 
        while True:
            for event in pygame.event.get():# ウィンドウの×ボタンを押した時、game_modeを99にする
                if event.type == pygame.QUIT:
                    self.game_mode = 99
            # (描画)
            self.plants.draw(self.screen) # 植物と鳥を描画
            self.birds.draw(self.screen)

            # (フレーム管理)
            self.clock.tick(FPS) # フレームの切り替え？
            self.f += 1 # フレームのカウントを+1
            if f % 10 == 0: # 10フレームごとにスコアを+1
                self.score += 1
            s = int(time.perf_counter()) # 秒数
            if s > plant_s: # 秒数が3秒を超えたら、植物基準のフレームのカウントを開始
                self.plant_f += 1 
            if s > bird_s + plant_s: # 秒数が20秒を超えたら、鳥基準でのフレームのカウントを開始
                self.bird_f += 1
            
            # (主人公の処理)
            if self.hero_mode == 0: # 主人公がジャンプしていないとき、フレームを3で割った商を2で割った余りによって画像を切り替える
                if (self.f // 3) % 2 == 0: 
                    hero_img = "hero_walk1.png"
                else:
                    hero_img = "hero_walk2.png"
            
            pressed_keys = pygame.key.get_pressed() # 的の中にポインタがないときにスペースキーを押すとジャンプ 
            mouse_xy = pygame.mouse.get_pos()
            if pressed_keys[pygame.K_SPACE]\
            and not (self.target.rect.x <= mouse_xy[0] <= self.target.rect.x + self.target.image.get_width() \
            and self.target.rect.y <= mouse_xy[1] <= self.target.rect.y + self.target.image.get_height()):
                if self.hero_mode == 0: # ジャンプ中にサイドジャンプしないよう、主人公のモードをジャンプ中切り替えている
                    self.hero.vy = jump_power      
                    self.hero_mode = 1
                    hero_img = "hero_jump.png" # ジャンプ中の画像も変更

            self.hero.image = pygame.image.load(hero_img) # 主人公の画像を再度読み込む

            if self.hero.rect.y < hero_Y: # 主人公がジャンプ中は重力が働く
                self.hero.vy += fall
            elif self.hero.rect.y > hero_Y: # 主人公が地面より下に着いたら、主人公を地面の上に戻し再度ジャンプ可能にする
                self.hero.rect.y = hero_Y
                self.hero_mode = 0
                self.hero.vy = 0
            
            # (植物の処理)
            for plant in self.plants: 
                if self.hero.rect.x < plant.rect.x < self.hero.rect.x + self.hero.image.get_width() and plant_count_mode == 0:
                    self.score += 25 # 植物を通り過ぎるとき、1フレームあたり25点
                    self.plant_count_mode = 1
                elif plant.rect.x > self.hero.rect.x and self.plant_count_mode == 1:
                    self.plant_count_mode = 0 # 通り過ぎたらカウント終了
                if pygame.sprite.collide_rect(plant, self.hero): # 衝突したら主人公の画像を切り替えて終了
                    hero_img = "hero_miss.png"
                    self.game_mode = 99
            
            if self.plant_f > self.plant_border: # 植物が配置される間隔まで到達したときの処理
                if s < bird_s:
                    self.plant_border = randint(40,120) # 鳥が飛び始めたら間隔を長めにする
                else:
                    self.plant_border = randint(70, 150)
                if self.f % 900 == 0:
                    self.plant_border = randint(40, 100) # 30秒経ったら間隔を戻す
                self.plants.add(Plant(self.width, hero_Y + randint(-10, 10) , plant_scroll, 0)) # 植物を配置
                self.plant_f = 0 # 植物基準のフレームをリセット
            
            # (鳥の処理)
            for bird in self.birds: # 鳥の処理
                if s > bird_s:
                    if s % 2 == 0: # 毎秒画像を切り替える
                        bird_img = "bird1.png"
                    else:
                        bird_img = "bird2.png"
                    bird.image = pygame.image.load(bird_img)
                if self.hero.rect.x < bird.rect.x < self.hero.rect.x + self.hero.image.get_width() and self.bird_count_mode == 0:
                    self.score += 50 # 鳥を通り過ぎるとき、1フレーム当たり50点
                    self.bird_count_mode = 1
                elif bird.rect.x > self.hero.rect.x :
                    self.bird_count_mode = 0 # 通り過ぎたらカウント終了
                if pygame.sprite.collide_rect(bird, self.hero): # 衝突したら主人公の画像を切り替えて終了
                    hero_img = "hero_miss.png"
                    self.game_mode = 99
            
            if self.bird_f > self.bird_border: # 鳥が配置される間隔まで到達したときの処理
                self.bird_border = randint(50, 100) 
                if self.f % 1200 == 0:
                    self.bird_border = randint(40, 80) #60秒経ったら間隔を短くする
                self.birds.add(Bird(self.width, hero_Y + randint(-125, -10) , randint(-20.0, plant_scroll), 0)) # 鳥を配置
                self.bird_f = 0 # 鳥基準のフレームをリセット
            
            # (的の処理)
            if self.f % 150 == 0 and self.f != 0:
                self.target.vx = randint(-self.target_v,self.target_v) #5秒ごとに的の移動する方向と速度が変化する
                self.target.vy = randint(-self.target_v,self.target_v)
                if f % 450 == 0:
                    self.target_v += 1 # 15秒ごとに的の移動速度の最大を1あげる
            
            if self.f % self.target_change == 0: #20秒ごとに的をランダムな位置に再配置する
                self.target.rect.x = randint(0, self.width - self.target.image.get_width())
                self.target.rect.y = randint(0, self.height - self.target.image.get_height())
                self.target_change = int(self.target_change * 0.9) # 切り替わるまでの間隔を短くする
            
            if self.target.rect.x < 0 or self.target.rect.x + self.target.image.get_width() > self.width:
                self.target.vx *= -1 # ウィンドウの端にあたったら方向転換
            if self.target.rect.y < 0 or self.target.rect.y + self.target.image.get_height() > self.height:
                self.target.vy *= -1
            
            # (壁の処理)
            self.wall_x += wall_move_x # 壁が迫る速度を設定
            self.wall_y += wall_move_y
            if self.target.rect.x <= mouse_xy[0] <= self.target.rect.x + self.target.image.get_width() \
            and self.target.rect.y <= mouse_xy[1] <= self.target.rect.y + self.target.image.get_height(): 
                self.wall_x -= wall_move_x + 1 # カーソルが的のうちにある時は壁を徐々に戻す
                self.wall_y -= wall_move_y +  1
            if self.wall_x > self.width: # ウィンドウの端より先に戻ったらウィンドウの端に合わせる
                self.wall_x = self.width
            if self.wall_y < 0:
                self.wall_y = 0
            
            # (描画の処理)
            self.hero.update() # 各座標の更新
            self.plants.update()
            self.birds.update()
            self.target.update()
            
            pygame.draw.line(self.screen, (0,0,0), (0, hero_Y+42), (self.width, hero_Y+42)) # 地平線

            self.screen.blit(self.hero.image, self.hero.rect) # 主人公を一番上に描画(現時点での)

            pygame.draw.rect(self.screen, (0,0,0), (self.width - self.wall_x, 0, self.width, self.height)) # 横壁の描画
            if s > self.bird_border:
                pygame.draw.rect(self.screen, (0,0,0), (0, 0, self.width, self.wall_y)) # 縦壁の描画
            
            self.screen.blit(self.target.image, self.target.rect) # 的を一番上に描画
            
            text1 = self.font.render("second:" + str(s - 1), True, (0,0,0)) # 秒数とスコアを画面下に描画
            text2 = self.font.render("score:" + str(self.score), True, (0, 0, 0))
            self.screen.blit(text1, [50, self.height - 30])
            self.screen.blit(text2, [200, self.height + -30])

            pygame.display.flip()
            self.screen.fill((255, 255, 255)) # スクリーンの背景を白で更新

            # (プログラム終了処理)
            if self.game_mode == 99: 
                time.sleep(0.5)
                print("score:" + str(self.score)) # コンソールに最終スコアをprint
                sys.exit(0)