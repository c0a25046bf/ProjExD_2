import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),# 上
    pg.K_DOWN: (0, +5),# 下
    pg.K_LEFT: (-5, 0),# 左
    pg.K_RIGHT: (+5, 0),# 右
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface,) -> None:
    dd_img =pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(dd_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    dd_img.set_alpha(150)
    
    font = pg.font.Font(None, 150)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = WIDTH // 2, HEIGHT // 2


    kk_img = pg.image.load("fig/8.png")

    screen.blit(dd_img, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(kk_img, (text_rect.centerx - 370, text_rect.centery - 50))
    screen.blit(kk_img, (text_rect.centerx + 370, text_rect.centery - 50))

    pg.display.update()
    time.sleep(5)  # 5秒待機

# --- 変更点1: get_kk_imgs関数の実装 ---
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量タプルと対応する画像Surfaceの辞書を返す
    """
    # 基本となる右向き画像（0.9倍）をロード
    img_r = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    # 左向き画像を作成（右向きを左右反転）
    img_l = pg.transform.flip(img_r, True, False)
    
    # 全方向の画像を回転させて辞書に格納
    kk_dict = {
        ( 0,  0): img_r,                                      # キー押下がない場合
        (+5,  0): img_r,                                      # 右
        (+5, -5): pg.transform.rotozoom(img_r, 45, 1.0),      # 右上
        ( 0, -5): pg.transform.rotozoom(img_r, 90, 1.0),      # 上
        (-5, -5): pg.transform.rotozoom(img_l, -45, 1.0),     # 左上（反転画像を回転）
        (-5,  0): img_l,                                      # 左（反転画像）
        (-5, +5): pg.transform.rotozoom(img_l, 45, 1.0),      # 左下（反転画像を回転）
        ( 0, +5): pg.transform.rotozoom(img_r, -90, 1.0),     # 下
        (+5, +5): pg.transform.rotozoom(img_r, -45, 1.0),     # 右下
    }
    return kk_dict
# -----------------------------------

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    
    # --- 変更点2: 画像辞書の取得と初期画像の設定 ---
    # `kk_dict`を直接返す関数を呼び出し、辞書を受け取る
    kk_imgs = get_kk_imgs() 
    # 初期画像（停止時）を取得してrectを作成
    kk_img = kk_imgs[(0, 0)] 
    # -----------------------------------------------

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +1, +1

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return
        screen.blit(bg_img, [0, 0]) 
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, mv in DELTA.items():
            if key_lst[k]: 
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # --- 変更点3: 合計移動量をキーにして向きを変えた画像を取得 ---
        # 8方向（または停止）の移動量をタプルにしてキーとし、対応する画像を取得
        kk_img = kk_imgs[tuple(sum_mv)] 
        # -----------------------------------------------------------

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: 
            vx *= -1
        if not tate:
            vy *= -1


        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
