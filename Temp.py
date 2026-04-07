from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

windowWidth, windowHeight = 500, 600
catcherX = 250
diamondX = random.randint(50, 450)
diamondY = 550
diamondSpeed = 2.0
score = 0
gameOver = False
paused = False
cheatMode = False
diamondColor = [random.random(), random.random(), random.random()]

# --- MIDPOINT LINE ALGORITHM ---
def drawPixel(x, y, color):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def getZone(x1, y1, x2, y2):
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

def mapToZone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y

def mapFromZone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y

def drawLine(x1, y1, x2, y2, color):
    zone = getZone(x1, y1, x2, y2)
    x1, y1 = mapToZone0(x1, y1, zone)
    x2, y2 = mapToZone0(x2, y2, zone)
    dx, dy = x2 - x1, y2 - y1
    d = 2 * dy - dx
    incE, incNE = 2 * dy, 2 * (dy - dx)
    x, y = x1, y1
    while x <= x2:
        cx, cy = mapFromZone0(x, y, zone)
        drawPixel(cx, cy, color)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1

# --- GAME OBJECTS ---
def drawOptn():
    # Left Arrow (Restart)
    drawLine(20, 570, 50, 570, (0, 0.8, 0.8))
    drawLine(20, 570, 35, 585, (0, 0.8, 0.8))
    drawLine(20, 570, 35, 555, (0, 0.8, 0.8))
    
    # Play/Pause
    if not paused:
        drawLine(245, 585, 245, 555, (1, 0.7, 0))
        drawLine(255, 585, 255, 555, (1, 0.7, 0))
    else:
        drawLine(245, 585, 245, 555, (1, 0.7, 0))
        drawLine(245, 585, 265, 570, (1, 0.7, 0))
        drawLine(245, 555, 265, 570, (1, 0.7, 0))
        
    # Cross (Exit)
    drawLine(450, 585, 480, 555, (1, 0, 0))
    drawLine(450, 555, 480, 585, (1, 0, 0))

def drawGame():
    global diamondColor, diamondX, diamondY, catcherX, gameOver
    # Diamond
    if not gameOver:
        drawLine(diamondX, diamondY+15, diamondX-10, diamondY, diamondColor)
        drawLine(diamondX-10, diamondY, diamondX, diamondY-15, diamondColor)
        drawLine(diamondX, diamondY-15, diamondX+10, diamondY, diamondColor)
        drawLine(diamondX+10, diamondY, diamondX, diamondY+15, diamondColor)
    
    # Catcher
    c = (1, 0, 0) if gameOver else (1, 1, 1)
    drawLine(catcherX-50, 25, catcherX+50, 25, c)
    drawLine(catcherX-40, 10, catcherX+40, 10, c)
    drawLine(catcherX-50, 25, catcherX-40, 10, c)
    drawLine(catcherX+50, 25, catcherX+40, 10, c)

# --- GAME LOGIC ---
def animate():
    global diamondY, diamondX, gameOver, score, diamondSpeed, diamondColor, catcherX, cheatMode
    if not paused and not gameOver:
        if cheatMode:
            # Chase the diamond
            cheatSpeed = 4.5 
            if catcherX < diamondX:
                catcherX += cheatSpeed
            elif catcherX > diamondX:
                catcherX -= cheatSpeed
            
            # catcher within screen boundaries
            if catcherX < 50: catcherX = 50
            if catcherX > 450: catcherX = 450

        diamondY -= diamondSpeed
        
        # Collision Detection
        if diamondY <= 25 and diamondY >= 10 and catcherX - 55 <= diamondX <= catcherX + 55:
            score += 1
            print(f"Score: {score}") 
            diamondY, diamondX = 550, random.randint(50, 450)
            diamondSpeed += 0.1
            diamondColor = [random.random(), random.random(), random.random()]
        elif diamondY < 0:
            gameOver = True
            print(f"Game Over! Final Score: {score}")
    glutPostRedisplay()

def mouseClick(button, state, x, y):
    global paused, gameOver, score, diamondSpeed, diamondY
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        my = windowHeight - y
        if 555 <= my <= 585:
            if 20 <= x <= 50: # Restart 
                score, diamondSpeed, diamondY, gameOver = 0, 2.0, 550, False
                print("Starting Over!")
            elif 240 <= x <= 270: # Pause 
                if not gameOver: paused = not paused
            elif 450 <= x <= 480: # Exit
                print(f"Goodbye! Final Score: {score}")
                if bool(glutLeaveMainLoop): 
                    glutLeaveMainLoop()
                else:
                    glutDestroyWindow(glutGetWindow()) 

def specialKeys(key, x, y):
    global catcherX
    if not paused and not gameOver:
        if key == GLUT_KEY_LEFT and catcherX > 40: catcherX -= 20 
        if key == GLUT_KEY_RIGHT and catcherX < 460: catcherX += 20 

def keyboard(key, x, y):
    global cheatMode
    if key == b'c': 
        cheatMode = not cheatMode 
        print(f"Cheat Mode: {'ON' if cheatMode else 'OFF'}")

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    drawOptn()
    drawGame()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(windowWidth, windowHeight)
    glutCreateWindow(b"Catch the Diamonds!")
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, windowWidth, 0, windowHeight, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouseClick)
    glutSpecialFunc(specialKeys)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()