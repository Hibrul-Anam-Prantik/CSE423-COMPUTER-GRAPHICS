from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

cam_orbit_angle   = 0    # horizontal orbit angle 
cam_elevation_y   = 500  # third person view
cam_orbit_radius  = 700  # orbit distance from origin
fovY              = 80
ARENA_HALF        = 600  # half sqaure arena

# cameraMode
fp_mode_active    = False  # right-click  
cheat_vision_on   = False  # V nearest enemy

#player
plyr_x            = 0.0
plyr_y            = 0.0
plyr_gun_angle    = 0.0    # gun facing direction 
PLYR_STEP         = 18.0   # fast player movement
GUN_TURN_STEP     = 5.0
PLYR_FALLEN       = False   

#Score
life_remaining    = 5
game_score        = 0
bullets_missed    = 0
MAX_MISSED        = 10
game_over_flag    = False

#Bullet
BULLET_SPEED      = 14.0
BULLET_HALF       = 7
active_bullets    = []  # list of {x, y, dx, dy}

#enemy
ENEMY_COUNT            = 5
ENEMY_SPEED            = 0.25  
ENEMY_HIT_DIST         = 45      
BULLET_HIT_DIST        = 100      
ENEMY_HIT_COOLDOWN_MAX = 120  #immunity

# pulse / shrink-expand animation
enemy_pulse_t     = 0.0
ENEMY_BASE_R      = 30.0
ENEMY_PULSE_AMP   = 8.0
ENEMY_PULSE_FREQ  = 0.015

def _make_enemy_dict(ex, ey):
    return {"x": ex, "y": ey, "hit_cd": 0}

def _rand_enemy_spawn():
    
    while True:
        ex = random.uniform(-ARENA_HALF + 80, ARENA_HALF - 80)
        ey = random.uniform(-ARENA_HALF + 80, ARENA_HALF - 80)
        if math.hypot(ex - plyr_x, ey - plyr_y) > 260:
            return _make_enemy_dict(ex, ey)

enemies_list = [_rand_enemy_spawn() for _ in range(ENEMY_COUNT)]


#cheatMode
 
cheat_mode_on     = False
cheatFire         = 0   

# Tolerance (degrees): if an enemy falls within this cone of the gun angle,
# it is considered "in front" and cheat mode fires.
CHEAT_AIM_TOLERANCE = 10.0

#utility
def deg2rad(d):
    return d * math.pi / 180.0

def angle_gap(a, b):
    #Smallest angular difference between two angles
    diff = abs(a - b) % 360
    return diff if diff <= 180 else 360 - diff

def draw_text(scr_x, scr_y, text_str, font=GLUT_BITMAP_HELVETICA_18):
    #Render a string at 2-D screen position (scr_x, scr_y)
    glColor3f(1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(scr_x, scr_y)
    for ch in text_str:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_arena_grid():
    CELL_SIZE   = 120
    num_cells   = int(2 * ARENA_HALF / CELL_SIZE)
    WALL_HEIGHT = 140

    tile_purple = (0.65, 0.55, 0.90)
    tile_white  = (1.00, 1.00, 1.00)

    #floor
    glBegin(GL_QUADS)
    for row in range(num_cells):
        for col in range(num_cells):
            x0 = -ARENA_HALF + col * CELL_SIZE
            y0 = -ARENA_HALF + row * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE
            glColor3f(*(tile_purple if (row + col) % 2 == 0 else tile_white))
            glVertex3f(x0, y0, 0); glVertex3f(x1, y0, 0)
            glVertex3f(x1, y1, 0); glVertex3f(x0, y1, 0)
    glEnd()

    # boundary
    H = ARENA_HALF
    glBegin(GL_QUADS)

    # wall-color
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-H,  H, 0);           glVertex3f( H,  H, 0)
    glVertex3f( H,  H, WALL_HEIGHT); glVertex3f(-H,  H, WALL_HEIGHT)

    # Near wall, Gray
    glColor3f(0.25, 0.25, 0.25)
    glVertex3f(-H, -H, 0);           glVertex3f( H, -H, 0)
    glVertex3f( H, -H, WALL_HEIGHT); glVertex3f(-H, -H, WALL_HEIGHT)

    # Left wall, Blue
    glColor3f(0.0, 0.20, 1.0)
    glVertex3f(-H, -H, 0);           glVertex3f(-H,  H, 0)
    glVertex3f(-H,  H, WALL_HEIGHT); glVertex3f(-H, -H, WALL_HEIGHT)

    # Right wall, green
    glColor3f(0.0, 0.85, 0.0)
    glVertex3f( H, -H, 0);           glVertex3f( H,  H, 0)
    glVertex3f( H,  H, WALL_HEIGHT); glVertex3f( H, -H, WALL_HEIGHT)

    glEnd()
 
#  Shapes: sphere (head) and cylinders (gun barrel) and cuboids (legs)
 
def draw_player_model(fallen=False):
    glPushMatrix()
    glTranslatef(plyr_x, plyr_y, 0)
    glRotatef(plyr_gun_angle, 0, 0, 1)  #rotating towards gun angle

    if fallen:
        glRotatef(90, 1, 0, 0)           #falls down and game over

    #blue vertical cylinder
    glColor3f(0.15, 0.40, 0.80)
    glPushMatrix()
    glTranslatef(0, 0, 18)
    gluCylinder(gluNewQuadric(), 13, 13, 48, 12, 4)
    glPopMatrix()

    #skin-tone sphere
    glColor3f(0.92, 0.76, 0.50)
    glPushMatrix()
    glTranslatef(0, 0, 74)
    gluSphere(gluNewQuadric(), 16, 14, 14)
    glPopMatrix()

    # left leg,dark-blue cuboid
    glColor3f(0.10, 0.28, 0.55)
    glPushMatrix()
    glTranslatef(-9, 0, 8)
    glScalef(9, 9, 20)
    glutSolidCube(1)
    glPopMatrix()

    # right leg, dark-blue cuboid
    glColor3f(0.10, 0.28, 0.55)
    glPushMatrix()
    glTranslatef(9, 0, 8)
    glScalef(9, 9, 20)
    glutSolidCube(1)
    glPopMatrix()

    # gun barrel, yellow cylinder
    glColor3f(0.88, 0.78, 0.08)
    glPushMatrix()
    glTranslatef(0, 0, 52)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 3.5, 50, 8, 2)
    glPopMatrix()

    glPopMatrix()

#enemyModel

def draw_single_enemy(ex, ey, body_r):
    glPushMatrix()
    glTranslatef(ex, ey, 0)

    # body
    glColor3f(0.90, 0.08, 0.08)
    glPushMatrix()
    glTranslatef(0, 0, body_r)
    gluSphere(gluNewQuadric(), body_r, 14, 14)
    glPopMatrix()

    # head
    head_r = body_r * 0.38
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0, 0, body_r * 2 + head_r * 0.6)
    gluSphere(gluNewQuadric(), head_r, 10, 10)
    glPopMatrix()

    glPopMatrix()

def draw_all_enemies():
    cur_r = ENEMY_BASE_R + ENEMY_PULSE_AMP * math.sin(
        enemy_pulse_t * ENEMY_PULSE_FREQ * 2 * math.pi)
    for en in enemies_list:
        draw_single_enemy(en["x"], en["y"], cur_r)

# bullteModel

def draw_all_bullets():
    glColor3f(1.0, 0.92, 0.08)
    for blt in active_bullets:
        glPushMatrix()
        glTranslatef(blt["x"], blt["y"], 22)
        glutSolidCube(BULLET_HALF * 2)
        glPopMatrix()


# bulletFiring

def fire_one_bullet():
    if game_over_flag:
        return
    rad = deg2rad(plyr_gun_angle)
    active_bullets.append({
        "x":  float(plyr_x),
        "y":  float(plyr_y),
        "dx": math.cos(rad) * BULLET_SPEED,
        "dy": math.sin(rad) * BULLET_SPEED,
    })

#enemyRespawn

def respawn_enemy_away():
    while True:
        ex = random.uniform(-ARENA_HALF + 80, ARENA_HALF - 80)
        ey = random.uniform(-ARENA_HALF + 80, ARENA_HALF - 80)
        if math.hypot(ex - plyr_x, ey - plyr_y) > 260:
            return ex, ey

#GameConditions

def update_game_logic():
    global active_bullets, life_remaining
    global bullets_missed, game_score, game_over_flag, PLYR_FALLEN

    # tick hit cooldowns
    for en in enemies_list:
        if en["hit_cd"] > 0:
            en["hit_cd"] -= 1

    # move bullet and count missed ones
    still_flying = []
    for blt in active_bullets:
        blt["x"] += blt["dx"]
        blt["y"] += blt["dy"]
        if abs(blt["x"]) > ARENA_HALF or abs(blt["y"]) > ARENA_HALF:
            bullets_missed += 1
            if bullets_missed >= MAX_MISSED and not game_over_flag:
                game_over_flag = True
                PLYR_FALLEN    = True
        else:
            still_flying.append(blt)
    active_bullets[:] = still_flying

    # bullet vs enemy collision
    undestroyed = []
    for blt in active_bullets:
        struck = False
        for en in enemies_list:
            if math.hypot(blt["x"] - en["x"], blt["y"] - en["y"]) < BULLET_HIT_DIST:
                struck = True
                game_score += 1
                en["x"], en["y"] = respawn_enemy_away()
                en["hit_cd"] = ENEMY_HIT_COOLDOWN_MAX
                break
        if not struck:
            undestroyed.append(blt)
    active_bullets[:] = undestroyed

    # enemies approaching player
    for en in enemies_list:
        ddx  = plyr_x - en["x"]
        ddy  = plyr_y - en["y"]
        dist = math.hypot(ddx, ddy)
        if dist > 1:
            en["x"] += (ddx / dist) * ENEMY_SPEED
            en["y"] += (ddy / dist) * ENEMY_SPEED

    # enemy touches player
    for en in enemies_list:
        if en["hit_cd"] > 0:
            continue
        if math.hypot(plyr_x - en["x"], plyr_y - en["y"]) < ENEMY_HIT_DIST:
            life_remaining  -= 1
            en["hit_cd"]     = ENEMY_HIT_COOLDOWN_MAX
            en["x"], en["y"] = respawn_enemy_away()
            if life_remaining <= 0 and not game_over_flag:
                game_over_flag = True
                PLYR_FALLEN    = True


#cheatModeLogic
def update_cheat_mode():
    global plyr_gun_angle, cheatFire

    if not cheat_mode_on or game_over_flag:
        return

    # slow continuous gun rotation
    plyr_gun_angle = (plyr_gun_angle + GUN_TURN_STEP * 0.35) % 360

    # decrement fire cooldown
    if cheatFire > 0:
        cheatFire -= 1

    # scanning enemies
    if cheatFire == 0:
        for en in enemies_list:
            bearing_to_enemy = math.degrees(
                math.atan2(en["y"] - plyr_y, en["x"] - plyr_x)
            ) % 360
            if angle_gap(plyr_gun_angle, bearing_to_enemy) <= CHEAT_AIM_TOLERANCE:
                fire_one_bullet()
                cheatFire = 12   # pause to avoid wasting bulltes
                break                  # one shot per frame

 
def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 1.0, 3000.0)   # zNear = 1.0 (not 0.1) avoids clip glitch
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if fp_mode_active:
        rad          = deg2rad(plyr_gun_angle)
        cam_behind_x = plyr_x - math.cos(rad) * 20.0
        cam_behind_y = plyr_y - math.sin(rad) * 20.0
        cam_z        = 85.0       # eye height 

        if cheat_vision_on and cheat_mode_on and enemies_list:
            nearest_en  = min(enemies_list,
                              key=lambda e: math.hypot(e["x"] - plyr_x, e["y"] - plyr_y))
            look_x = nearest_en["x"]
            look_y = nearest_en["y"]
            look_z = ENEMY_BASE_R   # aiming at enemy's base
        else:
            # looking alongside gun direction
            look_x = cam_behind_x + math.cos(rad) * 400.0
            look_y = cam_behind_y + math.sin(rad) * 400.0
            look_z = cam_z

        gluLookAt(cam_behind_x, cam_behind_y, cam_z,
                  look_x,       look_y,       look_z,
                  0, 0, 1)
    else:
        # thirdPerson view  
        rad   = deg2rad(cam_orbit_angle)
        cam_x = cam_orbit_radius * math.cos(rad)
        cam_y = cam_orbit_radius * math.sin(rad)
        gluLookAt(cam_x, cam_y, cam_elevation_y,
                  0.0,   0.0,   0.0,
                  0,     0,     1)

#keyListener 
def keyboardListener(key, x, y):
    global plyr_x, plyr_y, plyr_gun_angle
    global cheat_mode_on, cheat_vision_on
    global life_remaining, game_score, bullets_missed
    global game_over_flag, PLYR_FALLEN, active_bullets, enemies_list

    # R always resets 
    if key == b'r':
        life_remaining  = 5
        game_score      = 0
        bullets_missed  = 0
        game_over_flag  = False
        PLYR_FALLEN     = False
        plyr_x          = 0.0
        plyr_y          = 0.0
        plyr_gun_angle  = 0.0
        cheat_mode_on   = False
        cheat_vision_on = False
        active_bullets  = []
        enemies_list[:] = [_rand_enemy_spawn() for _ in range(ENEMY_COUNT)]
        return

    if game_over_flag:
        return

    # w and s
    if key == b'w':
        rad = deg2rad(plyr_gun_angle)
        nx  = plyr_x + math.cos(rad) * PLYR_STEP
        ny  = plyr_y + math.sin(rad) * PLYR_STEP
        if abs(nx) < ARENA_HALF - 20 and abs(ny) < ARENA_HALF - 20:
            plyr_x, plyr_y = nx, ny

    if key == b's':
        rad = deg2rad(plyr_gun_angle)
        nx  = plyr_x - math.cos(rad) * PLYR_STEP
        ny  = plyr_y - math.sin(rad) * PLYR_STEP
        if abs(nx) < ARENA_HALF - 20 and abs(ny) < ARENA_HALF - 20:
            plyr_x, plyr_y = nx, ny

    # a and d, gun rotation
    if key == b'a':
        plyr_gun_angle = (plyr_gun_angle + GUN_TURN_STEP) % 360
    if key == b'd':
        plyr_gun_angle = (plyr_gun_angle - GUN_TURN_STEP) % 360

    # C enables cheat mode
    if key == b'c':
        cheat_mode_on = not cheat_mode_on

    # V enables cheat vision
    if key == b'v':
        cheat_vision_on = not cheat_vision_on

#Arrow keys
def specialKeyListener(key, x, y):
    global cam_orbit_angle, cam_elevation_y

    if key == GLUT_KEY_LEFT:
        cam_orbit_angle = (cam_orbit_angle + 3) % 360
    if key == GLUT_KEY_RIGHT:
        cam_orbit_angle = (cam_orbit_angle - 3) % 360
    if key == GLUT_KEY_UP:
        cam_elevation_y = min(cam_elevation_y + 15, 1200)
    if key == GLUT_KEY_DOWN:
        cam_elevation_y = max(cam_elevation_y - 15, 40)

 
# mouseListener

def mouseListener(button, state, mx, my):
    global fp_mode_active

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_one_bullet()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fp_mode_active = not fp_mode_active


def idle():
    global enemy_pulse_t
    if not game_over_flag:
        update_game_logic()
        update_cheat_mode()
        enemy_pulse_t += 1
    glutPostRedisplay()


#rendering


def showScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    draw_arena_grid()
    draw_player_model(fallen=PLYR_FALLEN)
    draw_all_enemies()
    draw_all_bullets()

    # ── HUD ── (matches reference screenshot text exactly)
    draw_text(10, 775, f"Player Life Remaining: {life_remaining}")
    draw_text(10, 750, f"Game Score: {game_score}")
    draw_text(10, 725, f"Player Bullet Missed: {bullets_missed}")

    # status indicators
    mode_str = "FP" if fp_mode_active else "3P"
    draw_text(10, 700, f"[{mode_str}]  Cheat: {'ON' if cheat_mode_on else 'OFF'}  CheatVision: {'ON' if cheat_vision_on else 'OFF'}")

    if game_over_flag:
        draw_text(280, 420, "GAME OVER  -  Press R to Restart", GLUT_BITMAP_TIMES_ROMAN_24)

    glutSwapBuffers()
 

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy - 3D OpenGL")

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()
