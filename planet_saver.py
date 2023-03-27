import random
import pygame as pg
import os
from pygame import mixer
pg.init()
shot=mixer.Sound("Assets/shot.mp3")
bombed=mixer.Sound("Assets/bombed.mp3")
songs=[mixer.Sound("Assets/song1.mp3"),mixer.Sound("Assets/song2.mp3"),mixer.Sound("Assets/song3.mp3")]


YSPEED=6
RSPEED=2

WIDTH,HEIGHT =900,500
WIN=pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Planet Saver")
WHITE=(255,255,255)
BLACK=(0,0,0)
FPS=60

FONT= pg.font.Font('freesansbold.ttf', 32)


SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40
BULLET_WIDTH,BULLET_HEIGHT=2,4
bg_img=pg.image.load(os.path.join('Assets','space.png'))
BG=pg.transform.scale(bg_img,(WIDTH,HEIGHT))
YELLOW_SPACESHIP_IMAGE=pg.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP=pg.transform.rotate(pg.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),180)
RED_SPACESHIP_IMAGE=pg.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP=pg.transform.rotate(pg.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),0)
BULLET=pg.image.load(os.path.join('Assets','bullet.png'))

def draw_window(bg,reds,yellow,bullets,score,lvl):
    WIN.blit(bg,(0,0))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    for red in reds:
        WIN.blit(RED_SPACESHIP, (red.x, red.y))
    SCORE_LVL = FONT.render('Score: ' + str(score) + '  LVL: ' + str(lvl), True, BLACK, WHITE)
    SCORE_BOX = SCORE_LVL.get_rect()
    WIN.blit(SCORE_LVL,SCORE_BOX)
    for bul in bullets:
        WIN.blit(BULLET,(bul.x,bul.y))
    pg.display.update()
def handle_bul(bullets,reds,score):
    i=0
    while i<len(bullets):
        if bullets[i].y>=0:
            bullets[i].y-=4
            j=0
            while j<len(reds):
                red=reds[j]
                if (red.y>=bullets[i].y-20 and red.y<=bullets[i].y+20) and ( red.x>=bullets[i].x-40 and red.x<=bullets[i].x+20):
                    
                    reds.pop(j)
                    bullets.pop(i)
                    i-=1
                    j-=1
                    bombed.play()
                    score+=3
                if (len(bullets)==0): break
                j+=1


        else:
            bullets.pop(i)
            i-=1

        i += 1
    return score


def main():
    songs[0].play()
    reds=[]
    yellow = pg.Rect(WIDTH/2-SPACESHIP_WIDTH/2, HEIGHT-SPACESHIP_HEIGHT-10, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    score=2
    lvl=1
    
    avlbl_locs=[i for i in range(0, WIDTH - SPACESHIP_WIDTH - 10,SPACESHIP_WIDTH) if i not in [red.x for red in reds]]
    
    for i in range(lvl):
        new_loc=random.choice(avlbl_locs)
        reds.append(pg.Rect(new_loc, 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        avlbl_locs.remove(new_loc)
    bullets=[]
    clock=pg.time.Clock()
    run=True
    lost=False
    while run:
        if len(reds)<lvl:
            reds.append(pg.Rect(random.randint(0, WIDTH - SPACESHIP_WIDTH - 10), 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        elif len(reds)>lvl:
            reds=reds[0:lvl]
        replay=False

        clock.tick(FPS)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    if score > 0 and not lost:
                        
                        bullet=pg.Rect(yellow.x,yellow.y,5,5)
                        bullets.append(bullet)
                        shot.play()
                        score-=1
                if event.key == pg.K_r:
                    replay = True

        draw_window(BG,reds,yellow,bullets,score,lvl)

        if all([red.y<HEIGHT-2*SPACESHIP_HEIGHT+5 for red in reds])   :
            lost=False
            key_pressed=pg.key.get_pressed()
            if yellow.x>0 and key_pressed[pg.K_LEFT]:

               yellow.x-=YSPEED
            elif yellow.x < WIDTH - SPACESHIP_WIDTH and key_pressed[pg.K_RIGHT]:

                yellow.x+=YSPEED
            if len(bullets)>0:

                score=handle_bul(bullets,reds,score)



                templvl=(score//10)+1
                if templvl>lvl:
                    lvl=templvl
                    



            for red in reds: red.y+=RSPEED

        else:
            if replay :
                bullets.clear()
                for red in reds: red.y=0
                for red in reds: red.x=random.randint(0, WIDTH - SPACESHIP_WIDTH - 10)
                score=2
                lvl=1
            lost=True

    pg.quit()

if __name__ =="__main__":
    main()