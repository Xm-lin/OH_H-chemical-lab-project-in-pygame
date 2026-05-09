import sys
import pygame
from ui import Button

def point_in_triangle(pt, tri):
    (x1, y1), (x2, y2), (x3, y3) = tri

    def sign(p1, p2, p3):
        return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])

    b1 = sign(pt, (x1,y1), (x2,y2)) < 0.0
    b2 = sign(pt, (x2,y2), (x3,y3)) < 0.0
    b3 = sign(pt, (x3,y3), (x1,y1)) < 0.0

    return (b1 == b2) and (b2 == b3)

pygame.init()
WIDTH = 300
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Select your chemicals")
font = pygame.font.SysFont(None, 24)

# 建立按鈕
left_x=90
right_x=200
Buttons = [
    Button("acid_left",left_x,100,(220,0,0),"triangle"),
    Button("acid_right",right_x,100,(220,0,0),"triangle","right"),
    Button("base_left",left_x,180,(0,0,220),"triangle"),
    Button("base_right",right_x,180,(0,0,220),"triangle","right"),
    Button("indicator_left",left_x-30,260,(255,0,220),"triangle"),
    Button("indicator_right",right_x+30,260,(255,0,220),"triangle","right"),
    Button("Confirm",85,320,(100,100,100),"rect",width=120,height=40,border=50),
]


# 酸鹼數字
acid_num = 0
base_num = 0
indicator_num = 2
acids =["HCl","CH3COOH"]
bases = ["NH4OH","NaOH"]
indicators = ["Methyl Orange","Phenolphthalein","Bromothymol Blue","Methyl Red","Thymol Blue","Phenol Red"]

def data():
    return acid_num,base_num,indicator_num

# 顯示區
acid_text = pygame.Rect(95,90,100,40)
base_text = pygame.Rect(95,170,100,40)
indicator_text = pygame.Rect(66,250,160,40)

running = True
while running:
    screen.fill((200,200,200))

    # 顯示酸鹼數字框
    pygame.draw.rect(screen,(255,255,255),acid_text,border_bottom_left_radius=80,border_top_left_radius=80,border_bottom_right_radius=100,border_top_right_radius=100)
    pygame.draw.rect(screen,(255,255,255),base_text,border_bottom_left_radius=80,border_top_left_radius=80,border_bottom_right_radius=100,border_top_right_radius=100)
    pygame.draw.rect(screen,(255,255,255),indicator_text,border_bottom_left_radius=80,border_top_left_radius=80,border_bottom_right_radius=100,border_top_right_radius=100)
    choose_chemical = font.render(f"Choose acid, base, indicator:",True,(0,0,0))
    choose_acid = font.render(f"Acid:",True,(0,0,0))
    choose_base = font.render(f"Base:",True,(0,0,0))
    choose_indicator = font.render(f"Indecator:",True,(0,0,0))    
    acid_surface = font.render(f"{acids[acid_num]:}",True,(0,0,0))
    base_surface = font.render(f"{bases[base_num]:}",True,(0,0,0))
    indicator_surface = font.render(f"{indicators[indicator_num]:}",True,(0,0,0))

    screen.blit(choose_chemical,(10,20))
    screen.blit(choose_acid,(acid_text.x-80,acid_text.y-25))
    screen.blit(choose_base,(base_text.x-80,base_text.y-25))
    screen.blit(choose_indicator,(indicator_text.x-50,indicator_text.y-25))
    screen.blit(acid_surface,(acid_text.x+7,acid_text.y+13))
    screen.blit(base_surface,(base_text.x+7,base_text.y+13))
    screen.blit(indicator_surface,(indicator_text.x+7,indicator_text.y+13))

    # 畫按鈕
    for b in Buttons:
        b.draw(screen,font)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # 滑鼠移動
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for b in Buttons:
                if b.shape == "triangle":
                    b.touched = point_in_triangle(pos, b.coordinate)
                else:
                    b.touched = b.rect.collidepoint(pos)

        # 滑鼠按下，判斷點擊
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in Buttons:
                if b.is_clicked(event):
                    # 酸按鈕
                    if b.text == "acid_left":
                        acid_num = acid_num-1
                        if acid_num==-1:acid_num=1           
                    elif b.text == "acid_right":
                        acid_num = acid_num+1
                        if acid_num==2:acid_num=0
                    
                    if acid_num==1:
                        base_num=0

                    # 鹼按鈕
                    if b.text == "base_left":
                        base_num = base_num-1
                        if base_num==-1:base_num=1
                        if acid_num==1:base_num=0
                    if b.text == "base_right":
                        base_num = base_num+1
                        if base_num==2:base_num=0
                        if acid_num==1:base_num=0

                    #指示劑按鈕
                    if b.text == "indicator_left":
                        indicator_num-=1
                        if indicator_num==0:
                            indicator_num=5
                    if b.text == "indicator_right":
                        indicator_num+=1
                        if indicator_num==5:
                            indicator_num=0
                    #確認按鈕
                    if b.text == "Confirm":                     
                        running=False

    pygame.display.flip()

pygame.quit()
