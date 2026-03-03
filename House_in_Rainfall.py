from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random 

rainDrops = []
for _ in range(100):
    x = random.randint(0, 500)
    y = random.randint(0, 500)
    rainDrops.append([x, y])

rainAngle = 0      # 0 -> straight, - -> left, + -> right
dayNight = 0.0   # 0 -> night, 1 -> day

def drawLines(x, y):
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glEnd()

def drawTriangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()
    
def drawField():
    # glColor3f(0.42, 0.56, 0.14)
    glColor3f(0.6, 0.4, 0.1)
    drawTriangle(0, 300, 0, 0, 500, 0)
    drawTriangle(0, 300, 500, 300, 500, 0)
    
def drawTrees():
    glColor3f(0.13, 0.55, 0.13)
    for x in range(0, 500, 40):
        # left-most -> x
        # right-most -> x+40
        # middle -> x+20
        drawTriangle(x, 240, x + 40, 240, x + 20, 290)

def drawHouse():
    drawField()
    drawTrees()
    # house body
    glColor3f(1.0, 0.98, 0.94)
    drawTriangle(187.5, 255, 187.5, 190, 312.5, 190)
    drawTriangle(312.5, 190, 312.5, 255, 187.5, 255)
    # roof
    glColor3f(0.6, 0.2, 0.8) 
    drawTriangle(170, 255, 330, 255, 250, 310)
    # door
    glColor3f(0.53, 0.81, 0.98)
    drawTriangle(235, 190, 265, 190, 265, 230)
    drawTriangle(235, 190, 235, 230, 265, 230)
    # Window -> left
    drawTriangle(200, 215, 225, 215, 225, 240)
    drawTriangle(200, 215, 200, 240, 225, 240)
    # Window -> right
    drawTriangle(275, 215, 300, 215, 300, 240)
    drawTriangle(275, 215, 275, 240, 300, 240)
    # door lock "."
    glColor3f(0, 0, 0)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(257, 213)
    glEnd()
    # window frames "+"
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(212.5, 215)
    glVertex2f(212.5, 240)
    glVertex2f(200, 227.5)
    glVertex2f(225, 227.5)
    glVertex2f(287.5, 215)
    glVertex2f(287.5, 240)
    glVertex2f(275, 227.5)
    glVertex2f(300, 227.5)
    glEnd()
    
def drawRain():
    # glColor3f(0.5, 0.5, 0.8)
    glColor3f(.8, .8, 1)
    glBegin(GL_LINES)
    for drop in rainDrops:
        glVertex2f(drop[0], drop[1])
        glVertex2f(drop[0] + rainAngle, drop[1] - 20) 
    glEnd()

def animate():
    global rainDrops
    for drop in rainDrops:
        drop[0] += rainAngle * 0.1
        drop[1] -= 4

        # if drop[1] < 0:
        #     drop[1] = 500
        #     drop[0] = random.randint(0, 500)
        
        if drop[0] > 500: # if directed to right
            drop[0] = 0 # falls from left

        elif drop[0] < 0: # if directed to left
            drop[0] = 500 # falls from right

        if drop[1] < 0:  # down to up
            drop[1] = 500
            drop[0] = random.randint(0, 500)

    glutPostRedisplay()
    
def keyboard_listener(key, x, y):
    global dayNight
    if key == b'd':
        dayNight = min(1.0, dayNight + 0.25) # 1/4 = 0.25
    elif key == b'n':
        dayNight = max(0.0, dayNight - 0.25)
    glutPostRedisplay()

def special_key_listener(key, x, y):
    global rainAngle
    if key == GLUT_KEY_LEFT: 
        rainAngle -= 2
    elif key == GLUT_KEY_RIGHT:
        rainAngle += 2
    glutPostRedisplay()

def setupProjection():
    # glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    
def display():
    # glClearColor(dayNight, dayNight, dayNight, 1.0)
    glClearColor(0.0, dayNight * 0.3, dayNight * 0.6, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setupProjection()
    
    drawField()
    drawTrees()
    drawHouse()
    drawRain()
    
    glutSwapBuffers()
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(450, 200)
    glutCreateWindow(b"A House in Rainfall")
    glutDisplayFunc(display)
    glutIdleFunc(animate)          
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener) 
    glutMainLoop()

if __name__ == "__main__":
    main()



