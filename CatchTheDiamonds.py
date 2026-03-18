from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

window_width, window_height = 500, 600
catcher_x = 250
diamond_x = random.randint(50, 450)
diamond_y = 550
diamond_speed = 2.0
score = 0
game_over = False
paused = False
cheat_mode = False
diamond_color = [random.random(), random.random(), random.random()]

def draw_pixel(x, y, color):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def get_zone(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: return 0
        if dx < 0 and dy >= 0: return 3
        if dx < 0 and dy < 0: return 4
        return 7
    else:
        if dx >= 0 and dy >= 0: return 1
        if dx < 0 and dy >= 0: return 2
        if dx < 0 and dy < 0: return 5
        return 6

def map_to_zone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y

def map_from_zone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y

def draw_line(x1, y1, x2, y2, color):
    zone = get_zone(x1, y1, x2, y2)
    x1, y1 = map_to_zone0(x1, y1, zone)
    x2, y2 = map_to_zone0(x2, y2, zone)
    dx, dy = x2 - x1, y2 - y1
    d = 2 * dy - dx
    incE, incNE = 2 * dy, 2 * (dy - dx)
    x, y = x1, y1
    while x <= x2:
        cx, cy = map_from_zone0(x, y, zone)
        draw_pixel(cx, cy, color)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1

def draw_ui():
    # Left Arrow (Restart) - Teal
    draw_line(20, 570, 50, 570, (0, 0.8, 0.8))
    draw_line(20, 570, 35, 585, (0, 0.8, 0.8))
    draw_line(20, 570, 35, 555, (0, 0.8, 0.8))
    
    # Play/Pause - Amber
    if not paused:
        draw_line(245, 585, 245, 555, (1, 0.7, 0))
        draw_line(255, 585, 255, 555, (1, 0.7, 0))
    else:
        draw_line(245, 585, 245, 555, (1, 0.7, 0))
        draw_line(245, 585, 265, 570, (1, 0.7, 0))
        draw_line(245, 555, 265, 570, (1, 0.7, 0))
        
    # Cross (Exit) - Red
    draw_line(450, 585, 480, 555, (1, 0, 0))
    draw_line(450, 555, 480, 585, (1, 0, 0))

def draw_game():
    global diamond_color
    # Diamond
    if not game_over:
        draw_line(diamond_x, diamond_y+15, diamond_x-10, diamond_y, diamond_color)
        draw_line(diamond_x-10, diamond_y, diamond_x, diamond_y-15, diamond_color)
        draw_line(diamond_x, diamond_y-15, diamond_x+10, diamond_y, diamond_color)
        draw_line(diamond_x+10, diamond_y, diamond_x, diamond_y+15, diamond_color)
    
    # Catcher
    c = (1, 0, 0) if game_over else (1, 1, 1)
    draw_line(catcher_x-40, 40, catcher_x+40, 40, c)
    draw_line(catcher_x-30, 10, catcher_x+30, 10, c)
    draw_line(catcher_x-40, 40, catcher_x-30, 10, c)
    draw_line(catcher_x+40, 40, catcher_x+30, 10, c)


def animate():
    global diamond_y, diamond_x, game_over, score, diamond_speed, diamond_color, catcher_x
    if not paused and not game_over:
        if cheat_mode:
            # Move catcher towards diamond_x gradually
            cheat_speed = 2.0  # Adjust this to make the "bot" faster or slower
            if catcher_x < diamond_x:
                catcher_x += cheat_speed
            elif catcher_x > diamond_x:
                catcher_x -= cheat_speed
            
            # Boundary checks to keep catcher on screen
            if catcher_x < 40: catcher_x = 40
            if catcher_x > 460: catcher_x = 460

        diamond_y -= diamond_speed
        
        # Collision Detection (AABB) 
        if diamond_y <= 40 and diamond_y >= 10 and catcher_x - 45 <= diamond_x <= catcher_x + 45:
            score += 1
            print(f"Score: {score}") 
            diamond_y, diamond_x = 550, random.randint(50, 450)
            diamond_speed += 0.1
            diamond_color = [random.random(), random.random(), random.random()]
        elif diamond_y < 0:
            game_over = True
            print(f"Game Over! Final Score: {score}")
    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global paused, game_over, score, diamond_speed, diamond_y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        my = window_height - y
        if 555 <= my <= 585:
            if 20 <= x <= 50: # Restart 
                score, diamond_speed, diamond_y, game_over = 0, 2.0, 550, False
                print("Starting Over!")
            elif 240 <= x <= 270: # Pause 
                if not game_over: paused = not paused
            elif 450 <= x <= 480: # Exit
                print(f"Goodbye! Final Score: {score}")
                if bool(glutLeaveMainLoop): 
                    glutLeaveMainLoop()
                else:
                    glutDestroyWindow(glutGetWindow()) 
                    os._exit(0)

def special_keys(key, x, y):
    global catcher_x
    if not paused and not game_over:
        if key == GLUT_KEY_LEFT and catcher_x > 40: catcher_x -= 20 
        if key == GLUT_KEY_RIGHT and catcher_x < 460: catcher_x += 20 

def keyboard(key, x, y):
    global cheat_mode
    if key == b'c': cheat_mode = not cheat_mode 

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_ui()
    draw_game()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Catch the Diamonds!")
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_click)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()