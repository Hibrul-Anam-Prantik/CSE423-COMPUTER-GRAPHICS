from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

points = []
speed_multiplier = 1.0
is_frozen = False
is_blinking = False
blink_timer = 0

def draw_points():
    glPointSize(10)
    glBegin(GL_POINTS)
    for p in points:
        if is_blinking and (blink_timer // 10) % 2 == 0:
            glColor3f(0, 0, 0)
        else:
            glColor3f(p['r'], p['g'], p['b'])
        glVertex2f(p['x'], p['y'])
    glEnd()

def animate():
    global blink_timer
    if not is_frozen:
        blink_timer += 1
        for p in points:
            p['x'] += p['dx'] * speed_multiplier
            p['y'] += p['dy'] * speed_multiplier

            if p['x'] >= 245 or p['x'] <= -245:
                p['dx'] *= -1
            if p['y'] >= 245 or p['y'] <= -245:
                p['dy'] *= -1
    
    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global is_blinking
    if is_frozen:
        return

    mx = x - 250
    my = 250 - y

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        p = {
            'x': mx,
            'y': my,
            'dx': random.choice([-2, 2]),
            'dy': random.choice([-2, 2]),
            'r': random.random(),
            'g': random.random(),
            'b': random.random()
        }
        points.append(p)
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        is_blinking = not is_blinking

def keyboard_listener(key, x, y):
    global is_frozen
    if key == b' ':
        is_frozen = not is_frozen

def special_key_listener(key, x, y):
    global speed_multiplier
    if is_frozen:
        return
        
    if key == GLUT_KEY_UP:
        speed_multiplier += 0.2
    if key == GLUT_KEY_DOWN:
        speed_multiplier = max(0.1, speed_multiplier - 0.2)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_points()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"The Amazing Box")
    
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    
    glutMainLoop()

if __name__ == "__main__":
    main()