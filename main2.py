import pygame, math, time
from data import chemicals
from beaker import Beaker
from ui import Button
from chem_select import data
import subprocess
import sys
#pH更新函數
def pH_update(acid_text,base_text,total_H,total_OH,vol):
    kb = 1.8e-5 
    ka = 1.8e-5
    pKa = -math.log10(ka)
    pKb = -math.log10(kb)
    kw = 1e-14
    pH = None   
    #三種組合
    if acid_text=="HCl" and base_text=="NaOH":
        if vol ==0:
            pH=7
        elif total_H > total_OH:
            pH = -math.log10((total_H - total_OH) / vol)
        elif total_OH > total_H:
            pH = 14 + math.log10((total_OH - total_H) / vol)
        else:
            pH = 7.0
    elif acid_text == "HCl" and base_text == "NH4OH":
        if vol ==0:
            pH=7
        elif total_H > total_OH:
            pH = -math.log10((total_H - total_OH) / vol)
        elif total_OH > total_H: 
            pH = 14+math.log10(math.sqrt(kb * ((total_OH - total_H) / vol)))
        elif total_H==total_OH:
            if total_OH==0:
                pH=7
            else:
                pH = -math.log10(math.sqrt((kw / kb) * total_H / vol))
    elif acid_text == "CH3COOH" and base_text == "NH4OH":
        if vol ==0:
            pH=7
        elif total_H > total_OH:
            if total_OH == 0:
                pH = -math.log10(math.sqrt(ka*(total_H/vol)))
            else:
                pH = pKa + math.log10(total_OH/(total_H - total_OH))
        elif total_OH > total_H:
            if total_H == 0:
                pH = 14+math.log10(math.sqrt(kb*(total_OH/vol)))
            else:
                pOH = pKb + math.log10(total_H /(total_OH - total_H))
                pH = 14 - pOH
        else:
            pH = 7 + 0.5 * (pKa - pKb)
    
    if pH < 0: pH = 0
    if pH > 14: pH = 14

    return pH
#畫面更新函數
def update_system():
    global pH
    total_H = sum(beaker.contents_mole.get(n, 0) * chemicals[n]['H+'] for n in chemicals)
    total_OH = sum(beaker.contents_mole.get(n, 0) * chemicals[n]['OH-'] for n in chemicals)
    vol= max(beaker.volume, 0.0001)
    pH = pH_update(acid_text, base_text, total_H, total_OH, vol)

pygame.init()
acids =["HCl","CH3COOH"]
bases = ["NH4OH","NaOH"]
indicators = ["Methyl Orange","Phenolphthalein","Bromothymol Blue","Methyl Red","Thymol Blue","Phenol Red"]
acid_num,base_num,indicator_num = data()
acid_text = acids[acid_num]
base_text = bases[base_num] 


##畫面設定
##畫面參數
WIDTH, HEIGHT =650, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("酸鹼滴定虛擬實驗室")

##載入圖片 
beaker_img = pygame.image.load("OH_H/images/beaker.png").convert_alpha()
burette_img = pygame.image.load("OH_H/images/burette.png").convert_alpha()

##物件建立
#建立燒杯
mechine_x = 290
beaker = Beaker(mechine_x, 400)
#建立按鈕
add_acid_btn = Button(f"drop {acid_text}",50, 130, (255, 100, 100),"rect","left",150,border=10)
add_base_btn = Button(f"drop {base_text}",50, 180, (100, 100, 255),"rect","left",150,border=10)
reset_btn = Button("Reset", 47, 372, (250, 0, 0),width=60,border=10)
Quit_btn = Button("<Back to menu",10,10,(100,100,100),"rect",width=150,border=10)#時間
time_start = time.time()
time_coordinate = (155,370)

##參數設定
#字體
font = pygame.font.SysFont("Arial", 18,bold=True)
font_mid = pygame.font.SysFont(None, 24)
font_big = pygame.font.SysFont("Arial", 49)
clock = pygame.time.Clock()
pH = 7.0 
vol=0
#滴定動畫變數
drop_y = 250
drop_pos = [burette_img.get_width()//2 + mechine_x, drop_y]
drop_active = False
current_chemical = None
drop_speed = 30 
burette_liquid_height = 0
drop_color = (0,0,255)
# pH曲線變數
ph_history = []
graph_rect= pygame.Rect(47, 250, 160, 120)


running = True
while running:
    screen.fill((230, 230, 230))
    ###左側按鈕區
    ##按鈕區背景
    pygame.draw.rect(screen, (100,100,100),(0,0,250,670))
    pygame.draw.rect(screen, (255,255,255),(3,3,244,670))
    ##按鈕
    for btn in [add_acid_btn, add_base_btn, reset_btn,Quit_btn]:
        btn.update()
        btn.draw(screen, font)
    ##酸鹼指示劑文字
    screen.blit(font.render(f"Indicator :",True, (0, 0, 0)),(30,480))
    pygame.draw.line(screen,(210,210,210),(90,523),(230,523),2)
    screen.blit(font.render(f"{indicators[indicator_num]}",True, (41, 128, 185)),(93,505))
    ##pH曲線圖
    pygame.draw.rect(screen, (240, 240, 240), graph_rect)
    pygame.draw.rect(screen, (0, 0, 0), graph_rect, 1)
    pygame.draw.line(screen, (200, 200, 200), (graph_rect.left, graph_rect.centery), (graph_rect.right, graph_rect.centery), 1)
    if len(ph_history) > 1:
        points = []
        for i, val in enumerate(ph_history[-40:]):
            x = graph_rect.left + (i * (graph_rect.width / 40))
            y = graph_rect.bottom - (val * (graph_rect.height / 14))
            points.append((x, y))
        pygame.draw.lines(screen, (255, 0, 0), False, points, 2)
    screen.blit(font.render("pH Curve:", True, (50, 50, 50)), (graph_rect.x-15,graph_rect.y-25))
    #時間
    time_elapsed = time.time() - time_start
    screen.blit(font.render(f"Time: {int(time_elapsed)} s", True, (0, 0, 0)),time_coordinate)

    ###右側數值區
    ##物質加入量
    #背景
    pygame.draw.rect(screen, (250,250,250),(460,150,180,150),border_radius=15)
    pygame.draw.rect(screen, (200,200,200),(460,150,180,40),border_top_left_radius=15,border_top_right_radius=15)
    pygame.draw.rect(screen, (100,100,100),(460,150,180,150),width=4,border_radius=15)
    screen.blit(font.render("Titration Data", True, (0, 0, 0)), (500, 163))
    y_offset = 200
    screen.blit(font.render(acid_text, True, (0, 0, 0)), (480, y_offset))
    screen.blit(font.render(f"{beaker.contents_vol.get(acid_text, 0):<4.1f}", True, (0, 0, 0)), (554, y_offset))
    screen.blit(font.render("mL", True, (0, 0, 0)), (590, y_offset))
    y_offset += 30      
    screen.blit(font.render(base_text, True, (0, 0, 0)), (480, y_offset))
    screen.blit(font.render(f"{beaker.contents_vol.get(base_text, 0):<4.1f}", True, (0, 0, 0)), (554, y_offset))
    screen.blit(font.render("mL", True, (0, 0, 0)), (590, y_offset))
    y_offset += 30     
    pygame.draw.rect(screen, (150, 150, 150),(470,y_offset,160,4),border_radius=10)
    y_offset += 10
    screen.blit(font.render(f"Total", True, (0, 0, 0)), (480, y_offset))
    screen.blit(font.render(f"{vol:.1f}", True, (0, 0, 0)), (554, y_offset))
    screen.blit(font.render("mL", True, (0, 0, 0)), (590, y_offset))
    
    ##ph值
    #背景
    pygame.draw.rect(screen, (250,250,250),(460,360,180,150),border_radius=15)
    pygame.draw.rect(screen, (200,200,200),(460,360,180,40),border_top_left_radius=15,border_top_right_radius=15)
    pygame.draw.rect(screen, (100,100,100),(460,360,180,150),width=4,border_radius=15)
    screen.blit(font.render("      pH Data", True, (0, 0, 0)), (500, 373))
    #刻度
    x_st = 480
    y_st = 480
    pygame.draw.line(screen,(0,0,0),(x_st,y_st),(x_st+130,y_st),2)
    for i in range(13):
        if i==0 or i==7:
            pygame.draw.line(screen,(0,0,0),(x_st,y_st),(x_st,y_st-10),2)
            screen.blit(font.render(str(i),True, (0, 0, 0)),(x_st-4,y_st+4))
        else:
            pygame.draw.line(screen,(0,0,0),(x_st,y_st),(x_st,y_st-5),2)      
        
        x_st+=10
    pygame.draw.line(screen,(0,0,0),(x_st,y_st),(x_st,y_st-10),2)
    screen.blit(font.render(str(14),True, (0, 0, 0)),(x_st,y_st+4))
    #ph值
    screen.blit(font.render(f"pH={pH:.2f}",True, (0,0,0)),(480,410))
    #箭頭
    x_st = 480
    screen.blit(font_big.render("ˇ",True, (0, 0, 0)),(x_st-1+(130*(pH/14)),(y_st-35)))


    ###中間反應區
    ##滴定管
    screen.blit(burette_img, (mechine_x-3, 150))
    ##燒杯
    beaker.draw(screen, beaker_img)
    ##已滿標示
    if beaker.volume >= beaker.max_volume:
        screen.blit(font_big.render("Full", True, (255, 0, 0)), (mechine_x+17, HEIGHT-295))
    ##滴定動畫
    if drop_active:
        if current_chemical in ["HCl","CH3COOH"]:
            drop_color = (255, 0, 0)
        elif current_chemical in ["NaOH", "NH4OH"]:
            drop_color = (0, 0, 255)
        
        pygame.draw.circle(screen, drop_color, (int(drop_pos[0]), int(drop_pos[1])), 5)
        drop_pos[1] += drop_speed
        
        if drop_pos[1] >= 480: 
            beaker.add_chemical(current_chemical,5)
            vol += 5
            update_system()
            ph_history.append(pH)
            drop_pos[1] = drop_y
            drop_active = False
            
    ###事件偵測
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for b in [Quit_btn,add_acid_btn,add_base_btn,reset_btn]:
                    b.touched = b.rect.collidepoint(pos)

        if add_acid_btn.is_clicked(event):
            if beaker.volume < beaker.max_volume:
                current_chemical = acid_text
                drop_active = True
                beaker.update_color(pH,indicators[indicator_num])
        if add_base_btn.is_clicked(event):
            if beaker.volume < beaker.max_volume:
                current_chemical = base_text
                drop_active = True     
                beaker.update_color(pH,indicators[indicator_num])
            beaker.update_color(pH,indicators[indicator_num])
        if reset_btn.is_clicked(event):
            beaker = Beaker(mechine_x, 400)
            beaker.color = (173, 216, 230)
            indicator_num=0
            pH = 7.0
            ph_history = []
            time_start = time.time()
            beaker.update_color(pH,indicators[indicator_num])
            vol=0
        if Quit_btn.is_clicked(event):
            subprocess.Popen([sys.executable ,"menu.py"])
            running = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()