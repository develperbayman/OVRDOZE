import os, sys

import math
import random
import time
import mixer
from classtest import *
from _thread import *
import threading
import copy
import los
from network import Network
import ast
import network_parser
from app import App
from weapon_button import weapon_button
from button import Button
from glitch import Glitch
from values import *
import classes
from classes import items
import func
#import path_finding

import armory
import objects
import enemies
import RUN

import enem_obs

print("IMPORTS COMPLETE")



terminal = pygame.font.Font('texture/terminal.ttf', 20)
terminal2 = pygame.font.Font('texture/terminal.ttf', 30)
terminal3 = pygame.font.Font('texture/terminal.ttf', 10)

terminal_map_desc = pygame.font.Font('texture/terminal.ttf', 50)
terminal_map_desc2 = pygame.font.Font('texture/terminal.ttf', 25)


def give_weapon(kind,name):
    return armory.__weapons_map[kind][name].copy()



# if multiplayer:
#     net = Network()
#     print("MULTIPLAYER")
# else:
#     print("SINGLEPLAYER")


def thread_data_collect(net, packet, player_actor, multiplayer_actors, bullet_list, grenade_list, current_threading, zomb_info):
    try:
        reply = net.send(packet).translate({ord('/'): None})
        network_parser.gen_from_packet(reply, player_actor, multiplayer_actors, zomb_info)


    except Exception as e:
        print("CLIENT ERROR:", traceback.print_exc())
        pass
    current_threading = False


def write_packet(object):
    string = write_packet.get_string() + "\n"
    return string


def quit(app):
    app.pygame.mixer.music.unload()
    print("Quitting game")

    RUN.main()

def cont_game(arg):
    return True





def main(app, multiplayer = False, net = None, host = False, players = None, self_name = None, difficulty = "NORMAL", draw_los = True, dev_tools = True, skip_intervals = False, map = None, full_screen_mode = True):
    print("GAME STARTED WITH",difficulty)

    diff_rates = {"NO ENEMIES" : [0,1,1,1, -1], "EASY" : [0.9,0.9,0.75,1, 3], "NORMAL" : [1,1,1,1,6], "HARD" : [1.25, 1.25, 1.1, 0.85, 10], "ONSLAUGHT" : [1.5, 1.35, 1.2, 0.7, 14]} #

    sanity_drain, zombie_hp, zombie_damage, turret_bullets, enemy_count = diff_rates[difficulty]



    if multiplayer:
        enemy_count = 1

        packet_dict.clear()


    global barricade_in_hand

    clicked = False
    fps_counter = time.time()


    los_image = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
    los_image.set_colorkey((255,255,255))
        #
    #los_image.set_alpha(150)

    x_vel = 0
    y_vel = 0
    last_hp = 0
    multi_kill_ticks = 0
    multi_kill = 0
    global kills
    kills = 0
    player_Angle = 0
    bullets_new = []
    current_threading = False
    data_collector = None
    collision_check_player = True



    last_ping = 0

    pause = False

    wave_text_tick = -20



    wave_anim_ticks = [0,0]

    tick_rate = 3
    server_tick = 0

    respawn_ticks = 0
    app.pygame.init()
    app.pygame.font.init()
    app.pygame.mixer.init()



    if full_screen_mode:
        full_screen = app.pygame.display.set_mode(fs_size, flags = pygame.FULLSCREEN, vsync=1) #
        print(pygame.display.get_driver())
        print(app.pygame.display.Info())
        screen =  app.pygame.Surface(size).convert()
        mouse_conversion = fs_size[0] / size[0]
    else:
        screen = app.pygame.display.set_mode(size, pygame.RESIZABLE, vsync=1)
        mouse_conversion = 1

    print(mouse_conversion)

    expl1 = func.load_animation("anim/expl1",0,31)

    clock = app.pygame.time.Clock()
    multiplayer_actors = {}
    if multiplayer:

        for y in players:
            if y == "" or y == self_name:
                continue
            multiplayer_actors[y] = enemies.Player_Multi(y)
    enemy_up_time = time.time()









    weapon_keys = list(armory.__weapons_map["gun"].keys())
    print("KEYS",weapon_keys)


    #multiplayer = True









    active_maps = [map]

    enemy_list.clear()
    turret_list.clear()
    burn_list.clear()



    fps = []

    ### load

    player_inventory = classes.Inventory(interactables, player = True)

    turret_bro.clear()

    turret_bro.append(objects.MovingTurret.MovingTurret([100,300],4,5,500,20,-1, NAV_MESH = None, walls = None, map = None))

    map, map_render, map_boundaries, NAV_MESH, player_pos, camera_pos, wall_points, walls_filtered = load_level(map, mouse_conversion, player_inventory, app)

    wave = False
    wave_number = 0

    if not skip_intervals:
        wave_interval = 17
        wave_change_timer = time.time()
    else:
        wave_interval = 2
        wave_change_timer = time.time() - 15

    wave_length = 30





    player_actor = classes.Player(self_name, turret_bullets)

    player_melee = armory.Melee.Melee(strike_count = 2, damage = 35, hostile = False, owner_object = player_actor)




    #draw_los = True

    m_clicked = False



    phase = 0





    #[classes.Barricade([100,300], [200,400], map)]
    player_weapons.clear()
    player_weapons.append(give_weapon("gun","M1911"))
    player_weapons.append(give_weapon("gun","NRG-LMG Mark1"))
        #give_weapon("gun", "SCAR18"),
        # give_weapon("gun","M134 MINIGUN"),
        # give_weapon("gun","AR-15"),
        # give_weapon("gun","GLOCK"),
        # give_weapon("gun","AWP"),
        # give_weapon("gun","AK"),
        # give_weapon("gun","SPAS"),
        # give_weapon("gun","P90")
        # ]

    gun_name_list = ["M1911", "GLOCK", "AR-15", "MP5", "AWP", "AK", "SPAS", "P90", "SCAR18", "M134 MINIGUN", "NRG-LMG Mark1"]
    ruperts_shop_selections.clear()
    for i, x in enumerate(gun_name_list):
        ruperts_shop_selections.append(weapon_button(give_weapon("gun", x),i))

    a = sorted(ruperts_shop_selections, key=lambda x: x.weapon.price)

    ruperts_shop_selections.clear()

    for i, x in enumerate(a):
        x.slot = i
        ruperts_shop_selections.append(x)




    # ruperts_shop_selections.append(weapon_button(give_weapon("gun", "AR-15"),1))
    # ruperts_shop_selections.append(weapon_button(give_weapon("gun", "AK"),2))
    # ruperts_shop_selections.append(weapon_button(give_weapon("gun", "SPAS"),3))
    for weapon_1 in player_weapons:
        not_used_weapons.append(weapon_1.name)


    c_weapon = (player_weapons[0])
    weapon_scroll = 0

    #pygame.mixer.music.set_volume(0.75)

    app.pygame.mouse.set_visible(False)
    path = os.path.abspath(os.getcwd()) + "/sound/songs/"
    songs = []
    for file in os.listdir(path):
        if file.endswith(".wav") and file != "menu_loop.wav" and file != "overworld_loop.wav":
            songs.append("sound/songs/" + file)

    pause_tick = False

    background_surf = app.pygame.Surface(size)
    background_surf.set_alpha(100)

    glitch = Glitch(screen)


    resume_button = Button([size[0]/2,100], "Resume", cont_game, None,gameInstance=app.pygame,glitchInstance=glitch)
    quit_button = Button([size[0]/2,200], "Quit", quit, app,gameInstance=app.pygame,glitchInstance=glitch)
    drying_time = time.time()

    last_tick = time.time() - 1

    start_time = time.time()

    playing_song = ""

    fade_tick.value = 15

    beat_red = 0

    wave_text_color = True


    while 1:


        tick_time = time.time() - last_tick
        last_tick = time.time()

        tick_delta = tick_time/(1/60)

        timedelta.timedelta = min([tick_delta, 3])

        if player_actor.hp > 0:

            #hp_time_dilation = 0.1 + (player_actor.hp/100)**0.4 * 0.9

            if player_actor.hp < 30:

                timedelta.timedelta *= 0.5

            #pygame.display.set_gamma(1,random.randint(1,3),1.1)



        clock.tick(144)

        t = time.time()
        time_stamps = {}




        mouse_pos = app.pygame.mouse.get_pos()

        mouse_pos = [mouse_pos[0] / mouse_conversion, mouse_pos[1] / mouse_conversion]

        click_single_tick = False
        if app.pygame.mouse.get_pressed()[0] and clicked == False:
            clicked = True
            click_single_tick = True
        elif app.pygame.mouse.get_pressed()[0] == False:
            clicked = False



        if pause:
            app.pygame.mouse.set_visible(True)




            screen.fill((0,0,0))
            screen.blit(background_surf,(0,0))

            s1 = resume_button.tick(screen, mouse_pos, click_single_tick, glitch)
            quit_button.tick(screen, mouse_pos, click_single_tick, glitch, arg = app)


            pressed = app.pygame.key.get_pressed()
            if (pressed[app.pygame.K_ESCAPE] or s1) and not pause_tick:
                menu_click2.play()
                pause = False
                pause_tick = True
                glitch.glitch_tick = 5
                app.pygame.mouse.set_visible(False)
                click_single_tick = False
                app.pygame.mixer.music.unpause()

            elif not pressed[app.pygame.K_ESCAPE]:
                pause_tick = False

            for event in app.pygame.event.get():
                if event.type == app.pygame.QUIT: sys.exit()

            glitch.tick()
            if full_screen_mode:
                app.pygame.transform.scale(screen, full_screen.get_rect().size, full_screen)


            app.pygame.display.update()

            continue

        if c_weapon.jammed and click_single_tick:
            if random.uniform(0,1) < 0.3:
                c_weapon.jammed = False
                gun_jam_clear.play()
            else:
                gun_jam.play()




        if map.name == "Overworld":
            overworld = True
        else:
            overworld = False

        if dialogue != []:
            app.pygame.mouse.set_visible(True)
            block_movement = True

        else:
            # app.pygame.mouse.set_visible(False)
            block_movement = False


        if app.pygame.mixer.music.get_busy() == False:

            if overworld:
                app.pygame.mixer.music.load("sound/songs/overworld_loop.wav")
                app.pygame.mixer.music.play(-1)
            else:
                up_next = playing_song
                while up_next == playing_song:
                    up_next = func.pick_random_from_list(songs)
                app.pygame.mixer.music.load(up_next)
                playing_song = func.pick_random_from_list(songs)
                app.pygame.mixer.music.play()

                with open(f"{up_next}_timestamps.txt") as file: # Use file to refer to the file object
                    beat_map = ast.literal_eval(file.read())

                song_start_t = time.time()
                beat_index = 0

        beat_red = (beat_red-1)*0.85+1
        try:
            if time.time() - song_start_t > beat_map[beat_index] > 0:
                beat_red = 3
                beat_index += 1

                if wave_text_color:
                    wave_text_color = False
                else:
                    wave_text_color = True




        except:
            pass
        if wave:
            camera_pos = [camera_pos[0] + random.uniform(-beat_red+1, beat_red-1), camera_pos[1] + random.uniform(-beat_red+1, beat_red-1)]



        if time.time() - drying_time > 1:
            map_render.blit(map.__dict__["map_rendered_alpha"],(0,0))
            drying_time = time.time()


        time_stamps["blood_drying"] = time.time() - t
        t = time.time()




        if phase != 4:
            camera_pan = c_weapon.__dict__["view"]
        else:
            camera_pan = 0.2


        m_click = app.pygame.mouse.get_pressed()[1]

        if m_click == True and m_clicked == False and dev_tools:
            m_clicked = True

            print("CLICK")

            phase += 1


            if phase == 4:
                app.pygame.mouse.set_visible(True)
            else:
                app.pygame.mouse.set_visible(False)
            if phase == 7:
                phase = 0


        elif m_click == False:
            m_clicked = False

        r_click = app.pygame.mouse.get_pressed()[2]

        r_click_tick = False

        if r_click == True and r_clicked == False:
            r_clicked = True
            r_click_tick = True
            print("CLICK")


        elif r_click == False:
            r_clicked = False










        scroll = [False, False]


        for event in app.pygame.event.get():
            if event.type == app.pygame.QUIT: sys.exit()


            if event.type == app.pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    print("Scroll down")
                    if block_movement:
                        scroll[0] = True
                        continue
                    searching = True
                    while searching:
                        weapon_scroll -= 1
                        if weapon_scroll == -1:
                            weapon_scroll = len(player_weapons) -1

                        c_weapon = (player_weapons[weapon_scroll])

                        if c_weapon.get_Ammo() != 0 or player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) != 0 or c_weapon.__dict__["ammo"] == "INF":
                            searching = False

                elif event.button == 5:
                    print("Scroll up")
                    if block_movement:
                        scroll[1] = True
                        continue
                    searching = True
                    while searching:
                        weapon_scroll += 1
                        if weapon_scroll == len(player_weapons):
                            weapon_scroll = 0

                        c_weapon = (player_weapons[weapon_scroll])

                        if c_weapon.get_Ammo() != 0 or player_inventory.get_amount_of_type(c_weapon.__dict__["ammo"]) != 0 or c_weapon.__dict__["ammo"] == "INF":
                            searching = False

        pressed = app.pygame.key.get_pressed()
        if pressed[app.pygame.K_ESCAPE] and not pause_tick:
            glitch.glitch_tick = 5
            pause = True
            pause_tick = True
            menu_click2.play()
            app.pygame.mixer.music.pause()

        elif not pressed[app.pygame.K_ESCAPE]:
            pause_tick = False



        key_r_click = False
        if pressed[app.pygame.K_r] and r_1 == False:
            r_1 = True
            key_r_click = True
        elif pressed[app.pygame.K_r] == False:
            r_1 = False



        screen.fill([0,0,0])
        try:
            fps_counter = time.time() - fps_counter
            fps.insert(0, fps_counter)
            if len(fps) > 60:
                fps.remove(fps[60])

        except Exception as e:
            print("EXCEPTION", e)
        fps_counter = time.time()
        func.keypress_manager(key_r_click,c_weapon, player_inventory)

        last_camera_pos = camera_pos.copy()


        camera_pos = func.camera_aling(camera_pos,player_pos)

        if overworld:

            camera_map_edge_tolerance = 0

            if camera_pos[0] < - camera_map_edge_tolerance:
                camera_pos[0] = - camera_map_edge_tolerance
            elif camera_pos[0] > map.size_converted[0] - size[0] + camera_map_edge_tolerance:
                camera_pos[0] = map.size_converted[0] - size[0] + camera_map_edge_tolerance

            if camera_pos[1] <- camera_map_edge_tolerance:
                camera_pos[1] = - camera_map_edge_tolerance
            elif camera_pos[1] > map.size_converted[1] - size[1] + camera_map_edge_tolerance:
                camera_pos[1] = map.size_converted[1] - size[1] + camera_map_edge_tolerance



        cam_delta = func.minus_list(last_camera_pos,camera_pos)








        if pressed[app.pygame.K_TAB] and tab_pressed == False and player_actor.get_hp() > 0:

            tab_pressed = True

            player_inventory.toggle_inv(app, player_pos = player_pos)

        elif pressed[app.pygame.K_TAB] == False:
            tab_pressed = False

        f_press = False

        if pressed[app.pygame.K_f] and f_pressed == False and player_actor.get_hp() > 0:

            f_pressed = True

            f_press = True


        elif pressed[app.pygame.K_f] == False:
            f_pressed = False


        time_stamps["init"] = time.time() - t
        t = time.time()





        mouse_pos_var = [camera_pan*(mouse_pos[0] - size[0]/2), camera_pan*(mouse_pos[1] - size[1]/2)]

        if player_inventory.get_inv() == False:

            camera_pos = [camera_pos[0] + mouse_pos_var[0], camera_pos[1] + mouse_pos_var[1]]

        for active_map in active_maps:
            #active_map.__dict__["map_rendered"]

            screen.blit(map_render,[-camera_pos[0] + active_map.__dict__["pos"][0],-camera_pos[1] + active_map.__dict__["pos"][1]])



        los_walls = los.walls_generate(walls_filtered,camera_pos)


        time_stamps["walls"] = time.time() - t
        t = time.time()


        pvp = overworld

        if not pvp:

            if wave:
                if time.time() - wave_change_timer > wave_length:

                    if wave_number >= 5:
                        for x in interactables:
                            if x.type == "door":
                                x.active = True


                    wave = False
                    pygame.display.set_gamma(1,1.1,1.1)
                    wave_change_timer = time.time()

                    wave_anim_ticks = [120, 0]
                wave_text_tick += timedelta.mod(beat_red)


            else:

                #


                if True: #Kill enemies if no wave.

                    if len(enemy_list) != 0:
                        rand_enemy = func.pick_random_from_list(enemy_list)
                        if random.uniform(0,1) < 1 and not los.check_los(player_actor.pos, rand_enemy.pos, walls_filtered):
                            rand_enemy.kill(camera_pos, enemy_list, map_render, player_actor, silent = True)


                if time.time() - wave_change_timer > wave_interval:
                    wave_length += 3
                    #wave_interval += 1
                    wave = True
                    pygame.display.set_gamma(1.2,0.9,0.9)
                    wave_number += 1

                    wave_text_tick = -20

                    wave_anim_ticks = [0, 120]

                    if wave_number >= 5:
                        for x in interactables:
                            if x.type == "door":
                                x.active = False





            if len(enemy_list) < (enemy_count/(player_actor.__dict__["sanity"]/100+0.25)) and wave:
                type = "normal"
                type_drop = random.uniform(0,1)
                if type_drop < 0.02:
                    type = "big"
                elif type_drop < 0.05:
                    type = "bomber"


                zombo = enemies.Zombie(map.get_random_point(walls_filtered, p_pos = player_pos),interactables, player_actor, NAV_MESH, walls_filtered, hp_diff = zombie_hp, dam_diff = zombie_damage, type = type, wall_points = wall_points, player_ref = player_actor, identificator = random.randint(0,4096))
                #zombo = enem_obs.Enemy(map.get_random_point(walls_filtered, p_pos = player_pos), give_weapon("gun", func.pick_random_from_dict(armory.guns, key = True)), interactables)
                #print(f"Zombie spawned with id {zombo.identificator}")
                enemy_list.append(zombo)
                if multiplayer:
                    if "zombies" not in packet_dict:
                        packet_dict["zombies"] = []
                    packet_dict["zombies"].append(zombo)

            #func.print_s(screen, str(round(enemy_count/((player_actor.__dict__["sanity"]/100)+0.25),3)),3)

            if time.time() - enemy_up_time > 20 and enemy_count != -1:
                enemy_up_time = time.time()
                enemy_count += 1
        for x in barricade_list:
            if x.tick(screen, camera_pos, map = map) == "KILL":
                barricade_list.remove(x)

        time_stamps["barricade"] = time.time() - t
        t = time.time()

        for x in turret_list:
            x.tick(screen, camera_pos,enemy_list,0, walls_filtered, player_pos)


        for x in npcs:
            x.tick(screen, player_actor, camera_pos, map)


        time_stamps["turrets"] = time.time() - t
        t = time.time()
        delete_list = []
        for x in interactables:
            x.__dict__["inv_save"] = player_inventory
            if x.__dict__["alive"] == False:
                delete_list.append(x)
            else:
                x.tick(screen, player_pos, camera_pos)
                if loading_cue != []:
                    door_dest = loading_cue[0]
                    loading_cue.clear()
                    for x in app.maps:
                        if x.name == door_dest:
                            map, map_render, map_boundaries, NAV_MESH, player_pos, camera_pos, wall_points, walls_filtered = load_level(x, mouse_conversion, player_inventory, app)

                            wave = False
                            wave_number = 0
                            wave_anim_ticks = [0,0]

                            if not skip_intervals:
                                wave_interval = 17
                                wave_change_timer = time.time()
                            else:
                                wave_interval = 2
                                wave_change_timer = time.time() - 15

                            wave_length = 30

        time_stamps["interactables"] = time.time() - t
        t = time.time()

        for x in delete_list:
            interactables.remove(x)

        for x in turret_bro:
            x.tick(screen, camera_pos,enemy_list,0, walls_filtered, player_pos)

        for x in particle_list:
            x.tick(screen, camera_pos, map)

        time_stamps["particles"] = time.time() - t
        t = time.time()

        if multiplayer:

            if data_collector == None or data_collector.is_alive() == False and server_tick == tick_rate:

                try:
                    ping = time.time() - thread_start - 1/60
                except:
                    pass
                thread_start = time.time()


                x_pos_1 = str(round(player_pos[0]))
                y_pos_1 = str(round(player_pos[1]))
                angle_1 = str(round(player_actor.get_angle()))

                packet = "PACKET\nPLAYER:" + self_name + "_" + x_pos_1 + "_" + y_pos_1 + "_" + angle_1 + "_" + str(player_actor.get_hp()) + "\n"



                for type_1 in packet_dict:
                    for x in packet_dict[type_1]:
                        packet += x.get_string() + "\n"

                for issue in zombie_events:
                    packet += issue + "\n"
                packet += "#END"

                packet_dict.clear()

                zomb_info = [interactables, camera_pos, map_render, NAV_MESH, walls_filtered, zombie_hp, zombie_damage]
                data_collector = threading.Thread(target = thread_data_collect, args = (net, packet, player_actor, multiplayer_actors, bullet_list, grenade_list, current_threading, zomb_info))
                data_collector.start()

                server_tick = 0
            if server_tick < tick_rate:
                server_tick += 1

            for x in multiplayer_actors:
                multiplayer_actors[x].tick(screen, player_pos, camera_pos, walls_filtered)

        bullet_list_copy = bullet_list.copy()
        grenade_list_copy = grenade_list.copy()



        grenade_throw_string = ""

        if pressed[app.pygame.K_g] and grenade_throw == False and player_actor.get_hp() > 0:

            grenade_throw = True

            if player_inventory.get_amount_of_type("HE Grenade") > 0:
                grenade_list.append(armory.Grenade(player_pos, func.minus(mouse_pos, camera_pos), "HE Grenade"))
                player_inventory.remove_amount("HE Grenade",1)
                print("throwing nade")

            elif player_inventory.get_amount_of_type("Molotov") > 0:
                grenade_list.append(armory.Grenade(player_pos, func.minus(mouse_pos, camera_pos), "Molotov"))
                player_inventory.remove_amount("Molotov",1)
                print("throwing nade")

        elif pressed[app.pygame.K_g] == False:
            grenade_throw = False



        last_bullet_list = tuple(bullet_list)

        if player_actor.get_hp() > 0:

            x_diff = (mouse_pos[0]+camera_pos[0])-player_pos[0]
            y_diff = (mouse_pos[1]+ camera_pos[1])-player_pos[1]

            if not block_movement:

                try:
                    angle = math.atan(x_diff/y_diff) * 180/math.pi +90
                    if (x_diff < 0 and y_diff > 0) or (x_diff > 0 and y_diff > 0):
                        angle += 180
                except:
                    angle = 0

            else:
                angle = player_actor.angle

            player_actor.set_aim_at(angle)

            weapon_pan_rate = c_weapon.__dict__["handling"]

            player_angle = player_actor.get_angle()

            if abs(angle - player_angle) > 1:
                player_angle = player_angle + timedelta.mod(los.get_angle_diff(angle, player_angle)* (weapon_pan_rate))
            else:
                player_angle = angle

            player_actor.set_angle(player_angle)

            if c_weapon.__dict__["name"] in ["GLOCK", "M1911"]:
                pl = player_pistol
            else:
                pl = player

            func.render_player(screen, mouse_pos, pl,player_pos, camera_pos, player_actor)

            if not block_movement:
                player_pos, x_vel, y_vel = func.player_movement2(pressed,player_pos,x_vel,y_vel)

            if collision_check_player:
                #angle_coll = map.check_collision(player_pos, map_boundaries, collision_box = 10, screen = screen, x_vel = x_vel, y_vel = y_vel, phase = phase)
                collision_types, angle_coll = map.checkcollision(player_pos,[x_vel, y_vel], 10, map_boundaries, ignore_barricades = True)
                if angle_coll:
                    #dddwwwfunc.debug_render(math.degrees(angle_coll))
                    player_pos = angle_coll

            player_actor.set_pos(player_pos)

            if player_actor.knockback_tick != 0:

                player_actor.pos = [player_actor.pos[0] + math.cos(player_actor.knockback_angle) * player_actor.knockback_tick**0.5, player_actor.pos[1] - math.sin(player_actor.knockback_angle) *player_actor.knockback_tick**0.5]
                player_actor.knockback_tick -= 1

            player_pos = player_actor.pos

            for x in burn_list:
                if los.get_dist_points(x.pos, player_pos) < 25:
                    player_actor.set_hp(timedelta.mod(1), reduce = True)

            if player_actor.__dict__["barricade_in_hand"] != None:
                func.print_s(screen, str(player_actor.__dict__["barricade_in_hand"].__dict__["stage"]), 3)
                result = player_actor.__dict__["barricade_in_hand"].tick(screen, camera_pos, mouse_pos, click_single_tick, map)
                if result == True:
                    barricade_list.append(player_actor.__dict__["barricade_in_hand"])
                    player_actor.__dict__["barricade_in_hand"] = None
                elif result == "revert":
                    player_inventory.append_to_inv(items["Barricade"], 1)
                    player_actor.__dict__["barricade_in_hand"] = None
            else:


                if player_inventory.get_inv() == False and not overworld:



                    firing_tick = func.weapon_fire(c_weapon, player_inventory, player_actor.get_angle(), player_pos, screen)
                    player_melee.tick(screen, r_click_tick)

                    if c_weapon._bullets_in_clip == 0 and click_single_tick:
                        gun_jam.play()

                else:
                    c_weapon.spread_recoverial()
                    c_weapon.weapon_tick()

            player_alive = True

        else:

            if player_alive:
                func.list_play(death_sounds)
                player_alive = False
                respawn_ticks = 120
                for i in range(5):
                    particle_list.append(classes.Particle(func.minus(player_pos, camera_pos), type = "blood_particle", magnitude = 1.2,screen = map_render))

            if respawn_ticks != 0:
                respawn_ticks -= 1
            else:
                player_actor.set_hp(100)
                player_pos = map.get_random_point(walls_filtered, enemies = enemy_list)
                #c_weapon = give_weapon(player_we[weapon_scroll])

        c_weapon.add_to_spread(math.sqrt(x_vel**2 + y_vel**2)/10)


        if last_hp == player_actor.get_hp() and player_alive == True:
            free_tick += timedelta.mod(1)
            if free_tick > 60 and player_actor.get_hp() < 100:
                player_actor.set_hp(timedelta.mod(-1), reduce = True)
                if player_actor.get_hp() >= 100:
                    player_actor.hp = 100




        else:
            free_tick = 0
            #glitch.glitch_tick = 5

        time_stamps["player"] = time.time() - t
        t = time.time()


        closest = 1000
        closest_prompt = None
        closest_available_prompt = None
        for x in interactables:

            dist = x.prompt_dist(player_pos)
            if dist:
                if dist < closest:
                    closest_prompt = x
                    closest = dist

                    if closest_prompt.type == "item":

                        if player_inventory.append_to_inv(closest_prompt.item, closest_prompt.amount, scan_only = True) != closest_prompt.amount:
                            closest_available_prompt = closest_prompt

        if closest_available_prompt != None:

            closest_available_prompt.tick_prompt(screen, player_pos, camera_pos, f_press = f_press)
        else:
            if closest_prompt != None:
                closest_prompt.tick_prompt(screen, player_pos, camera_pos, f_press = f_press)

        last_hp = player_actor.get_hp()
        if multi_kill_ticks > 0:
            multi_kill_ticks -= timedelta.mod(1)
        else:
            multi_kill = 0

        time_stamps["prompts"] = time.time() - t
        t = time.time()




        for enemy in enemy_list:
            enemy.tick(screen, map_boundaries, player_actor, camera_pos, map, walls_filtered, NAV_MESH, map_render, phase = phase, wall_points = wall_points)

        time_stamps["enemies"] = time.time() - t
        t = time.time()



        i2 = []
        for x in bullet_list:
            if x not in last_bullet_list:
                i2.append(x)
            kills_bullet = x.move_and_draw_Bullet(screen, camera_pos, map_boundaries, map, enemy_list, player_actor, draw_blood_parts = map_render, dummies = multiplayer_actors)
            if kills_bullet != 0 and kills_bullet != None:
                kills += kills_bullet
                multi_kill += kills_bullet

                if multi_kill > 99:
                    multi_kill = 1


                multi_kill_ticks = 45
                kill_counter = classes.kill_count_render(multi_kill, kill_rgb)


        last_bullet_list = tuple(bullet_list)

        bullets_new = tuple(i2)

        time_stamps["bullets"] = time.time() - t
        t = time.time()


        for x in grenade_list:
            x.tick(screen, map_boundaries, player_pos, camera_pos, grenade_list, explosions, expl1, map, walls_filtered)
        mp = multi_kill
        for x in explosions:
            m_k, m_k_t = x.tick(screen, player_actor, enemy_list ,map_render,camera_pos,explosions, multi_kill, multi_kill_ticks, walls_filtered)

            if m_k != None:
                multi_kill = m_k

            if m_k_t != None:
                multi_kill_ticks = m_k_t

        for x in burn_list:
            x.tick(screen, map_render)

        if mp != multi_kill:
            kill_counter = classes.kill_count_render(multi_kill, kill_rgb)








        time_stamps["misc"] = time.time() - t
        t = time.time()

        if map.top_layer != None:
            screen.blit(map.top_layer, [-camera_pos[0], -camera_pos[1]])


        if draw_los:
            los_image, draw_time = los.render_los_image(los_image, phase, camera_pos, player_pos,map, los_walls, debug_angle = player_actor.get_angle())

            ###
            ### OPTIMZE point_inits, finishing
            ###

            time_stamps["los_compute"] = time.time() - t
            t = time.time()
            #draw_time = 0
            start = time.time()

            screen.blit(los_image, (0, 0))

            draw_time2 = time.time() - start

            draw_time += time.time() - start

        try:
            if multiplayer:
                func.print_s(screen, "PING: " + str(round(last_ping*1000)) + "ms", 3)

                last_ping = last_ping * 59/60 + ping/60


        except Exception as e:
            print(e)

        time_stamps["los_draw"] = time.time() - t
        t = time.time()


        if draw_los:

            if 60*draw_time < 55:
                color = [255,255,255]
            else:
                color = [255,0,0]



            los_total_draw_time_frame = round(60*draw_time,3)

            if los_total_draw_time_frame < 0.8:
                color = [255,255,255]
            else:
                color = [255,0,0]

            perc1 = round(100*draw_time/(draw_time+draw_time2))
            perc2 = round(100*draw_time2/(draw_time+draw_time2))

        if wave_number >= 5:
            if not wave:
                text = terminal.render("EXIT DOOR IS OPEN!", False, [255,255,255])
                screen.blit(text, [size[0]/2 - text.get_rect().center[0], size[1] - 30 - text.get_rect().center[1]])



        if phase != 0:
            if phase == 1:
                t = "LINE OF SIGHT, POINTS"
            elif phase == 2:
                t = "LINE OF SIGHT, INTERSECT"
            elif phase == 3:
                t = "COLLISION"
            elif phase == 4:
                t = "NAV MESH"
            elif phase == 5:
                t = "RENDER TIMES"
            elif phase == 6:
                t = "ENEMY DEBUG"

            text = terminal3.render("DEVSCREEN: " + t, False, [255,255,255])
            screen.blit(text, [200, 20])


        if player_actor.get_hp() > 0:

            if not block_movement:
                func.draw_HUD(screen, player_inventory, cam_delta, camera_pos, c_weapon, player_weapons, player_actor, mouse_pos, clicked, r_click_tick,wave, wave_anim_ticks, round(wave_text_tick), wave_number, wave_text_color, beat_red)

            if not overworld:
                player_actor.set_sanity(0.005*sanity_drain)


            if phase == 3:
                map_points = map.__dict__["points_inside_polygons"]
                map_polygons = map.__dict__["polygons"]
                for point in map_points:
                    app.pygame.draw.circle(screen, [255,0,0], [point[0] - camera_pos[0], point[1] - camera_pos[1]], 5)

                for a,b,c,d in map_polygons:
                    for e,f in [[a,b], [b,c], [c,d], [d,a]]:
                        app.pygame.draw.line(screen, [255,255,255], [e[0] - camera_pos[0], e[1] - camera_pos[1]], [f[0] - camera_pos[0], f[1] - camera_pos[1]])


            if phase == 4:
                mo_pos_real = [mouse_pos[0] + camera_pos[0], mouse_pos[1] + camera_pos[1]]
                if r_click_tick:
                    ref_point = {"point" : [int(mo_pos_real[0]), int(mo_pos_real[1])], "connected" : []}


                    for point_dict in NAV_MESH:
                        point = point_dict["point"]
                        if point == ref_point["point"]:
                            continue
                        if los.check_los(point, ref_point["point"], walls_filtered):
                            ref_point["connected"].append(point)

                    NAV_MESH.append(ref_point)

                    file = open("nav_mesh.txt", "a")
                    file.write(str(ref_point["point"]) + "\n")
                    file.close()



                text = terminal3.render("APPARENT POS: " +str(round(mo_pos_real[0])) + " " +  str(round(mo_pos_real[1])), False, [255,255,255])
                screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 20])
                app.pygame.draw.line(screen, [255,255,255], mouse_pos, [mouse_pos[0] + 20, mouse_pos[1] + 20])
                pos = [(mouse_pos[0] + camera_pos[0]) * mouse_conversion, (mouse_pos[1] + camera_pos[1]) * mouse_conversion]
                text = terminal3.render("REAL POS: " + str(round(pos[0])) + " " +  str(round(pos[1])), False, [255,255,255])
                screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 40])



                for point_dict in NAV_MESH:
                    point = point_dict["point"]
                    app.pygame.draw.circle(screen, [255,0,0], [point[0] - camera_pos[0], point[1] - camera_pos[1]], 5)
                    for point_2 in point_dict["connected"]:
                        app.pygame.draw.line(screen, [255,255,255], [point[0] - camera_pos[0], point[1] - camera_pos[1]], [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]],1)

                calc_time_1 = time.time()
                route = func.calc_route(player_pos, mo_pos_real, NAV_MESH, walls_filtered)
                calc_time_2 = time.time() - calc_time_1
                point_2 = player_pos
                for point in route:
                    app.pygame.draw.line(screen, [255,0,0], [point[0] - camera_pos[0], point[1] - camera_pos[1]], [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]], 4)
                    point_2 = point
                app.pygame.draw.line(screen, [255,0,0], [mo_pos_real[0] - camera_pos[0], mo_pos_real[1] - camera_pos[1]], [point_2[0] - camera_pos[0], point_2[1] - camera_pos[1]], 4)

                text = terminal3.render("CALC TIME: " + str(round(calc_time_2*1000,2)) + "ms", False, [255,255,255])
                screen.blit(text, [mouse_pos[0] + 20, mouse_pos[1] + 60])
            if dialogue != []:
                text_str = dialogue[0].main(screen, mouse_pos, click_single_tick, scroll, glitch, app, player_inventory, items, player_actor)

                if text_str != "":



                    pygame.draw.rect(screen, [255,255,255], [size[0]/4, 3*size[1]/4-20, size[0]/2, size[1]/4],4)

                    pygame.draw.line(screen, [255,255,255], [size[0]/4, 3*size[1]/4 + 10], [3 * size[0]/4 - 5, 3*size[1]/4 + 10], 4)

                    y_pos = - 10 * len(text_str[1].split("\n"))

                    for text_line in text_str[1].split("\n"):

                        text = terminal.render(text_line, False, [255,255,255])
                        pos = [size[0] / 2, 7 * size[1] / 8]
                        screen.blit(text, [pos[0] - text.get_rect().center[0], pos[1] - text.get_rect().center[1] +5 + y_pos])

                        y_pos += 20

                    if text_str[0] == "You":
                        text = terminal.render(text_str[0], False, [255,255,255])
                        pos = [3 * size[0]/4-8 - text.get_rect().size[0], 3*size[1]/4-15]
                    else:
                        text = terminal.render(text_str[0], False, [255,255,255])
                        pos = [size[0]/4+5, 3*size[1]/4-15]

                    screen.blit(text, [pos[0], pos[1]])


        else:
            text = terminal.render("RESPAWN IN", False, [255,255,255])
            pos = [size[0] / 2, size[1] / 2-40]
            screen.blit(text, [pos[0] - text.get_rect().center[0], pos[1] - text.get_rect().center[1]])

            if respawn_ticks <= 40:
                t = "1"
            elif respawn_ticks <= 80:
                t = "2"
            else:
                t = "3"

            text = terminal2.render(t, False, [255,255,255])
            pos = [size[0] / 2, size[1] / 2]
            screen.blit(text, [pos[0] - text.get_rect().center[0], pos[1] - text.get_rect().center[1]])



        try:
            kill_counter.tick(screen, cam_delta, kill_counter)
        except:
            pass




        if multiplayer:
            text = terminal3.render("MULTIPLAYER", False, [255,255,255])
            screen.blit(text, [400,20])
            text = terminal3.render(self_name, False, [255,255,255])
            screen.blit(text, [400,40])
        else:
            zombie_events.clear()


        if phase != 5:
            try:
                func.print_s(screen, "FPS: " + str(round(1/(sum(fps)/60))), 1)
                pass
            except:
                pass

            func.print_s(screen, "KILLS: " + str(kills), 2)

            time_elapsed = round(time.time() - start_time)

            minutes = round((time_elapsed-29.9)/60)

            seconds = time_elapsed - minutes * 60

            if len(str(seconds)) == 1:
                seconds = "0" + str(seconds)

            func.print_s(screen, f"{minutes}:{seconds}",3)




        else:
            obje = enumerate(time_stamps, 1)
            total = 0
            try:
                for i, k in obje:
                    time_stamps[k] = time_stamps[k]*1/20 + last_time_stamp[k]*19/20

                    color = [255,round(255/(1 + time_stamps[k]*1000)), round(255/(1 + time_stamps[k]*1000))]


                    func.print_s(screen, k + ":" + str(round(time_stamps[k]*1000,1)) + "ms", i, color = color)

                    total += time_stamps[k]
                if total > 1/60:
                    color = [255,0,0]
                else:
                    color = [255,255,255]
                func.print_s(screen, "TOTAL" + ":" + str(round(total*1000,1)) + "ms (" + str(round(1/total)) + "FPS)", i+1, color = color)
            except Exception as e:
                print(e)


        last_time_stamp = time_stamps.copy()

        if wave_anim_ticks[0] > 0:
            wave_anim_ticks[0] -= timedelta.mod(1)
        if wave_anim_ticks[1] > 0:
            wave_anim_ticks[1] -= timedelta.mod(1)
        try:

            if multiplayer:
                for list_1, list_copy, slot in [[bullet_list, bullet_list_copy, "bullets"], [grenade_list, grenade_list_copy, "grenades"]]:

                    if slot not in packet_dict:
                        packet_dict[slot] = []

                    for object in reversed(list_1):
                        if object not in list_copy and object.__dict__["mp"] == False:
                            packet_dict[slot].append(object)
                        else:
                            break
                    list_copy = list_1.copy()


        except Exception as e:
            print(e)


        if not fade_tick.tick():
            tick = fade_tick.rounded()
            if 0 <= tick <= 9:
                screen.blit(fade_to_black_screen[tick], [0,0])

            elif 51 <= tick <= 60:
                screen.blit(fade_to_black_screen[60 - tick], [0,0])

            else:
                screen.fill([0,0,0])

        if not map_desc_tick.tick() and map_desc_tick.value > 20:
            tick = map_desc_tick.value - 20
            alpha = 255
            if tick < 40:
                alpha = 255 * tick/40

            elif 160 > tick > 100:
                alpha = 255 * (160 - tick)/60

            text = terminal_map_desc.render(map.name, False, [255,255,255])
            text.set_alpha(alpha)
            screen.blit(text, [size[0]/2 - text.get_rect().center[0], size[1]/3 - text.get_rect().center[1]])








        if pause:
            background_surf.blit(screen, (0,0))
        glitch.tick()
        if full_screen_mode:
            app.pygame.transform.scale(screen, full_screen.get_rect().size, full_screen)
        melee_list.clear()
        app.pygame.display.update()

if __name__ == "__main__":
    main()
