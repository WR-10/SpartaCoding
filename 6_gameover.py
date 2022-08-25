import os
import  pygame
###########################################################################################
# 기본초기화 (반드시 해야하는 것들)
pygame.init()

# 화면크기
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀
pygame.display.set_caption("ballgame")

#fps
clock = pygame.time.Clock()
###########################################################################################

# 1. 사용자 게임 초기화

  



current_path = os.path.dirname(__file__) 
img_path = os.path.join(current_path,'images') 

background = pygame.image.load(os.path.join(img_path, "background.png"))



stage = pygame.image.load(os.path.join(img_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]



character = pygame.image.load(os.path.join(img_path, "character.png"))
charater_size = character.get_rect().size
character_width = charater_size[0]
character_height = charater_size[1]
character_x = (screen_width/2) - (character_width/2)
character_y = screen_height - character_height - stage_height
character_speed = 0.6


character_to_x_left = 0
character_to_x_right = 0

#무기 생성
weapon = pygame.image.load(os.path.join(img_path,'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#여러 번의 발사 가능
weapons = []

#무기 이동 속도
weapon_speed = 10



#공 만들기
ball_imgs = [
    pygame.image.load(os.path.join(img_path,'ball1.png')),
    pygame.image.load(os.path.join(img_path,'ball2.png')),
    pygame.image.load(os.path.join(img_path,'ball3.png')),
    pygame.image.load(os.path.join(img_path,'ball4.png'))]



# 공 크기에 따른 스피드
ball_speed_y = [-18, -15, -12, -9]



#공들
balls = []


# 최초 발생하는 큰공추가
balls.append({
    'pos_x' : 50, 
    'pos_y' : 50, 
    'img_idx' : 0, 
    'to_x' : 3, 
    'to_y' : -6, 
    'init_spd_y' : ball_speed_y[0] }) 


#사라질 무기, 사라질 공 정보
weapon_to_remove = -1
ball_to_remove = -1



# 폰트 선언
game_font = pygame.font.Font(None, 40)
total_time =100
start_ticks = pygame.time.get_ticks()


game_result = "Game Over"


running = True # 게임이 진행중인지 확인
while running:
    dt = clock.tick(30) 

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_left -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x_right += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x = character_x + (character_width / 2) - (weapon_width / 2)
                weapon_y = character_y
                weapons.append([weapon_x,weapon_y])



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                character_to_x_right=0
            elif event.key == pygame.K_LEFT:
                character_to_x_left= 0
    
    # 3. 게임 캐릭터 위치 정의
    character_x += (character_to_x_right + character_to_x_left) * dt

    if character_x < 0:
        character_x = 0
    elif character_x >= screen_width - character_width:
        character_x = screen_width - character_width

    #무기 위치 조정
    weapons = [[w[0],w[1] - weapon_speed] for w in weapons] #위로 조정


    #천장에 닿은 무기 제거
    weapons = [[w[0],w[1]] for w in weapons if w[1] > 0]


    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val["img_idx"]


        ball_size = ball_imgs[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]


        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val['to_x'] = ball_val['to_x'] * -1

         #세로 위치
         #스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val['to_y'] = ball_val['init_spd_y']
        else: 
            ball_val['to_y'] += 0.5

        ball_val['pos_x'] += ball_val['to_x']
        ball_val['pos_y'] += ball_val['to_y']


    # 4. 충돌 처리


    #캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x
    character_rect.top = character_y


    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val["img_idx"]


        #공 rect정보 
        ball_rect = ball_imgs[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y


        #공과 캐릭터 충돌처리
        if character_rect.colliderect(ball_rect):
            running = False
            break
        
        #공과 무기들 충돌처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x = weapon_val[0]
            weapon_y = weapon_val[1]
        
            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x
            weapon_rect.top = weapon_y
            
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx 
                ball_to_remove = ball_idx

                
                if ball_img_idx < 3:
                    
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 
                    small_ball_rect = ball_imgs[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #왼쪽으로 튕겨나 가는 공
                    balls.append({
                        'pos_x' : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        'pos_y' : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), 
                        'img_idx' : ball_img_idx + 1, 
                        'to_x' : - 3, 
                        'to_y' : - 6, 
                        'init_spd_y' : ball_speed_y[ball_img_idx + 1]
                    })
                    #오른쪽으로 튕겨나 가는 공
                    balls.append({
                        'pos_x' : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), 
                        'pos_y' : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), 
                        'img_idx' : ball_img_idx + 1, 
                        'to_x' : 3, 
                        'to_y' : -6, 
                        'init_spd_y' : ball_speed_y[ball_img_idx + 1]
                    })

                break
        else: 
            continue 
        break #



    #충돌된 공 or 무기 없애기
    if ball_to_remove>-1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove>-1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    #모든 공 없앤 경우 게임 종료
    if len(balls) == 0:
        game_result = 'Mission Complete!'
        running = False


    # 5. 화면에 그리기
    screen.blit(background,(0,0))
    

    for weapon_x, weapon_y in weapons:
        screen.blit(weapon,(weapon_x,weapon_y))


    for idx,val in enumerate(balls):
        ball_pos_x = val['pos_x']
        ball_pos_y = val['pos_y']
        ball_img_idx = val['img_idx']
        screen.blit(ball_imgs[ball_img_idx],(ball_pos_x,ball_pos_y))


    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x,character_y))
  
   #경과시간
    elapse_time = (pygame.time.get_ticks()-start_ticks) / 1000
    timer = game_font.render("Time : {} ".format(int(total_time-elapse_time)),True, (255,255,255))
    screen.blit(timer,(10,10))

    #시간초과

    if total_time-elapse_time <= 0:
        game_result = 'Time Out'
        running = False

    pygame.display.update()

#게임오버 메시지
msg = game_font.render(game_result ,True, (255,255,0))
msg_rect = msg.get_rect(center = (int(screen_width/2),int(screen_height/2)))

screen.blit(msg, msg_rect)

pygame.display.update() 

#2초 대기
pygame.time.delay(2000)

pygame.quit()