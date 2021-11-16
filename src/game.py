from pygame.image import load
from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from src.option import *
from db.db_interface import InterfDB
from src.store import store
from src.pvp import *
import src.pvp
db = InterfDB("db/score.db")


# 시작 화면
def intro_screen():
    global resized_screen

    # temp_dino를 전역변수로 설정합니다.
    global temp_dino
    global type_idx
    global dino_type
    dino_type = ['ORIGINAL', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'PURPLE', 'BLACK', 'PINK']
    type_idx = 0
    click_count = 0
    #
    temp_dino = Dino(dino_size[0], dino_size[1])
    temp_dino.is_blinking = True
    game_start = False

    # 이미지 로드
    # 배경 이미지
    background, background_rect = load_image('coin_t_rex.png', width, height)
    # 버튼 이미지
    r_btn_1p, r_btn_1p_rect = load_image(*resize('btn_1p.png', 150, 60, -1))
    btn_1p, btn_1p_rect = load_image('btn_1p.png', 150, 60, -1)
    r_btn_2p, r_btn_2p_rect = load_image(*resize('btn_2p.png', 150, 60, -1))
    btn_2p, btn_2p_rect = load_image('btn_2p.png', 150, 60, -1)
    r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 150, 60, -1))
    btn_board, btn_board_rect = load_image('btn_board.png', 150, 60, -1)
    r_btn_option, r_btn_option_rect = load_image(*resize('btn_option.png', 150, 60, -1))
    btn_option, btn_option_rect = load_image('btn_option.png', 150, 60, -1)


    # DINO IMAGE
    while not game_start:
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE and not full_screen:
                    #민주 -> 필요없어보여서 주석처리
                    # r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('btn_start.png', 150, 50, -1))
                    # btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 150, 50, -1)
                    # r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 150, 50, -1))
                    # btn_board, btn_board_rect = load_image('btn_board.png', 150, 50, -1)
                    # r_btn_option, r_btn_option_rect = load_image(*resize('btn_option.png', 150, 50, -1))
                    # btn_option, btn_option_rect = load_image('btn_option.png', 150, 50, -1)
                    # IMGPOS
                    # BACKGROUND IMG POS
                    background_rect.bottomleft = (width * 0, height)
                if event.type == pygame.QUIT:
                    game_start = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                # 버튼 클릭했을 때 event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        # 1player game button
                        if r_btn_1p_rect.collidepoint(x, y):
                            #temp_dino.is_jumping = True
                            #temp_dino.is_blinking = False
                            temp_dino.movement[1] = -1 * temp_dino.jump_speed
                            game_start = True
                            select_mode()
                        # 2player game button
                        if r_btn_2p_rect.collidepoint(x, y):
                            pvp()
                        # board button
                        if r_btn_board_rect.collidepoint(x, y):
                            board()
                        # option button
                        if r_btn_option_rect.collidepoint(x, y):
                            option()

                        # temp_dino를 누르는 경우:
                        # if temp_dino.rect.collidepoint(x, y):
                        #     click_count += 1
                        #     type_idx = click_count % len(dino_type)
                        #     temp_dino = Dino(dino_size[0], dino_size[1], type=dino_type[type_idx])
                        #     temp_dino.is_blinking = True

        temp_dino.update()

        # interface draw
        if pygame.display.get_surface() is not None:
            r_btn_1p_rect.centerx = resized_screen.get_width() * 0.8
            r_btn_2p_rect.centerx = resized_screen.get_width() * 0.8
            r_btn_board_rect.centerx =  resized_screen.get_width() * 0.8
            r_btn_option_rect.centerx = resized_screen.get_width() * 0.8
            r_btn_1p_rect.centery = resized_screen.get_height() * 0.25
            r_btn_2p_rect.centery = resized_screen.get_height() * (0.25 + 0.75 * button_offset)
            r_btn_board_rect.centery = resized_screen.get_height() * (0.25 + 1.5 * button_offset)
            r_btn_option_rect.centery = resized_screen.get_height() * (0.25+ 2.25 * button_offset)

            screen.blit(background, background_rect)
            disp_intro_buttons(btn_1p, btn_2p, btn_board, btn_option)

            # temp_dino.draw()
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                                        resized_screen_center)

            pygame.display.update()

        clock.tick(FPS)

        # if temp_dino.is_jumping == False and temp_dino.is_blinking == False:
        #     game_start = True
        #     select_mode()

    pygame.quit()
    quit()


# 게임 작동
def gameplay_easy():
    global resized_screen
    global high_score
    result = db.query_db("select score from easy_mode order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    if bgm_on:
        pygame.mixer.music.play(-1) # 배경음악 실행
    game_speed = 4
    start_menu = False
    game_over = False
    game_quit = False
    # 게임 후 버튼
    r_btn_restart, r_btn_restart_rect = load_image(*resize('btn_restart.png', 150, 80, -1))
    btn_restart, btn_restart_rect = load_image('btn_restart.png', 150, 80, -1)
    r_btn_save, r_btn_save_rect = load_image(*resize('btn_save.png', 150, 80, -1))
    btn_save, btn_save_rect = load_image('btn_save.png', 150, 80, -1)
    r_btn_exit, r_btn_exit_rect = load_image(*resize('btn_exit.png', 150, 80, -1))
    btn_exit, btn_exit_rect = load_image('btn_exit.png', 150, 80, -1)

    ###
    life = 5
    ###
    paused = False

    player_dino = Dino(dino_size[0], dino_size[1], type=dino_type[type_idx])

    new_ground = Ground(-1 * game_speed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    heart = HeartIndicator(life)
    speed_indicator = Scoreboard(width * 0.12, height * 0.15)
    counter = 0
    speed_text = font.render("SPEED", True, black)
    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    # add stones
    stones = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    # highjump_items = pygame.sprite.Group()

    Stone.containers = stones
    Cactus.containers = cacti
    FireCactus.containers = fire_cacti  # fire_Cactus => FireCactus
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    # HighJumpItem.containers = highjump_items

    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    game_over_image, game_over_rect = load_image('game_over.png', 380, 100, -1)
    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(15 * 6 / 5), -1)
    my_font = pygame.font.Font('DungGeunMo.ttf', 30)
    high_image = my_font.render('HI', True, black)
    high_rect = high_image.get_rect()
    high_rect.top = height * 0.15
    high_rect.left = width * 0.73

    while not game_quit:
        while start_menu:
            pass
        while not game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 종료
                        game_quit = True
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player_dino.rect.bottom == int(0.98 * height):
                                player_dino.is_jumping = True
                                if pygame.mixer.get_init() is not None:
                                    jump_sound.play()
                                player_dino.movement[1] = -1 * player_dino.jump_speed
                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (player_dino.is_jumping and player_dino.is_dead):
                                player_dino.is_ducking = True
                        if event.key == pygame.K_ESCAPE: #ESC = 일시정지
                            paused = not paused
                            paused = pausing()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            player_dino.is_ducking = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and player_dino.rect.bottom == int(0.98 * height):
                            # (mouse left button, wheel button, mouse right button)
                            player_dino.is_jumping = True
                            if pygame.mixer.get_init() is not None:
                                jump_sound.play()
                            player_dino.movement[1] = -1 * player_dino.jump_speed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (player_dino.is_jumping and player_dino.is_dead):
                                player_dino.is_ducking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        player_dino.is_ducking = False

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            if not paused:
                for s in stones:
                    s.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, s):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                for c in cacti:
                    c.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, c):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, f):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, p):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False
                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                if not player_dino.is_super:
                    for s in shield_items:
                        s.movement[0] = -1 * game_speed
                        if pygame.sprite.collide_mask(player_dino, s):
                            if pygame.mixer.get_init() is not None:
                                check_point_sound.play()
                            player_dino.collision_immune = True
                            player_dino.is_super = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()

                STONE_INTERVAL = 50
                CACTUS_INTERVAL = 50
                PTERA_INTERVAL = 300
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 500
                LIFE_INTERVAL = 1000
                SLOW_INTERVAL = 1000
                HIGHJUMP_INTERVAL = 300
                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                if len(cacti) < 2:
                    if len(cacti) == 0:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))

                if len(fire_cacti) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(FireCactus(game_speed, object_size[0], object_size[1]))

                if len(stones) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 3) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Stone(game_speed, object_size[0], object_size[1]))

                if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(game_speed, ptera_size[0], ptera_size[1]))

                if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                    Cloud(width, random.randrange(height / 5, height / 2))

                player_dino.update()
                cacti.update()
                fire_cacti.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                # highjump_items.update()
                new_ground.update()
                scb.update(player_dino.score)
                highsc.update(high_score)
                speed_indicator.update(game_speed - 3)
                heart.update(life)
                slow_items.update()

                stones.update()

                if pygame.display.get_surface() is not None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    speed_indicator.draw()
                    screen.blit(speed_text, (width * 0.01, height * 0.15))
                    heart.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(high_image, high_rect)
                    cacti.draw(screen)
                    stones.draw(screen)
                    fire_cacti.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    # highjump_items.draw(screen)
                    player_dino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_center)
                    pygame.display.update()
                clock.tick(FPS)

                if player_dino.is_dead:
                    game_over = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if player_dino.score > high_score:
                        high_score = player_dino.score

                if counter % speed_up_limit == speed_up_limit - 1:
                    new_ground.speed -= 1
                    game_speed += 1

                counter = (counter + 1)

        if game_quit:
            break

        while game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_quit = True
                            game_over = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            game_over = False
                            game_quit = True
                            type_score(player_dino.score)
                            if not db.is_limit_data(player_dino.score, mode="easy"):
                                db.query_db(
                                    f"insert into easy_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                                db.commit()
                                board("easy")
                            else:
                                board("easy")

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # game_over = True
                        # game_quit = False
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            x, y = event.pos
                            if r_btn_restart_rect.collidepoint(x, y):
                                select_mode()

                            if r_btn_save_rect.collidepoint(x, y):
                                type_score(player_dino.score)
                                if not db.is_limit_data(player_dino.score, mode="easy"):
                                    db.query_db(
                                        f"insert into easy_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                                    db.commit()
                                    board("easy")
                                else:
                                    board("easy")
                            if r_btn_exit_rect.collidepoint(x, y):
                                intro_screen()
                        # type_score(player_dino.score)
                        # if not db.is_limit_data(player_dino.score):
                        #     db.query_db(
                        #         f"insert into user(username, score) values ('{gamer_name}', '{player_dino.score}');")
                        #     db.commit()
                        #     board()
                        # else:
                        #     board()

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)
                r_btn_restart_rect.centerx, r_btn_restart_rect.centery = resized_screen.get_width() * 0.25, resized_screen.get_height() * 0.6
                r_btn_save_rect.centerx, r_btn_save_rect.centery = resized_screen.get_width() * 0.5, resized_screen.get_height() * 0.6
                r_btn_exit_rect.centerx, r_btn_exit_rect.centery = resized_screen.get_width() * 0.75, resized_screen.get_height() * 0.6
                disp_gameover_buttons(btn_restart, btn_save, btn_exit)

                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            if pygame.display.get_surface() is not None:
                disp_gameover_msg(game_over_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(high_image, high_rect)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


def gameplay_hard():
    global resized_screen
    global high_score
    result = db.query_db("select score from hard_mode order by score desc;", one=True)
    if result is not None:
        high_score = result['score']

    # HERE: REMOVE SOUND!!
    if bgm_on:
        pygame.mixer.music.play(-1)  # 배경음악 실행

    game_speed = 4
    start_menu = False
    game_over = False
    game_quit = False
    ###
    life = 5
    pking_life = 5
    shield_item_count = db.query_db("select shield from item where item_id=1;", one=True)['shield']
    life_item_count = db.query_db("select life from item where item_id=1;", one=True)['life']
    slow_item_count = db.query_db("select slow from item where item_id=1;", one=True)['slow']
    coin_item_count = db.query_db("select coin from item where item_id=1;", one=True)['coin']

    ###
    paused = False

    # 게임 후 버튼
    r_btn_restart, r_btn_restart_rect = load_image(*resize('btn_restart.png', 150, 80, -1))
    btn_restart, btn_restart_rect = load_image('btn_restart.png', 150, 80, -1)
    r_btn_save, r_btn_save_rect = load_image(*resize('btn_save.png', 150, 80, -1))
    btn_save, btn_save_rect = load_image('btn_save.png', 150, 80, -1)
    r_btn_exit, r_btn_exit_rect = load_image(*resize('btn_exit.png', 150, 80, -1))
    btn_exit, btn_exit_rect = load_image('btn_exit.png', 150, 80, -1)



    # 디노 타입 때문에 변경된 부분
    player_dino = Dino(dino_size[0], dino_size[1], type=dino_type[type_idx])
    #

    new_ground = Ground(-1 * game_speed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    heart = HeartIndicator(life)
    speed_indicator = Scoreboard(width * 0.12, height * 0.15)
    counter = 0

    speed_text = font.render("SPEED", True, black)

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    stones = pygame.sprite.Group()  # add stones
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    coin_items = pygame.sprite.Group()

    Cactus.containers = cacti
    FireCactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    Stone.containers = stones
    CoinItem.containers = coin_items


    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    game_over_image, game_over_rect = load_image('game_over.png', 380, 100, -1)
    shield_item_image, shield_time_rect = load_sprite_sheet('item.png', 2, 1, 30, 30, -1)
    heart_item_image, heart_item_rect = load_image('heart_bullet.png', 30, 30, -1)
    slow_item_image, slow_item_rect = load_sprite_sheet('slow_pic.png', 2, 1, 30, 30, -1)
    coin_image, coin_rect = load_sprite_sheet('coin.png', 1, 7, 30, 30, -1)
    my_font = pygame.font.Font('DungGeunMo.ttf', 30)
    high_image = my_font.render('HI', True, black)
    high_rect = high_image.get_rect()
    high_rect.top = height * 0.15
    high_rect.left = width * 0.73

    # 1. 미사일 발사.
    space_go = False
    m_list = []
    bk = 0
    # 익룡이 격추되었을때
    is_down = False
    boom_count = 0
    #

    # 방향키 구현
    go_left = False
    go_right = False
    #

    # 보스몬스터 변수설정
    is_pking_time = False
    is_pking_alive = True
    pking = PteraKing(hp=pking_life)
    pking_heart = HeartIndicator(pking.hp, loc=1)
    pm_list = []
    pm_vector = []
    pm_pattern0_count = 0
    pm_pattern1_count = 0
    pking_appearance_score = 100

    jumpingx2 = False

    while not game_quit:
        while start_menu:
            pass
        while not game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player_dino.rect.bottom == int(0.98 * height):
                                player_dino.is_jumping = True
                                if pygame.mixer.get_init() is not None:
                                    jump_sound.play()
                                player_dino.movement[1] = -1 * player_dino.jump_speed

                        if event.key == pygame.K_DOWN:
                            # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (player_dino.is_jumping and player_dino.is_dead):
                                player_dino.is_ducking = True

                        if event.key == pygame.K_LEFT:
                            # print("left")
                            go_left = True

                        if event.key == pygame.K_RIGHT:
                            # print("right")
                            go_right = True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                        # jumping x2 ( press key s)
                        if event.key == pygame.K_s:
                            jumpingx2 = True

                        # 2. a키를 누르면, 미사일이 나갑니다.
                        if event.key == pygame.K_a:
                            space_go = True
                            bk = 0
                        #

                        # shield item
                        if event.key == pygame.K_q:
                            if shield_item_count > 0:
                                if pygame.mixer.get_init() is not None:
                                    check_point_sound.play()
                                player_dino.collision_immune = True
                                player_dino.is_super = True
                                item_time = pygame.time.get_ticks()
                                shield_item_count -= 1

                        # life item
                        if event.key == pygame.K_w:
                            if life_item_count > 0 and life < 5:
                                if pygame.mixer.get_init() is not None:
                                    check_point_sound.play()
                                life += 1
                                life_item_count -= 1

                        # slow item
                        if event.key == pygame.K_e:
                            if slow_item_count > 0 and game_speed > 4:
                                if pygame.mixer.get_init() is not None:
                                    check_point_sound.play()
                                game_speed -= 1
                                new_ground.speed += 1
                                slow_item_count -= 1

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            player_dino.is_ducking = False

                        # 3.a키에서 손을 떼면, 미사일이 발사 되지 않습니다.
                        if event.key == pygame.K_a:
                            space_go = False
                        # 방향키 추가
                        if event.key == pygame.K_LEFT:
                            go_left = False
                        if event.key == pygame.K_RIGHT:
                            go_right = False
                        #

                        # jumgpingx2
                        if event.key == pygame.K_s:
                            jumpingx2 = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and player_dino.rect.bottom == int(0.98 * height):
                            # (mouse left button, wheel button, mouse right button)
                            player_dino.is_jumping = True
                            if pygame.mixer.get_init() is not None:
                                jump_sound.play()
                            player_dino.movement[1] = -1 * player_dino.jump_speed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (player_dino.is_jumping and player_dino.is_dead):
                                player_dino.is_ducking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        player_dino.is_ducking = False

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            if not paused:

                if go_left:
                    if player_dino.rect.left < 0:
                        player_dino.rect.left = 0
                    else:
                        player_dino.rect.left = player_dino.rect.left - game_speed

                if go_right:
                    if player_dino.rect.right > width:
                        player_dino.rect.right = width
                    else:
                        player_dino.rect.left = player_dino.rect.left + game_speed
                #

                # 4. space_go가 True이고, 일정 시간이 지나면, 미사일을 만들고, 이를 미사일 배열에 넣습니다.
                if space_go and (int(bk % 15) == 0):
                    # print(bk)
                    mm = Obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if player_dino.type == 'RED':
                        mm.put_img("./sprites/black_bullet.png")
                        mm.change_size(10, 10)
                    elif player_dino.type == 'YELLOW':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(10, 10)
                    elif player_dino.type == 'ORANGE':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(10, 10)
                    elif player_dino.type == 'PURPLE':
                        mm.put_img("./sprites/pink_bullet.png")
                        mm.change_size(15, 5)
                    elif player_dino.type == 'PINK':
                        mm.put_img("./sprites/heart_bullet.png")
                        mm.change_size(10, 10)
                    else:
                        mm.put_img("./sprites/red_bullet.png")
                        mm.change_size(10, 10)

                    if not player_dino.is_ducking:
                        mm.x = round(player_dino.rect.centerx)
                        mm.y = round(player_dino.rect.top * 1.035)

                    if player_dino.is_ducking:
                        mm.x = round(player_dino.rect.centerx)
                        mm.y = round(player_dino.rect.centery * 1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk = bk + 1
                d_list = []

                for i in range(len(m_list)):
                    m = m_list[i]
                    m.x += m.move
                    if m.x > width:
                        d_list.append(i)

                d_list.reverse()
                for d in d_list:
                    del m_list[d]

                if jumpingx2:
                    if player_dino.rect.bottom == int(height * 0.98):
                        player_dino.is_jumping = True
                        player_dino.movement[1] = -1 * player_dino.super_jump_speed

                # 보스 몬스터 패턴0(위에서 가만히 있는 패턴): 보스 익룡이 쏘는 미사일.
                if is_pking_time and (pking.pattern_idx == 0) and (int(pm_pattern0_count % 20) == 0):
                    pm = Obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15, 15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.x_move = random.randint(0, 15)
                    pm.y_move = random.randint(1, 3)

                    pm_list.append(pm)
                pm_pattern0_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm = pm_list[i]
                    pm.x -= pm.x_move
                    pm.y += pm.y_move
                    if pm.y > height or pm.x < 0:
                        pd_list.append(i)
                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]

                # 보스 몬스터 패턴1(좌우로 왔다갔다 하는 패턴): 보스 익룡이 쏘는 미사일.
                if is_pking_time and (pking.pattern_idx == 1) and (int(pm_pattern1_count % 20) == 0):
                    # print(pm_list)
                    pm = Obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15, 15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.move = 3
                    pm_list.append(pm)
                pm_pattern1_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm = pm_list[i]
                    pm.y += pm.move
                    if pm.y > height or pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]
                #

                for c in cacti:
                    c.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, c):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, f):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * game_speed

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if len(m_list) == 0:
                        pass
                    else:
                        if (m.x >= p.rect.left) and (m.x <= p.rect.right) and (m.y > p.rect.top) and (
                                m.y < p.rect.bottom):
                            print("격추 성공")
                            is_down = True
                            boom = Obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200, 100)
                            boom.x = p.rect.centerx - round(p.rect.width) * 2.5
                            boom.y = p.rect.centery - round(p.rect.height) * 1.5
                            player_dino.score += 30
                            p.kill()
                            # 여기만 바꿈
                            m_list.remove(m)

                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, p):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for s in stones:
                    s.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, s):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                if player_dino.is_super:
                    if pygame.time.get_ticks() - item_time > shield_time:
                        player_dino.collision_immune = False
                        player_dino.is_super = False

                for c in coin_items:
                    c.movement[0] = -1 * game_speed
                    if pygame.sprite.collide_mask(player_dino, c):
                        if pygame.mixer.get_init() is not None:
                            check_point_sound.play()
                        coin_item_count += 1
                        c.kill()
                    elif l.rect.right < 0:
                        c.kill()

                STONE_INTERVAL = 100
                CACTUS_INTERVAL = 50
                # 익룡을 더 자주 등장시키기 위해 12로 수정했습니다. (원래값은 300)
                PTERA_INTERVAL = 12
                #
                CLOUD_INTERVAL = 300

                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                # print(pking.hp)
                if is_pking_alive and (player_dino.score > pking_appearance_score):
                    is_pking_time = True
                else:
                    is_pking_time = False

                if len(coin_items) < 2:
                    if len(coin_items) == 0:
                        last_obstacle.empty()
                        last_obstacle.add(CoinItem(game_speed, object_size[0], object_size[1]))
                else:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(CoinItem(game_speed, object_size[0], object_size[1]))

                if is_pking_time:
                    if len(cacti) < 2:
                        if len(cacti) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))

                    if len(fire_cacti) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(
                                    CACTUS_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(FireCactus(game_speed, object_size[0], object_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))

                    if len(m_list) == 0:
                        pass
                    else:
                        if (m.x >= pking.rect.left) and (m.x <= pking.rect.right) and (m.y > pking.rect.top) and (
                                m.y < pking.rect.bottom):
                            is_down = True
                            boom = Obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200, 100)
                            boom.x = pking.rect.centerx - round(pking.rect.width)
                            boom.y = pking.rect.centery - round(pking.rect.height / 2)
                            pking.hp -= 1
                            m_list.remove(m)

                            if pking.hp <= 0:
                                pking.kill()
                                new_ground.speed -= 1
                                game_speed += 1
                                pking_life *= 1.2
                                pking_life = int(pking_life)
                                pking = PteraKing(hp=pking_life)
                                pking_heart = HeartIndicator(pking.hp, loc=1)
                                pking_appearance_score *= 2

                    #
                    if len(pm_list) == 0:
                        pass
                    else:
                        # print("x: ",pm.x,"y: ",pm.y)
                        for pm in pm_list:
                            if (pm.x >= player_dino.rect.left) and (pm.x <= player_dino.rect.right) and (
                                    pm.y > player_dino.rect.top) and (pm.y < player_dino.rect.bottom):
                                print("공격에 맞음.")
                                # if pygame.sprite.collide_mask(player_dino, pm):
                                player_dino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    player_dino.is_dead = True
                                pm_list.remove(pm)
                    #
                else:
                    if len(cacti) < 2:
                        if len(cacti) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))
                        else:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(
                                        CACTUS_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))

                    if len(fire_cacti) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(
                                    CACTUS_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(FireCactus(game_speed, object_size[0], object_size[1]))

                    if len(stones) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Stone(game_speed, object_size[0], object_size[1]))

                    if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(Ptera(game_speed, ptera_size[0], ptera_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))

                player_dino.update()
                cacti.update()
                fire_cacti.update()
                stones.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                new_ground.update()
                scb.update(player_dino.score)
                highsc.update(high_score)
                speed_indicator.update(game_speed - 3)
                heart.update(life)
                pking_heart.update(pking.hp)
                slow_items.update()
                coin_items.update()

                # 보스몬스터 타임이면,
                if is_pking_time:
                    pking.update()
                #

                if pygame.display.get_surface() is not None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    speed_indicator.draw()
                    screen.blit(speed_text, (width * 0.01, height * 0.15))
                    screen.blit(shield_item_image[0], (width * 0.01, height * 0.23))
                    screen.blit(heart_item_image, (width * 0.01, height * 0.33))
                    screen.blit(slow_item_image[0], (width * 0.01, height * 0.43))
                    screen.blit(coin_image[0], (width * 0.60, height * 0.15))
                    shield_item_count_text = font.render(f"X{shield_item_count}", True, black)
                    life_item_count_text = font.render(f"X{life_item_count}", True, black)
                    slow_item_count_text = font.render(f"X{slow_item_count}", True, black)
                    coin_count_text = font.render(f"X{coin_item_count}", True, black)
                    screen.blit(shield_item_count_text, (width * 0.05, height * 0.23))
                    screen.blit(life_item_count_text, (width * 0.05, height * 0.33))
                    screen.blit(slow_item_count_text, (width * 0.05, height * 0.43))
                    screen.blit(coin_count_text, (width * 0.65, height * 0.15))
                    heart.draw()
                    pking_heart.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(high_image, high_rect)
                    cacti.draw(screen)
                    fire_cacti.draw(screen)
                    stones.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    coin_items.draw(screen)

                    # pkingtime이면, 보스몬스터를 보여줘라.
                    if is_pking_time:
                        # print(pking.pattern_idx)
                        pking.draw()
                        # 보스 익룡이 쏘는 미사일을 보여준다.
                        for pm in pm_list:
                            pm.show()
                    #

                    # 5. 미사일 배열에 저장된 미사일들을 게임 스크린에 그려줍니다.
                    for m in m_list:
                        m.show()
                        # print(type(mm.x))
                    if is_down:
                        boom.show()
                        boom_count += 1
                        # boom_count가 5가 될 때까지 boom이미지를 계속 보여준다.
                        if boom_count > 10:
                            boom_count = 0
                            is_down = False
                    #

                    player_dino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_center)
                    pygame.display.update()
                clock.tick(FPS)

                if player_dino.is_dead:
                    game_over = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if player_dino.score > high_score:
                        high_score = player_dino.score

        if game_quit:
            break

        while game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_quit = True
                            game_over = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            game_over = False
                            game_quit = True
                            type_score(player_dino.score)
                            if not db.is_limit_data(player_dino.score, mode="hard"):
                                db.query_db(
                                    f"insert into hard_mode(username, score) values ('{gamer_name}', '{player_dino.score}');")
                                db.query_db(
                                    f"update item set shield = {shield_item_count}, life = {life_item_count}, slow = {slow_item_count}, coin = {coin_item_count} where item_id=1;")
                                db.commit()
                                board("hard")
                            else:
                                board("hard")

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #game_over = False
                        #game_quit = True
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            x, y = event.pos
                            if r_btn_restart_rect.collidepoint(x, y):
                                select_mode()
                            if r_btn_save_rect.collidepoint(x, y):
                                type_score(player_dino.score)
                                if not db.is_limit_data(player_dino.score, mode="hard"):
                                    db.query_db(
                                        f"insert into hard_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                                    db.query_db(
                                        f"update item set shield = {shield_item_count}, life = {life_item_count}, slow = {slow_item_count}, coin = {coin_item_count} where item_id=1;")
                                    db.commit()
                                    board("hard")
                                else:
                                    board("hard")
                            if r_btn_exit_rect.collidepoint(x, y):
                                intro_screen()

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)
                r_btn_restart_rect.centerx, r_btn_restart_rect.centery = resized_screen.get_width() * 0.25, resized_screen.get_height() * 0.6
                r_btn_save_rect.centerx, r_btn_save_rect.centery = resized_screen.get_width() * 0.5, resized_screen.get_height() * 0.6
                r_btn_exit_rect.centerx, r_btn_exit_rect.centery = resized_screen.get_width() * 0.75, resized_screen.get_height() * 0.6
                disp_gameover_buttons(btn_restart, btn_save, btn_exit)

                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            highsc.update(high_score)
            if pygame.display.get_surface() is not None:
                disp_gameover_msg(game_over_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(high_image, high_rect)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()

def board(mode=""):
    global resized_screen
    game_quit = False
    scroll_y = 0
    # 10
    max_per_screen = 10
    length = 0
    results = ""
    if mode == "":
        easy_mode_results = db.query_db(f"select username, score from easy_mode order by score desc;")
        hard_mode_results = db.query_db(f"select username, score from hard_mode order by score desc;")
        length = len(easy_mode_results) if len(easy_mode_results) > len(hard_mode_results) else len(hard_mode_results)
    else:
        results = db.query_db(f"select username, score from {mode}_mode order by score desc;")
        length = len(results)
    screen_board_height = resized_screen.get_height() + (length // max_per_screen) * resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
    ))

    title_image, title_rect = load_image("ranking.png", 360, 75, -1)
    title_rect.centerx = width * 0.5
    title_rect.centery = height * 0.2

    #back button
    btn_back, btn_back_rect = load_image('btn_back.png', 100, 50, -1)
    r_btn_back, r_btn_back_rect = load_image(*resize('btn_back.png', 100, 50, -1))

    while not game_quit:
        if pygame.display.get_surface() is None:
            game_quit = True
        else:
            screen_board.fill(background_col)
            screen_board.blit(title_image, title_rect)
            screen_board.blit(btn_back, btn_back_rect)
            if results:
                for i, result in enumerate(results):
                    top_i_surface = font.render(f"TOP {i + 1}", True, black)
                    name_inform_surface = font.render("Name", True, black)
                    score_inform_surface = font.render("Score", True, black)
                    score_surface = font.render(str(result['score']), True, black)
                    txt_surface = font.render(result['username'], True, black)

                    screen_board.blit(top_i_surface, (width * 0.25, height * (0.55 + 0.1 * i)))
                    screen_board.blit(name_inform_surface, (width * 0.4, height * 0.40))
                    screen_board.blit(score_inform_surface, (width * 0.6, height * 0.40))
                    screen_board.blit(txt_surface, (width * 0.4, height * (0.55 + 0.1 * i)))
                    screen_board.blit(score_surface, (width * 0.6, height * (0.55 + 0.1 * i)))
            else:
                easy_mode_surface = font.render(f"[Easy Mode]", True, black)
                hard_mode_surface = font.render(f"[Hard Mode]", True, black)
                screen_board.blit(easy_mode_surface, (width * 0.2, height * 0.35))
                screen_board.blit(hard_mode_surface, (width * 0.62, height * 0.35))
                for i, result in enumerate(easy_mode_results):
                    top_i_surface = font.render(f"TOP {i + 1}", True, black)
                    name_inform_surface = font.render("Name", True, black)
                    score_inform_surface = font.render("Score", True, black)
                    score_surface = font.render(str(result['score']), True, black)
                    txt_surface = font.render(result['username'], True, black)

                    screen_board.blit(top_i_surface, (width * 0.05, height * (0.55 + 0.1 * i)))
                    screen_board.blit(name_inform_surface, (width * 0.2, height * 0.45))
                    screen_board.blit(score_inform_surface, (width * 0.35, height * 0.45))
                    screen_board.blit(txt_surface, (width * 0.2, height * (0.55 + 0.1 * i)))
                    screen_board.blit(score_surface, (width * 0.35, height * (0.55 + 0.1 * i)))

                for i, result in enumerate(hard_mode_results):
                    top_i_surface = font.render(f"TOP {i + 1}", True, black)
                    name_inform_surface = font.render("Name", True, black)
                    score_inform_surface = font.render("Score", True, black)
                    score_surface = font.render(str(result['score']), True, black)
                    txt_surface = font.render(result['username'], True, black)

                    screen_board.blit(top_i_surface, (width * 0.5, height * (0.55 + 0.1 * i)))
                    screen_board.blit(name_inform_surface, (width * 0.62, height * 0.45))
                    screen_board.blit(score_inform_surface, (width * 0.77, height * 0.45))
                    screen_board.blit(txt_surface, (width * 0.62, height * (0.55 + 0.1 * i)))
                    screen_board.blit(score_surface, (width * 0.77, height * (0.55 + 0.1 * i)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game_quit = True
                        intro_screen()
                    if event.key == pygame.K_UP:
                        scroll_y = min(scroll_y + 15, 0)
                    if event.key == pygame.K_DOWN:
                        scroll_y = max(scroll_y - 15, -(len(results) // max_per_screen) * scr_size[1])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if r_btn_back_rect.collidepoint(x, y):
                            intro_screen()  
                    if event.button == 4:
                        scroll_y = min(scroll_y + 15, 0)
                    if event.button == 5:
                        scroll_y = max(scroll_y - 15, -(len(results) // max_per_screen) * scr_size[1])
                    #if event.button == 1:
                        #game_quit = True
                        #intro_screen()
                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)
            r_btn_back_rect.centerx = resized_screen.get_width() * 0.1
            r_btn_back_rect.centery = resized_screen.get_height() * 0.1        
            score_board(btn_back)
            screen.blit(btn_back, btn_back_rect)
            screen.blit(screen_board, (0, scroll_y))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


def pausing():
    global resized_screen
    game_quit = False
    pause_pic, pause_pic_rect = load_image('paused.png', 360, 75, -1)
    pause_pic_rect.centerx = width * 0.5
    pause_pic_rect.centery = height * 0.2

    pygame.mixer.music.pause()  # 일시정지상태가 되면 배경음악도 일시정지

    # BUTTON IMG LOAD
    retbutton_image, retbutton_rect = load_image('main_button.png', 70, 62, -1)
    resume_image, resume_rect = load_image('continue_button.png', 70, 62, -1)

    resized_retbutton_image, resized_retbutton_rect = load_image(*resize('main_button.png', 70, 62, -1))
    resized_resume_image, resized_resume_rect = load_image(*resize('continue_button.png', 70, 62, -1))

    # BUTTONPOS
    retbutton_rect.centerx = width * 0.4
    retbutton_rect.top = height * 0.52
    resume_rect.centerx = width * 0.6
    resume_rect.top = height * 0.52

    resized_retbutton_rect.centerx = resized_screen.get_width() * 0.4
    resized_retbutton_rect.top = resized_screen.get_height() * 0.52
    resized_resume_rect.centerx = resized_screen.get_width() * 0.6
    resized_resume_rect.top = resized_screen.get_height() * 0.52

    while not game_quit:
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            game_quit = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        # pausing상태에서 다시 esc누르면 배경음악 일시정지 해제
                        return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if resized_retbutton_rect.collidepoint(x, y):
                            intro_screen()

                        if resized_resume_rect.collidepoint(x, y):
                            pygame.mixer.music.unpause()  # pausing상태에서 오른쪽의 아이콘 클릭하면 배경음악 일시정지 해제

                            return False

                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)

            screen.fill(white)
            screen.blit(pause_pic, pause_pic_rect)
            screen.blit(retbutton_image, retbutton_rect)
            screen.blit(resume_image, resume_rect)
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


def type_score(score):
    global resized_screen
    global gamer_name
    global width, height
    done = False
    active = True
    message_pos = (width * 0.25, height * 0.3)
    score_pos = (width * 0.35, height * 0.4)
    input_box_pos = (width * 0.43, height * 0.5)
    type_box_size = 100
    letter_num_restriction = 3
    input_box = pygame.Rect(input_box_pos[0], input_box_pos[1], 500, 50)
    color = pygame.Color('dodgerblue2')
    text = ''
    text2 = font.render("플레이어 이름을 입력해주세요", True, black)
    text3 = font.render(f"CURRENT SCORE: {score}", True, black)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                intro_screen()
            if event.type == pygame.KEYDOWN:
                # if active:
                if event.key == pygame.K_RETURN:
                    gamer_name = text.upper()
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if event.unicode.isalpha():
                        if len(text) < letter_num_restriction:
                            text += event.unicode

            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)

        screen.fill(white)
        txt_surface = text_size(50).render(text.upper(), True, color)
        input_box.w = type_box_size
        screen.blit(txt_surface, (input_box.centerx - len(text) * 11 - 5, input_box.y))
        screen.blit(text2, message_pos)
        screen.blit(text3, score_pos)
        pygame.draw.rect(screen, color, input_box, 2)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)

        pygame.display.flip()
        clock.tick(FPS)

